#!/usr/bin/env python

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
