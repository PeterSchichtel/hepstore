from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
    
setup(name='hepstore',
      version='0.1',
      description='interface to the hep mc generators',
      long_description=readme(),
      url='local',
      author='Peter Schichtel',
      author_email='peterschichtel@icloud.com',
      license='Public',
      packages=['hepstore','hepstore.eas','hepstore.learn'],
      install_requires=[
          'docker',
          'docker-pycreds',
          'sklearn',
      ],
      entry_points = {
          'console_scripts': [
              'hepstore       = hepstore:main',
              'herwig         = hepstore.herwig:run',
              'corsika        = hepstore.corsika:run',
              'hepmc2corsika  = hepstore.hepmc2corsika:run',
              'eas            = hepstore.eas:run',
              'learn          = hepstore.learn:run',
          ]
      },
      keywords = ['hepstore'],
      include_package_data=True,
      zip_safe=False)
