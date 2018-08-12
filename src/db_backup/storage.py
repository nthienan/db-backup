import fnmatch
import logging
import os
import re
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

    def __init__(self, dir=None, numberToKeep=0, **kwargs):
        super().__init__()
        self.dir = dir
        self.num_to_keep = numberToKeep
        self.type = 'Local'

    def store(self, data=None, timestamp=None):
        logging.info('Local storage stores backup files...')
        time_str = timestamp.strftime('%Y%m%d%H%M%S_UTC')
        if not os.path.exists(self.dir):
            logging.debug('%s does not exist' % self.dir)
            os.makedirs(self.dir)
            logging.debug('%s has been created' % self.dir)

        files = list()
        for key, value in data.items():
            file_name = os.path.join(self.dir, '%s_%s' % (time_str, key))
            with open(file_name, 'wb') as f:
                f.write(value)
                files.append(file_name)
        logging.info('Backup files are stored. %s' % files)
        self._remove_oldest_backup(data.keys())

    def _remove_oldest_backup(self, db_names):
        all_files = os.listdir(self.dir)
        for db in db_names:
            filterred_files = dict()
            file_name_pattern = '*_%s' % db
            for f in all_files:
                if fnmatch.fnmatch(f, file_name_pattern):
                    epoch = _file_name_to_epoch_time(f)
                    filterred_files[epoch] = f
            keep_files = 0
            for key in sorted(filterred_files.keys(), reverse=True):
                if keep_files < self.num_to_keep:
                    keep_files = keep_files + 1
                else:
                    logging.info('Remove file %s due to exceed %s files to keep.' %
                                 (filterred_files[key], self.num_to_keep))
                    os.remove(os.path.join(self.dir, filterred_files[key]))

    def retrieve(self, *args, **kwargs):
        pass


def _file_name_to_epoch_time(file_name):
    file_regex = re.search(r'^([0-9]{14})*', file_name)
    time_str = file_regex.group(0)
    time = datetime.strptime(time_str, '%Y%m%d%H%M%S')
    return (time - datetime(1970, 1, 1)).total_seconds()
