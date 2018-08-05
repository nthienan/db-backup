import os
import shutil
import yaml

from datetime import datetime
from setuptools import setup, find_packages, Command
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
name ='db-backup'
version = '0.0.1'

class CleanCommand(Command):
    description = "custom clean command that forcefully removes dist and build directories"
    user_options = []
    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        if path.exists(path.join(here, 'build')):
            shutil.rmtree(path.join(here, 'build'))
        if path.exists(path.join(here, 'dist')):
            shutil.rmtree(path.join(here, 'dist'))
        if path.exists(path.join(here, name.replace('-', '_') + '.egg-info')):
            shutil.rmtree(path.join(here, name.replace('-', '_') + '.egg-info'))


# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    data = f.readlines()
    requires = data


setup(
    name=name,
    version=version,  # Required
    description='DB-Backup',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/practice-devops/tools/mariadb-backup',
    author='An Nguyen',
    author_email='nthienan.it@gmail.com',
    license='MIT',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='db, backup, devops, CI/CD',

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=['db.backup'],
    package_dir={'db.backup': 'src/db_backup'},
    scripts=['src/db_backup.py'],
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=requires,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },

    project_urls={
        'Bug Reports': 'https://gitlab.com/practice-devops/tools/mariadb-backup/issues',
        'Source': 'https://gitlab.com/practice-devops/tools/mariadb-backup',
    },

    cmdclass={
        'clean': CleanCommand
    },

)
