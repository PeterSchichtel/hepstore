#!/usr/bin/env python

# global imports
import argparse
import os

# our own parser
class DockerParser(argparse.ArgumentParser):

    def __init__( self,
                  description = "This App allows to run code on any Docker image out of the box with python 2.7." ) :
        argparse.ArgumentParser.__init__( self, description = description ) 
        # specify arguments for versioning
        self.add_argument( "--docker_repository",
                           type    = str,
                           default = "peterschichtel",
                           help    = "docker repo of the genrator" )
        self.add_argument( "--docker_image",
                           type    = str,
                           default = "herwig",
                           help    = "which generator to run, default Herwig " )   
        self.add_argument( "--docker_image_version",
                           type    = str,
                           default = "7.0.4",
                           help    = "which version to run, default 7.0.4" ) 
        # mount a directory
        self.add_argument( "--docker_directory",
                           type    = str,
                           default = os.getcwd(),
                           help    =
                           "mount this directoy as /UserDirectory (automatic working dir!), default is PWD!" )
        # verbose stdout
        self.add_argument( "--docker_verbose",
                           action  = "store_true",
                           help    = "print container stdout" )
        pass

    pass

