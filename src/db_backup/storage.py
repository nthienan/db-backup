import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime

from git import Repo


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
            logging.info('Git repo does not exist')
            os.makedirs(self.repo_dir)
            logging.info('Cloning git repo for the first run...')
            repo = Repo.clone_from(self.repo_url, self.repo_dir)
            logging.info('Repo has been cloned successfully')
        else:
            logging.info('Git pull changes from remote')
            repo = Repo(self.repo_dir)
            repo.git.pull('origin', 'master')

        files = list()
        for key, value in data.items():
            file_name = os.path.join(self.repo_dir, key)
            with open(file_name, 'wb') as f:
                f.write(value)
                files.append(file_name)

        if len(files) > 0:
            logging.debug('git add %s' % files)
            repo.index.add(files)
            time_stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            logging.info('Commit and push changes to remote')
            commit = repo.index.commit('automatically backup at %s UTC' % time_stamp)
            logging.debug('Git commit: %s - %s' % (commit.hexsha, commit.message))
            repo.git.push('origin', 'master')

    def retrieve(self, *args, **kwargs):
        pass
