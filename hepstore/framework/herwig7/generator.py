#!/usr/bin/env python

# global imports
import os
import subprocess
import StringIO

# hepstore imports
from hepstore.core.utility import *
from hepstore.core.physics.model.nucleon_interaction import fragment
from hepstore.core.physics.process import Process
from hepstore.core.physics.particle import *
from hepstore.core.physics.momentum import *
from hepstore.core.docker import hepmc2corsika

# import runcard
import runcard


# h7 generator
class Generator(object):

    def __init__( self, options ):
        self.options    = options
        self.path       = os.getcwd()
        self.name       = 'herwig'
        self.process    = Process()
        self.primary    = Particle()
        self.eventfiles = None
        self.hepmc_dir  = None
        pass
    
    def card( self ):
        fpath = os.path.join( self.path, self.name )
        with open( os.path.join("%s.in" % fpath), 'w' ) as fcard:
            runcard.collider( fcard )
            runcard.beams(    fcard, energy1   = self.process.initial[0].momentum.energy, energy2 = self.process.initial[1].momentum.energy )
            runcard.model(    fcard )
            runcard.process(  fcard, process   = self.process )
            runcard.cuts(     fcard, process   = self.process )
            runcard.provider( fcard )
            runcard.scale(    fcard )
            runcard.shower(   fcard )
            runcard.pdf(      fcard )
            runcard.hepmc(    fcard )
            runcard.save(     fcard, name      = self.name )
            pass #with
        pass

    def run( self ):
        # make sure full path is available
        self.path = os.path.abspath( self.path )
        # start herwig run
        print "--h7[%i]: working on '%s'" % (os.getpid(),self.path)
        # create directory
        mkdir( self.path )
        # create runcard
        print "--h7[%i]: runcard" % os.getpid()
        self.card()
        # build
        print "--h7[%i]: build" % os.getpid()
        args = [ 'hepstore-herwig',
                 '--docker_verbose',
                 '--docker_directory', self.path,
                 'build', '%s.in'  % self.name ]
        subprocess( args, onscreen=False, fname=os.path.join(self.path,'build-std') )
        # integrate
        print "--h7[%i]: integrate" % os.getpid()
        args = [  'hepstore-herwig',
                  '--docker_verbose',
                  '--docker_directory', self.path,
                  'integrate', '%s.run' % self.name, ]
        subprocess( args, onscreen=False, fname=os.path.join(self.path,'integrate-std') )
        # find a clean generation folder
        self.next()
        mkdir( os.path.join( self.path, self.folder))
        os.link( os.path.abspath( os.path.join(self.path,'Herwig-scratch') ),
                 os.path.abspath( os.path.join(self.path,self.folder,'Herwig-scratch') )
        )
        os.link( os.path.abspath( os.path.join(self.path,'%s.run' % self.name) ),
                 os.path.abspath( os.path.join(self.path,self.folder,'%s.run' % self.name) )
        )
        # run
        print "--h7[%i]: run" % os.getpid()
        args = [  'hepstore-herwig',
                  '--docker_verbose',
                  '--docker_directory', os.path.join(self.path,self.folder),
                  'run'      , '%s.run' % self.name, '-N', '%i' % self.options.nevents, '-s', '%i' % self.seed ]
        subprocess( args, onscreen=False, fname=os.path.join(self.path,self.folder,'run-std') )
        # return the path to the hepmc file
        self.hepmc_dir = os.path.join( self.path, self.folder )
        pass

    def next(self):
        # use the given random seed
        if self.options.regenerate or not os.path.exists(os.path.join(self.path,'seeds.dat')):
            with open(os.path.join(self.path,'seeds.dat'),'w') as fout:
                fout.write("%i\n" % self.options.seed)
                pass
            self.seed = self.options.seed
        # generate a new random seed 
        else:
            count=1
            with open(os.path.join(self.path,'seeds.dat'),'r') as fin:
                while count in map(int, fin.readlines() ):
                    count+=1
                    pass
                pass
            with open(os.path.join(self.path,'seeds.dat'),'a') as fout:
                fout.write("%i\n" % count)
                pass
            self.seed = count
            pass
        # find a clean folder to run
        count=0
        while count in [ int(item.split("_")[-1]) for item in glob.glob(os.path.join(self.path,'run_*'))]:
            count+=1
            pass
        self.folder = "run_%i" % count
        pass

    

    
    
    pass
            
