import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime

from git import Repo

logger = logging.getLogger()


class Storage(ABC):
    def __init__(self):
        self.supported = [
            'Git'
        ]
        self.type = None

    @abstractmethod
    def store(self, *args, **kwargs):
        pass

    @abstractmethod
    def retrieve(self, *args, **kwargs):
        pass


class Git(Storage):

    def __init__(self, url, dir, **kwargs):
        super().__init__()
        self.repo_url = url
        self.repo_dir = dir
        self.type = 'Git'

    def store(self, data):
        if not os.path.exists(os.path.join(self.repo_dir, '.git')):
            logger.info('Git repo does not exist')
            os.makedirs(self.repo_dir)
            logger.info('Cloning git repo for the first run...')
            repo = Repo.clone_from(self.repo_url, self.repo_dir)
            logger.info('Cloning is finished')
        else:
            logger.info('Pulling changes from remote...')
            repo = Repo(self.repo_dir)
            repo.git.pull('origin', 'master')
            logger.info('Pulling is finished')

        files = list()
        for key, value in data.items():
            file_name = os.path.join(self.repo_dir, key)
            with open(file_name, 'wb') as f:
                f.write(value)
                files.append(file_name)

        if len(files) > 0:
            logger.info('git add %s...' % files)
            repo.index.add(files)
            time_stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            logger.info('Committing and pushing change to git repo...')
            repo.index.commit('automatically backup at %s UTC' % time_stamp)
            repo.git.push('origin', 'master')
            logger.info('Pushing backup files has been finished')

    def retrieve(self, *args, **kwargs):
        pass
