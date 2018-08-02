#!/usr/bin/env python

import argparse
import json
import os
import logging
import sys

from datetime import datetime
from git import Repo
from subprocess import Popen, PIPE


GIT_REPO_DIR = '/backup/git_repo'

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


def dump_databases(opts):
    logger = logging.getLogger()
    output_files = list()
    databases = opts.databases.split(',')
    for db in databases:
        logger.info('Starting backup database \'%s\'...' % db)
        file_name = '%s.sql' % db
        output = os.path.join(GIT_REPO_DIR, '%s' % file_name)
        cmd = 'mysqldump -h %s -P %s -u%s -p%s %s > %s' % (opts.host, opts.port, opts.user, opts.password, db, output)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        if stderr:
            logger.error('Error occurred when backup %s: %s' % (db, stderr))
        else:
            output_files.append(file_name)
            logger.info('Finshed backing up database \'%s\'' % db)
    return output_files


def backup(opts):
    logger = logging.getLogger()
    if not os.path.exists(GIT_REPO_DIR):
        logger.info('Git repo does not exist')
        logger.info('Cloning git repo for the first run...')
        repo = Repo.clone_from(opts.git_repo, GIT_REPO_DIR)
        logger.info('Cloning is finshed')
    else:
        logger.info('Pulling changes from remote...')
        repo = Repo(GIT_REPO_DIR)
        repo.git.pull('origin', 'master')
        logger.info('Pulling is finshed')
    output_files = dump_databases(opts)
    repo.index.add(output_files)
    time_stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('Committing and pushing change to git repo...')
    repo.index.commit('automatically backup at %s UTC' % time_stamp)
    repo.git.push('origin', 'master')
    logger.info('Pushing backup files has been finshed')


def main(args):
    opts = parse_ops(args)
    init_logger()
    logger = logging.getLogger()
    backup(opts)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
