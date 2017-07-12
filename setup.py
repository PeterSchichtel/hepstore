#!/usr/bin/env python

# setup file for hepstore
from setuptools import setup

# read a README file
def readme():
    with open('README.rst') as f:
        return f.read()
    pass

# actual setup configuration
setup(
    # names, version, mail, etc.
    name             = 'hepstore',
    version          = '0.1',
    description      = 'market place for reproducible high energy phenomenology analyses',
    long_description = readme(),
    url              = 'local',
    author           = 'Peter Schichtel',
    author_email     = 'peterschichtel@icloud.com',
    license          = 'Public',
    # packages shipped with hepstore
    packages=[
        'hepstore',
        'hepstore.core',
        'hepstore.core.interface',
        'hepstore.core.plotter',
        'hepstore.core.school',
        'hepstore.core.school.books',
        'hepstore.core.statistic',
        'hepstore.framework',
        'hepstore.framework.eas',
    ],
    # requirement
    install_requires = [
        'docker',
        'docker-pycreds',
        'sklearn',
    ],
    # command line tools
    entry_points = {
        'console_scripts': [
            'hepstore                = hepstore:main',
            'hepstore-docker         = hepstore.core.interface:main',
            'hepstore-herwig         = hepstore.core.interface.herwig:main',
            'hepstore-sherpa         = hepstore.core.interface.sherpa:main',
            'hepstore-corsika        = hepstore.core.interface.corsika:run',
            'hepstore-hepmc2corsika  = hepstore.core.interface.hepmc2corsika:run',
            'hepstore-plot           = hepstore.core.plotter:main',
            'hepstore-school         = hepstore.core.school:main',
            'hepstore-statistic      = hepstore.core.statistic:main',
            'hepstore-eas            = hepstore.framework.eas:main',
        ]
    },
    # search words
    keywords = [
        'hepstore',
        'reproducibility'
        'phenomenology',
        'particle physics'
        'monte carlo',
        'analysis strategy',
        'machine learning',
    ],
    # zip? not for now
    include_package_data = True,
    zip_safe             = False,
)
