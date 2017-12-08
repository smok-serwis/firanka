# coding=UTF-8
from setuptools import setup, find_packages

from sai import __version__

setup(
    version=__version__,
    packages=find_packages(exclude=['tests.*', 'tests']),
    python_requires='==2.7.*',
    tests_require=['nose', 'mock', 'coverage'],
    test_suite='nose.collector',
    zip_safe=False
)
