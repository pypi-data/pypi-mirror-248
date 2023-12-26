import argparse
import logging
import importlib
import os
import sys
from typing import Any
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
import yaml
from schd import __version__ as schd_version


logger = logging.getLogger(__name__)


def build_job(job_name, job_class_name, config):
    if not '.' in job_class_name:
        module = sys.modules[__name__]
        job_cls = getattr(module, job_class_name)
    else:
        module_name, cls_name = job_class_name.rsplit('.', 1)
        m = importlib.import_module(module_name)
        job_cls = getattr(m, cls_name)

    if hasattr('job_cls', 'from_settings'):
        job = job_cls.from_settings(job_name=job_name, config=config)
    else:
        job = job_cls(**config)

    return job


class CommandJob:
    def __init__(self, cmd, job_name=None):
        self.cmd = cmd
        self.logger = logging.getLogger(f'CommandJob#{job_name}')

    @classmethod
    def from_settings(cls, job_name, config):
        return cls(cmd=config['cmd'], job_name=job_name)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.logger.info('Running command: %s', self.cmd)
        p = subprocess.run(self.cmd, shell=True, env=os.environ, stdout=sys.stdout, stderr=sys.stderr)
        self.logger.info('process completed, %s', p.returncode)
        self.logger.info('process output %s', p.stdout)


def read_config(config_file=None):
    if config_file is None and 'SCHD_CONFIG' in os.environ:
        config_file = os.environ['SCHD_CONFIG']

    if config_file is None:
        config_file = 'conf/schd.yaml'

    with open(config_file, 'r', encoding='utf8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config


def run_daemon(config_file=None):
    config = read_config(config_file=config_file)
    sched = BlockingScheduler(executors={'default': ThreadPoolExecutor(10)})

    for job_name, job_config in config['jobs'].items():
        job_class_name = job_config.pop('class')
        job_cron = job_config.pop('cron')
        job = build_job(job_name, job_class_name, job_config)
        sched.add_job(job, CronTrigger.from_crontab(job_cron), id=job_name, misfire_grace_time=10)
        logger.info('job added, %s', job_name)

    logger.info('scheduler starting.')
    sched.start()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--logfile')
    parser.add_argument('--config', '-c')
    args = parser.parse_args()
    config_file = args.config

    print(f'starting schd, {schd_version}, config_file={config_file}')

    if args.logfile:
        log_stream = open(args.logfile, 'a', encoding='utf8')
        sys.stdout = log_stream
        sys.stderr = log_stream
    else:
        log_stream = sys.stdout

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=log_stream)
    run_daemon(config_file)


if __name__ == '__main__':
    main()