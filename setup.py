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
    # pckages shipped with hepstore
    packages=[
        'hepstore',
        'hepstore.core',
        'hepstroe.core.statistics',
        'hepstore.core.school',
        'hepstore.core.school.books',
        'hepstore.framework',
        'hepstore.framework.monte_carlo',
        'hepstore.framework.anaylis',
        'hepstore.framework.anaylis.eas',
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
            'hepstore-school         = hepstore.core.school:main',
            'hepstore-plot           = hepstore.core.plotter:main',
            'hepstore-herwig         = hepstore.framework.monte_carlo.herwig:main',
            'hepstore-sherpa         = hepstore.framework.monte_carlo.sherpa:main',
            'hepstore-corsika        = hepstore.frameworl.monte_carlo.corsika:run',
            'hepstore-hepmc2corsika  = hepstore.fromework.monte_carlo.hepmc2corsika:run',
            'hepstore-eas            = hepstore.framework.analysis.eas:main',
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
