#!/usr/bin/env python

import argparse
import json
import os
import logging
import sys
import signal

from datetime import datetime
from git import Repo
from subprocess import Popen, PIPE
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


GIT_REPO_DIR = '/backup/git_repo'
SHOUBLE_STOPED = False

def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


def parse_ops(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', dest='cfg_file',
                        help='config file')
    parser.add_argument('--host', dest='host', default='mariadb',
                        help='hostname or IP address to connect to database; default mariadb')
    parser.add_argument('--port', dest='port', default='3306',
                        help='port to use to connect to database; default 3306')
    parser.add_argument('-u', '--user', dest='user', default='root',
                        help='username for the database; default root')
    parser.add_argument('-p', '--password', dest='password',
                        help='password for the database')
    parser.add_argument('--databases', dest='databases',
                        help='names of databases to dump, can be specify multiple database seperate by comma')
    # git options
    parser.add_argument('--git-repo', dest='git_repo',
                        help='URL of git repository including access token in URL e.g. https://oauth2:<access_token>@gitlab.com/username/private-project')
    return parser.parse_args(args)


def sigterm_handler(signum, frame):
    global SHOUBLE_STOPED
    if signal.SIGTERM == signum:
        SHOUBLE_STOPED = True


def dump_databases(host, port, user, password, databases):
    logger = logging.getLogger()
    output_files = list()
    databases = databases.split(',')
    for db in databases:
        logger.info('Starting backup database \'%s\'...' % db)
        file_name = '%s.sql' % db
        output = os.path.join(GIT_REPO_DIR, '%s' % file_name)
        cmd = 'mysqldump -h %s -P %s -u%s -p%s %s > %s' % (host, port, user, password, db, output)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        if stderr:
            logger.error('Error occurred when backup %s: %s' % (db, stderr))
        else:
            output_files.append(file_name)
            logger.info('Finshed backing up database \'%s\'' % db)
    return output_files


def backup(git_url, host, port, user, password, databases):
    logger = logging.getLogger()
    if not os.path.exists(GIT_REPO_DIR):
        logger.info('Git repo does not exist')
        logger.info('Cloning git repo for the first run...')
        repo = Repo.clone_from(git_url, GIT_REPO_DIR)
        logger.info('Cloning is finshed')
    else:
        logger.info('Pulling changes from remote...')
        repo = Repo(GIT_REPO_DIR)
        repo.git.pull('origin', 'master')
        logger.info('Pulling is finshed')
    output_files = dump_databases(host, port, user, password, databases)
    repo.index.add(output_files)
    time_stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('Committing and pushing change to git repo...')
    repo.index.commit('automatically backup at %s UTC' % time_stamp)
    repo.git.push('origin', 'master')
    logger.info('Pushing backup files has been finshed')


def main(args):
    global SHOUBLE_STOPED
    opts = parse_ops(args)
    init_logger()
    logger = logging.getLogger()
    scheduler = BackgroundScheduler()
    backup_args = (opts.git_repo, opts.host, opts.port, opts.user, opts.password, opts.databases)
    scheduler.add_job(func=backup, args=backup_args, trigger='cron', second='30')
    scheduler.start()
    while not SHOUBLE_STOPED:
        pass
    scheduler.shutdown()
    logger.info("Bye bye! See you soon.")


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sigterm_handler)
    sys.exit(main(sys.argv[1:]))
