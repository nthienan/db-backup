import logging
import os
import time

import yaml

from .scheduler import Scheduler
from .worker import Worker


class Application:
    def __init__(self, cfg_file):
        self.cfg_file = cfg_file
        self.is_running = False
        self._load_config_file()
        self.init_logger(self.cfg['logging']['level'])
        self.scheduler = Scheduler()

    def run(self, delay=30):
        time.sleep(delay)
        for db in self.cfg['backup']:
            self.scheduler.schedule(worker=Worker(**db), triggers=db['trigger'])
        self.scheduler.start()
        self.is_running = True
        while self.is_running:
            time.sleep(3)

    def stop(self):
        self.is_running = False
        if self.scheduler.is_running():
            self.scheduler.shutdown()

    def _load_config_file(self):
        if not os.path.exists(self.cfg_file):
            raise RuntimeError('\'%s\' does not exist' % self.cfg_file)
        with open(self.cfg_file) as f:
            self.cfg = yaml.load(f)

    @classmethod
    def init_logger(cls, level):
        logger = logging.getLogger()
        logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
