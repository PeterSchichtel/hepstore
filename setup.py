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
      
      packages=['hepstore',
                'hepstore.errors',
                'hepstore.docker',
                'hepstore.analysis',
                'hepstore.multiprocess',
                'hepstore.eas',
                'hepstore.school',
                'hepstore.tools',
                'hepstore.plot'],
      
      install_requires=[
          'docker',
          'docker-pycreds',
          'sklearn',
      ],
      
      entry_points = {
          'console_scripts': [
              'hepstore                = hepstore:main',
              'hepstore-herwig         = hepstore.docker.herwig:main',
              'hepstore-sherpa         = hepstore.docker.sherpa:main',
              'hepstore-corsika        = hepstore.docker.corsika:run',
              'hepstore-hepmc2corsika  = hepstore.docker.hepmc2corsika:run',
              'hepstore-analysis       = hepstore.analysis:main',
              'hepstore-eas            = hepstore.eas:main',
              'hepstore-school         = hepstore.school:main',
              'hepstore-plot           = hepstore.plot:run',
          ]
      },
      
      keywords = ['hepstore'],
      include_package_data=True,
      zip_safe=False,
)
