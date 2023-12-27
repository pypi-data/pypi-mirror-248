import copy

from ray.air import RunConfig
from ray.tune.schedulers import ASHAScheduler
from ray.tune.search.optuna import OptunaSearch

from .utils import TimeoutStopper
from ..utils import find_port, check_type, is_notebook, beam_device
from ..logger import beam_logger as logger
from ..path import beam_path, BeamPath

import ray
from ray.tune import JupyterNotebookReporter, TuneConfig
from ray import tune, train
from functools import partial
from ..experiment import Experiment

import numpy as np
from .core import BeamHPO


class RayHPO(BeamHPO):

    @staticmethod
    def _categorical(param, choices):
        return tune.choice(choices)

    @staticmethod
    def _uniform(param, start, end):
        return tune.uniform(start, end)

    @staticmethod
    def _loguniform(param, start, end):
        return tune.loguniform(start, end)

    @staticmethod
    def _linspace(param, start, end, n_steps, endpoint=True, dtype=None):
        x = np.linspace(start, end, n_steps, endpoint=endpoint)
        step_size = (end - start) / n_steps
        end = end - step_size * (1 - endpoint)

        if np.sum(np.abs(x - np.round(x))) < 1e-8 or dtype in [int, np.int, np.int64, 'int', 'int64']:

            start = int(np.round(start))
            step_size = int(np.round(step_size))
            end = int(np.round(end))

            return tune.qrandint(start, end, step_size)

        return tune.quniform(start, end, (end - start) / n_steps)

    @staticmethod
    def _logspace(param, start, end, n_steps, base=None, dtype=None):

        if base is None:
            base = 10

        emin = base ** start
        emax = base ** end

        x = np.logspace(start, end, n_steps, base=base)

        if np.sum(np.abs(x - np.round(x))) < 1e-8 or dtype in [int, np.int, np.int64, 'int', 'int64']:
            base = int(x[1] / x[0])
            return tune.lograndint(int(emin), int(emax), base=base)

        step_size = (x[1] / x[0]) ** ( (end - start) / n_steps )
        return tune.qloguniform(emin, emax, step_size, base=base)

    @staticmethod
    def _randn(param, mu, sigma):
        return tune.qrandn(mu, sigma)

    @staticmethod
    def init_ray(runtime_env=None, dashboard_port=None, include_dashboard=True):

        ray.init(runtime_env=runtime_env, dashboard_port=dashboard_port,
                 include_dashboard=include_dashboard, dashboard_host="0.0.0.0")

    @staticmethod
    def shutdown_ray():
        ray.shutdown()

    def runner(self, config):

        hparams = self.generate_hparams(config)

        experiment = Experiment(hparams, hpo='tune', print_hyperparameters=False)
        alg, report = experiment(self.ag, return_results=True)
        train.report({report.objective_name: report.best_objective})

        self.tracker(algorithm=alg, results=report.data, hparams=hparams, suggestion=config)

    def run(self, *args, runtime_env=None, tune_config_kwargs=None, run_config_kwargs=None, **kwargs):

        hparams = copy.deepcopy(self.hparams)
        hparams.update(kwargs)

        search_space = self.get_suggestions()

        self.shutdown_ray()

        dashboard_port = find_port(port=self.hparams.get('dashboard_port'),
                                   get_port_from_beam_port_range=self.hparams.get('get_port_from_beam_port_range'))

        logger.info(f"Opening ray-dashboard on port: {dashboard_port}")
        self.init_ray(runtime_env=runtime_env, dashboard_port=int(dashboard_port),
                      include_dashboard=self.hparams.get('include_dashboard'))

        stop = kwargs.get('stop', None)
        train_timeout = hparams.get('train-timeout')
        if train_timeout is not None and train_timeout > 0:
            stop = TimeoutStopper(train_timeout)

        # fix gpu to device 0
        if self.experiment_hparams.get('device') != 'cpu':
            self.experiment_hparams.set('device', 'cuda')

        runner_tune = tune.with_resources(
                tune.with_parameters(partial(self.runner)),
                resources={"cpu": hparams.get('cpus-per-trial'),
                           "gpu": hparams.get('gpus-per-trial')}
            )

        tune_config_kwargs = tune_config_kwargs or {}
        if 'metric' not in tune_config_kwargs.keys():
            tune_config_kwargs['metric'] = self.experiment_hparams.get('objective')
        if 'mode' not in tune_config_kwargs.keys():
            mode = self.experiment_hparams.get('objective-mode')
            tune_config_kwargs['mode'] = self.get_optimization_mode(mode, tune_config_kwargs['metric'])

        if 'progress_reporter' not in tune_config_kwargs.keys() and is_notebook():
            tune_config_kwargs['progress_reporter'] = JupyterNotebookReporter(overwrite=True)

        tune_config_kwargs['num_samples'] = self.hparams.get('n_trials')
        tune_config_kwargs['max_concurrent_trials'] = self.hparams.get('n_jobs', 1)

        # if 'scheduler' not in tune_config_kwargs.keys():
        #     tune_config_kwargs['scheduler'] = ASHAScheduler()

        if 'search_alg' not in tune_config_kwargs.keys():
            metric = tune_config_kwargs['metric']
            mode = tune_config_kwargs['mode']
            tune_config_kwargs['search_alg'] = OptunaSearch(search_space, metric=metric, mode=mode)
            # tune_config_kwargs['search_alg'] = OptunaSearch()

        tune_config = TuneConfig(**tune_config_kwargs)

        local_dir = self.hparams.get('hpo_path')
        run_config = RunConfig(stop=stop, local_dir=local_dir)

        logger.info(f"Starting ray-tune hyperparameter optimization process. "
                    f"Results and logs will be stored at {local_dir}")

        tuner = tune.Tuner(runner_tune, param_space=None, tune_config=tune_config, run_config=run_config)
        analysis = tuner.fit()

        return analysis
