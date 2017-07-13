#!/usr/bin/env/ python

# global imports
import os
import glob
import shutil
import importlib

# hepstore imports 
from hepstore.core.tool import *
from hepstore.core.physics import model
from hepstore.core.physics.particle import *
from hepstore.core.physics.momentum import *
from hepstore.core.docker import hepmc2corsika
from hepstore.core.docker import corsika

# local imports
import model

# generic mc generator class interfacing
# to dedicated tools as herwig, sherpa, etc
class Generator(object):
    
    def __init__( self, options ):
        self.options        = options
        self.path           = os.getcwd()
        self.primary        = Primary( pid      = Pid( str(options.element) ),
                                       energy   = float(   options.energy ) ) )
        self.setup_incoming()
        pass

    def setup_incoming( self, proton=True ):
        self.remainder = model.fragment( self.primary )
        for p in self.remainder:
            if   p.pid.name == 'proton' and proton:
                self.incoming = p
                self.remainder.remove(p)
                break
            elif p.pid.name == 'neutron' and not proton:
                self.incoming = p
                self.remainder.remove(p)
                break
            pass
        self.options.incoming = self.incoming
        pass

    def setup_directory( self ):
        if self.options.regenerate:
            shutil.rmtree(
                os.path.join( self.path, 'mc_generation' ))
            shutil.rmtree(
                os.path.join( self.path, 'events' ))
            pass
        mkdir(  os.path.join( self.path, 'mc_generation' ))
        mkdir(  os.path.join( self.path, 'events' ))
        pass
    
    def run( self, path ):
        self.path           = path
        self.setup_directory()
        # generate events in hepmc format
        lib                 = importlib.import_module(
            os.path.normpath(path).split('/')[3] )
        app                 = lib.Generator( self.options )
        self.hepmc_filepath = app.run(
            os.path.join( path, 'mc_generation') )
        # convert events to corsika readable
        self.convert()
        # enrich with ramainder
        self.enrich()
        pass

    def convert( self ):
        print "--generator: convert to corsika format"
        hepmc2corsika.run( [
            '--docker_directory', os.path.dirname( self.hepmc_filepath),
            '-f', '%s' %   os.path.basename( self.hepmc_filepath ),
            '-o', 'event'
        ])
        pass

    def enrich( self ):
        print "--generator: apply nucleon interaction model"
        for fname in glob.glob(
                os.path.join(
                    os.path.dirname( self.hepmc_file), 'event-*' )):
            corsika.add_particles( fname,
                                   self.next_name(fname),
                                   self.remainder()  )
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
