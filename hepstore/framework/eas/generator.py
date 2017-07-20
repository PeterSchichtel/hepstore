#!/usr/bin/env/ python

# global imports
import os
import glob
import shutil
import importlib

# hepstore imports 
from hepstore.core.utility import *
from hepstore.core.docker import hepmc2corsika
import hepstore.core.physics.model.nucleon_interaction as nucleon_interaction
from hepstore.core.physics.process import Process

# local importts
from particle import *

############################################################################
# add particles to a corsika event file
############################################################################
def add_particles( fname_in, fname_out, particles ):
    total_number  = len(particles)
    total_energy  = sum( [ p.energy for p in particles ] )    
    with open( fname_in, 'r' ) as fin:
        with open( fname_out, 'w' ) as fout:
            line_count = 0
            for i,line in enumerate( fin.readlines() ):
                if i==0:
                    count  = int(   line.split()[0] ) + total_number
                    energy = float( line.split()[0] ) + total_energy
                    fout.write("  %i %f \n" % ( count, energy ) )
                    pass
                else:
                    fout.write(line)
                    pass
                line_count += 1
                pass
            for p in particles:
                fout.write(
                    "%5i%5i  %15.7e %15.7e %15.7e %15.7e \n" % (
                        line_count, p.corsika, p.energy, p.pz, p.px, p.py ) )
                line_count += 1
                pass
            pass
        pass
    pass    
############################################################################

############################################################################
# create physics process
############################################################################
def create_final_state( final = 'dijet' ):
    # create final state
    if final == 'dijet':
        final_state = ( Particle( name = 'jet' ), Particle( name = 'jet' ) )
        pass
    else:
        raise KeyError( "unknown final state '%s' " % final )
    # return process obj
    return final_state
        
############################################################################

############################################################################
# generic mc generator class interfacing
# to dedicated tools as herwig, sherpa, etc
############################################################################
class Generator(object):
    
    def __init__( self, options ):
        self.options        = options
        pass

    def setup_directory( self ):
        # empty if regenerate
        if self.options.regenerate and self.options.generate:
            shutil.rmtree(
                os.path.join( self.path, 'mc_generation' ))
            shutil.rmtree(
                os.path.join( self.path, 'events' ))
            pass
        if self.options.regenerate and self.options.shower:
            shutil.rmtree(
                os.path.join( self.path, 'showers' ))
            pass
        # create like mkdir -p
        mkdir(  os.path.join( self.path, 'mc_generation' ))
        mkdir(  os.path.join( self.path, 'events' ))
        mkdir(  os.path.join( self.path, 'showers' ))
        # check for event files
        self.eventfiles = glob.glob( os.path.join( self.path, 'events', 'event-*' ) )
        pass
                  
    def import_path( self, generator ):
        if   'h7'      == generator:
            return 'hepstore.framework.herwig7.generator'
        elif 'corsika' == generator:
            return 'hepstore.framework.corsika.generator'
        elif 'sherpa' == generator:
            return 'hepstore.framework.sherpa.generator'
        else:
            raise KeyError("unknown generator in import path '%s'" % generator )
        pass

    def hepmc2corsika( self ):
        print "--generator[%i]: convert hepmc to corsika format" % os.getpid()
        hepmcfiles = [ os.path.basename(f) for f in glob.glob( os.path.join(self.hepmc_dir,'*.hepmc') )]
        args = [ 'hepstore-hepmc2corsika',
                 '--docker_verbose',
                 '--docker_directory', self.hepmc_dir,
                 '-f', ] + hepmcfiles + [
                 '-o', 'event' ]
        ###print ' '.join(args)
        subprocess( args, onscreen=False, fname=os.path.join(self.hepmc_dir,'h2c-std') )
        pass
    
    def run( self, path ):
        # extract information
        self.path      = path
        energy,element,process,final,generator,model = os.path.normpath(self.path).split('/')
        # check if we actually want to generate hard events
        if self.options.generate and generator == 'corsika':
            print "--generator[%i]: ignore corsika request for hard events" % os.getpid()
            return None
        if self.options.shower:
            generator = 'corsika'
            pass
        # create primary particle
        self.primary   = Primary( name     = element,
                                  energy   = float(energy) )
        # check if we have to model the nucleonic interaction
        if self.options.generator != 'corsika':
            incoming,self.remainder = nucleon_interaction.remainder( self.primary )
            pass
        else:
            incoming       = self.primary
            self.remainder = None
            pass
        # physics process
        self.process   =  Process( initial = ( incoming, Primary( name = 'proton', energy = 1.0, zsign = -1.0 ) ),
                                   final   = create_final_state( final ) ,
                                   process = process  )
        # setup dirs
        self.setup_directory()
        # build generator object
        module         = importlib.import_module( self.import_path( generator ) )
        app            = module.Generator( self.options )
        # setup the generator
        app.primary    = self.primary
        app.process    = self.process
        app.eventfiles = self.eventfiles
        if self.options.generate:
            app.path   = os.path.join( self.path, 'mc_generation' )
            pass
        elif self.options.shower:
            app.path   = os.path.join( self.path, 'showers' )
            pass
        else:
            raise KeyError ('either generate or shower!')
        # generate events
        app.run()
        # in the case we need to convert to corsika inputs
        if self.options.generate:
            # find event file
            self.hepmc_dir = app.hepmc_dir
            if self.hepmc_dir == None:
                return
            # convert to stackin
            self.hepmc2corsika()
            # enriche nucleons
            for fname in glob.glob( os.path.join(self.hepmc_dir,'event-*') ):
                add_particles( fname, self.next_name(fname), self.remainder )
                pass
            pass
        pass
    
    def next_name( self, fname ):
        name                = fname.split("-")[:-1]
        num                 = int(fname.split("-")[-1])
        if self.options.regenerate:
            return os.path.join( self.path,
                                 'events',
                                 os.path.basename(fname) )
        else:
            list_of_nums    = [
                int(item.split("-")[-1])
                for item in glob.glob(
                        os.path.join( self.path,
                                      'events',
                                      'event-*', ))
            ]
            count           = 1
            while count in list_of_nums:
                count      += 1
                pass
            return os.path.join(
                self.path,
                'events',
                "%s-%i" % ( "-".join(os.path.basename(fname).split("-")[:-1]),
                            count )
            )
        pass
    
    pass
############################################################################
