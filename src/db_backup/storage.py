import logging
import os
from abc import ABC, abstractmethod

from git import Repo


class Storage(ABC):
    def __init__(self):
        self.supported = [
            'Git'
        ]
        self.type = None

    @abstractmethod
    def store(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def retrieve(self, *args, **kwargs):
        raise NotImplementedError()


class Git(Storage):
    def __init__(self, url=None, dir=None, versioning=True, **kwargs):
        super().__init__()
        self.repo_url = url
        self.repo_dir = dir
        self.versioning = versioning
        self.type = 'Git'

    def store(self, data=None, timestamp=None):
        logging.info('Git storage stores backup files...')
        if data is None:
            logging.info('Skipping Git storage due to no data')
            return
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
            if not self.versioning:
                key = '%s_%s' % (timestamp.strftime('%Y%m%d%H%M%S_UTC'), key)
            file_name = os.path.join(self.repo_dir, key)
            with open(file_name, 'wb') as f:
                f.write(value)
                files.append(file_name)

        if len(files) > 0:
            logging.debug('git add %s' % files)
            repo.index.add(files)
            time_stamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            logging.info('Commit and push changes to remote')
            commit = repo.index.commit('automatically backup at %s UTC' % time_stamp)
            logging.debug('Git commit: %s - %s' % (commit.hexsha, commit.message))
            repo.git.push('origin', 'master')
        logging.info('All backup files are stored. %s' % files)

    def retrieve(self, *args, **kwargs):
        pass


class Local(Storage):

    def __init__(self, dir=None, **kwargs):
        super().__init__()
        self.dir = dir
        self.type = 'Local'

    def store(self, data=None, timestamp=None):
        time_str = timestamp.strftime('%Y%m%d%H%M%S_UTC')
        if not os.path.exists(self.dir):
            logging.info('%s does not exist' % self.dir)
            os.makedirs(self.dir)

        files = list()
        logging.info('Local storage stores backup files...')
        for key, value in data.items():
            file_name = os.path.join(self.dir, '%s_%s' % (time_str, key))
            with open(file_name, 'wb') as f:
                f.write(value)
                files.append(file_name)
        logging.info('All backup files are stored. %s' % files)

    def retrieve(self, *args, **kwargs):
        pass
