import logging

from abc import ABC, abstractmethod
from subprocess import Popen, PIPE


class AbstractDB(ABC):
    @abstractmethod
    def backup(self, *args, **kwargs):
        pass

    @abstractmethod
    def restore(self, *args, **kwargs):
        pass


class MariaDB:
    def __init__(self, host='localhost', port='3306', user='root', password='secret', databases=[], **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.databases = databases
        self.name = 'MariaDB-%s@%s %s' % (user, host, databases)

    def backup(self):
        results = dict()
        for db in self.databases:
            logging.info('Starting backup database \'%s\'...' % db)
            cmd = 'mysqldump -h %s -P %s -u%s -p%s %s' % (self.host, self.port, self.user, self.password, db)
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = p.communicate()
            if stderr:
                raise RuntimeError('Error occurred when backup %s: %s' % (db, stderr))
            else:
                results.update({'%s.sql' % db: stdout})
                logging.info('Finshed backing up database \'%s\'' % db)
        return results

    def restore(self):
        logging.info('Do nothing')
