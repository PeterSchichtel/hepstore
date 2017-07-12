#!/usr/bin/env python
######################################################################################
# module   : hepstore.core.docker_interface
# author(s): Peter Schichtel
# year     : 2017
# version  : 0.1
######################################################################################


######################################################################################
# global imports
######################################################################################
import docker
import os
######################################################################################

######################################################################################
# the actual interface class
######################################################################################
class DockerIF(object):

    # constructor
    def __init__( self,
                  image   = 'GENERATOR',
                  version = 'TAG',
                  verbose = False ):
        # save arguments
        self.IMAGE   = image
        self.TAG     = version
        self.name    = '%s:%s' % (self.IMAGE,self.TAG)
        self.verbose = verbose
        # connect to docker
        self.client  = docker.from_env()
        # check if docker image exist otherwise try to pull
        if not len( self.client.images.list( name = self.IMAGE ) )>0:
            print '--%s: pull image' % self.name
            self.client.images.pull( self.IMAGE, tag = self.TAG )
            pass
        pass

    # actual command run interface
    def run( self, args,
             directory = None,
             verbose   = False):
        # construct docker container name
        containername = '%s:%s' % (self.IMAGE, self.TAG )
        # see if there is a directory to be mounted from host machine
        try:
            folder    = os.path.realpath(directory)
            volume    = {folder: {'bind': '/UserVolume', 'mode': 'rw'}}
            pass
        except Exception:
            volume    = {}
            pass
        # run the command on the container
        container = self.client.containers.run( containername,
                                                command     = args,
                                                volumes     = volume,
                                                working_dir = '/UserVolume',
                                                detach      = True )
        # print the container output on screen
        for i,line in enumerate(
                container.logs( stdout=True, stderr=True, stream=True) ):
            if self.verbose:
                print '%i: %s' % (i,line.strip())
                pass
            pass
        # remove container
        container.remove()
        pass

    pass # DockerIF
######################################################################################

######################################################################################
# an actual app
######################################################################################
def main(args=None):

    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(
        description =
        "This App allows to run code on any Docker image out of the box with python 2.7." )
    
    # specify arguments for versioning
    parser.add_argument( "--docker_repository",
                         type    = str,
                         default = "peterschichtel",
                         help    = "docker repo of the genrator" )
    
    parser.add_argument( "--docker_image",
                         type    = str,
                         default = "herwig",
                         help    = "which generator to run, default Herwig " )
    
    parser.add_argument( "--docker_image_version",
                         type    = str,
                         default = "7.0.4",
                         help    = "which version to run, default 7.0.4" )
    
    # mount a directory
    parser.add_argument( "--docker_directory",
                         type    = str,
                         default = os.getcwd(),
                         help    =
                         "mount this directoy as /UserDirectory (automatic working dir!), default is PWD!" )

    # verbose stdout
    parser.add_argument( "--docker_verbose",
                         action  = "store_true",
                         help    = "print container stdout" )
    
    # parse args
    parsed_args, unknown = parser.parse_known_args(args)
            
    # generate the app
    app = DockerIF(
        image     = os.path.join( parsed_args.docker_repository,
                                  parsed_args.docker_image ),
        version   = parsed_args.docker_image_version,
        verbose   = parsed_args.docker_verbose
    )

    # run the app
    app.run(
        directory = parsed_args.directory,
        args      = [ '/bin/bash',
                      '-c',
                      '%s' % " ".join( unknown )
        ]
    )

    pass # main
######################################################################################

######################################################################################
# allow as executable file
######################################################################################
if __name__ == "__main__":
    main()
    pass
######################################################################################


