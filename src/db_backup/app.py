import logging
import os
import time

import yaml
from apscheduler.schedulers.background import BackgroundScheduler

from .worker import Worker


class Application:
    def __init__(self, cfg_file):
        self.cfg_file = cfg_file
        self.is_running = False
        self.init_logger()
        self.scheduler = BackgroundScheduler()

    def run(self, delay=30):
        self._load_config_file()
        time.sleep(delay)
        for db in self.cfg['backup']:
            worker = Worker(**db)
            worker.work()
        self.start()

    def start(self):
        self.is_running = True
        # backup_args = (self.opts.git_repo, self.opts.host, self.opts.port, self.opts.user, self.opts.password, self.opts.databases)
        # self.scheduler.add_job(func=backup, args=backup_args, trigger='cron', second='30')
        # self.scheduler.start()
        while self.is_running:
            time.sleep(30)

    def stop(self):
        self.is_running = False
        if self.scheduler.running:
            self.scheduler.shutdown()

    def _load_config_file(self):
        if not os.path.exists(self.cfg_file):
            raise RuntimeError('\'%s\' does not exist' % self.cfg_file)
        with open(self.cfg_file) as f:
            self.cfg = yaml.load(f)

    @classmethod
    def init_logger(cls):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
