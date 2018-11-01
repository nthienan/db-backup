import logging

from abc import ABC, abstractmethod
from datetime import datetime
from subprocess import Popen, PIPE


class AbstractDB(ABC):
    @abstractmethod
    def backup(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def restore(self, *args, **kwargs):
        raise NotImplementedError()


class MariaDB(AbstractDB):
    def __init__(self, host='localhost', port='3306', user='root', password='secret', databases=[], **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.databases = databases
        self.name = 'MariaDB-%s@%s-%s' % (user, host, databases)

    def backup(self, *args, **kwargs):
        results = {'data': dict(), 'timestamp': datetime.utcnow()}
        for db in self.databases:
            logging.info('Starting backup database \'%s\'...' % db)
            cmd = 'mysqldump -h %s -P %s -u%s -p%s %s' % (self.host, self.port, self.user, self.password, db)
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = p.communicate()
            if stderr:
                raise RuntimeError('Error occurred when backup %s: %s' % (db, stderr))
            else:
                results['data'].update({'%s.sql' % db: stdout})
                logging.info('Backup database \'%s\' is done' % db)
        return results

    def restore(self, *args, **kwargs):
        logging.info('Do nothing')

class PostgreSQL(AbstractDB):
    def __init__(self, host='localhost', port='5432', user='postgres', password='secret', databases=[], **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.databases = databases
        self.name = 'PostgreSQL-%s@%s-%s' % (user, host, databases)

    def backup(self, *args, **kwargs):
        results = {'data': dict(), 'timestamp': datetime.utcnow()}
        for db in self.databases:
            logging.info('Starting backup database \'%s\'...' % db)
            cmd = 'pg_dump --dbname=postgresql://%s:%s@%s:%s/%s' % (self.user, self.password, self.host, self.port, db)
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = p.communicate()
            if stderr:
                raise RuntimeError('Error occurred when backup %s: %s' % (db, stderr))
            else:
                results['data'].update({'%s.sql' % db: stdout})
                logging.info('Backup database \'%s\' is done' % db)
        return results

    def restore(self, *args, **kwargs):
        logging.info('Not implement yet')
