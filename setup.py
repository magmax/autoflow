# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

VERSION = (0, 0, 0, 0)
VERSION_STR = '.'.join(str(x) for x in VERSION)

DESCRIPTION = 'Discover the app flow'

def read_file(filename):
    if os.path.exists(filename):
        with open(filename) as fd:
            return fd.read()
    return DESCRIPTION


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test"),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest  # NOQA
        errno = pytest.main(self.pytest_args or ['server'])
        sys.exit(errno)


setup(
    name='autoflow',
    version=VERSION_STR,
    description=DESCRIPTION,
    long_description=read_file('README.rst'),
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Programming Language :: Python :: 3.5',
        'Environment :: Web Environment',
        'Topic :: System :: Monitoring',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords=('status', 'discover'),
    author='Miguel Ángel García',
    author_email='miguelangel.garcia@gmail.com',
    url='',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=[
        'factory_boy   >= 2.5.2',
        'fake-factory  >= 0.5.3',
        'pytest        >= 2.6.1',
        'pytest-django >= 2.6.2',
        'pytest-cov    >= 1.8.1',

        'coverage      >= 4.0.2',

        'flake8        == 2.2.3',
    ],
    install_requires=[
        'Django                  >= 1.9.5',
        'pytz                    >= 2016.4',
    ],
    extras_require={
        'redis':      ['redis    >= 2.10.3'],
        'postgresql': ['psycopg2 >= 2.5.4'],
    },
    scripts=['bin/autoflow.py'],
)
