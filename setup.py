# coding=UTF-8
from setuptools import setup, find_packages
from pip.req import parse_requirements


from firanka import __version__

setup(
    version=__version__,
    packages=find_packages(exclude=['tests.*', 'tests']),
    tests_require=["nose", 'coverage>=4.0,<4.4'],
    install_requires=map(str, parse_requirements('requirements.txt')),
    test_suite='nose.collector',
)
