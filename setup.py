# coding=UTF-8
from setuptools import setup, find_packages

from firanka import __version__

setup(
    version=__version__,
    packages=find_packages(exclude=['tests.*', 'tests']),
    tests_require=["nose", 'coverage>=4.0,<4.4'],
    install_requires=['six'],
    test_suite='nose.collector',
)
