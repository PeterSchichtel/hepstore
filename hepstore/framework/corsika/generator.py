#!/usr/bin/env python

# global imports
import os
from itertools import cycle
import glob

# hepstore imports
from hepstore.core.utility import *
from hepstore.core.physics.process import Process
from hepstore.core.physics.particle import *
from hepstore.core.physics.momentum import *

# import runcard
import runcard

# corsika generator
class Generator(object):

    def __init__( self, options ):
        self.options    = options
        self.path       = os.getcwd()
        self.name       = 'corsika'
        self.primary    = Particle()
        self.process    = Process()
        self.eventfiles = None
        pass
    
    def card( self ):
        self.fpath = os.path.join( self.path, 'runcard_%i.dat' % self.seed )
        with open( self.fpath , 'w' ) as fcard:
            runcard.run(               fcard, number=self.seed )
            if self.eventfile == None:
                runcard.primary(       fcard, pid=self.primary.corsika, e_start=self.primary.energy, e_stop=(self.primary.energy+float(self.options.erange)), )
                self.version  = '7.4'
                pass
            else:
                runcard.primary(       fcard, stackin=os.path.basename(self.eventfile) )
                self.version  = '7.4_stackin'
                pass
            runcard.geometry(          fcard, )
            runcard.seed(              fcard, seed_1=10*self.seed+1, seed_2=10*self.seed+2, seed_3=10*self.seed+3 )
            runcard.observation_level( fcard, )
            runcard.switches(          fcard, )
            pass #with
        pass

    def run( self ):
        # make sure full path is available
        self.path = os.path.abspath( self.path )
        # collect event files
        self.eventfiles = cycle(self.eventfiles)
        # start corsika shower
        print "--corsika[%i]: working on '%s'" % (os.getpid(),self.path)
        # create directory
        mkdir( self.path )
        for i in range(0,self.options.nevents):
            # prepare next run
            self.next()
            # create runcard
            self.card()
            # run
            args = [ 'hepstore-corsika',
                     '--docker_verbose',
                     '--docker_image_version', self.version,
                     '--docker_directory', self.path,
                     '-f', os.path.basename(self.fpath), ]
            subprocess( args, onscreen=False, fname=os.path.join(self.path,'corsika-std-%i' % self.seed) )
            pass
        # collect dat files
        datfiles = [ os.path.basename(f) for f in glob.glob( os.path.join( self.path, 'DAT*' ) ) if '.long' not in os.path.basename(f) ]
        # filter if particle file exists
        datfiles = [ f for f in datfiles if not os.path.exists( os.path.join( self.path, 'particle_file_%i' % int(f.split('T')[1]) ) ) ]
        if datfiles != []:
            print "--corsika[%i]: convert" % os.getpid()
            args = [ 'hepstore-corsika',
                     '--docker_verbose',
                     '--docker_directory', self.path,
                     '-c', ] + datfiles
            subprocess( args, onscreen=False,  fname=os.path.join(self.path,'convert-std-%i' % self.seed) )
            pass
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
                lines = [ l.strip() for l in fin.readlines() ]
                while count in map(int, lines ):
                    count+=1
                    pass
                pass
            with open(os.path.join(self.path,'seeds.dat'),'a') as fout:
                fout.write("%i\n" % count)
                pass
            self.seed = count
            pass
        try:
            self.eventfile = next(self.eventfiles)
            os.link( os.path.abspath( self.eventfile ), os.path.abspath( os.path.join( self.path, os.path.basename( self.eventfile ) ) ) )
            pass
        except StopIteration:
            self.eventfile = None
            pass
        except OSError:
            pass
        except Exception as exc:
            print exc
            raise exc
        pass
    
    pass
            
