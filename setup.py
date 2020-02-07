from setuptools import setup, find_packages

from firanka import __version__

setup(
    name='firanka',
    version=__version__,
    packages=find_packages(exclude=['tests.*', 'tests', 'docs']),
    install_requires=['sortedcontainers'],
    url='https://github.com/smok-serwis/firanka',
    author=u'Piotr Maślanka',
    author_email=u'pmaslanka@smok.co',
    tests_require=[
        "nose2", "mock", "coverage", "nose2[coverage_plugin]"
    ],
    test_suite='nose2.collector.collector',
    python_requires='!=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',

)
