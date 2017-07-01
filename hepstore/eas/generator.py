#!/usr/bin/env/ python

import os
import glob
import shutil

from hepstore.tools import *
import importlib

class Generator(object):
    
    def __init__(self,options):
        self.options        = options
        self.path           = os.getcwd()
        pass
    
    def run(self,path):
        if self.options.regenerate:
            shutil.rmtree(os.path.join(path,'mc_generation'))
            shutil.rmtree(os.path.join(path,'events'))
            pass
        mkdir(os.path.join(path,'mc_generation'))
        mkdir(os.path.join(path,'events'))
        # generate events in hepmc format
        self.path           = path
        lib                 = importlib.import_module(os.path.normpath(path).split('/')[3])
        app                 = lib.Generator(self.options)
        self.hepmc_filepath = app.run(os.path.join(path,'mc_generation')
        # convert events
        self.convert()
        # enrich with nucleons
        self.enrich()
        pass

    def convert(self):
        print "--generator: convert to corsika format"
        from hepstore.docker import hepmc2corsika as converter
        converter.run([ '--directory', os.path.dirname(self.hepmc_filepath), '-f', '%s' % os.path.basename(self.hepmc_filepath), '-o', 'event' ])
        pass

    def enrich(self):
        print "--generator: apply nucleon interaction model"
        for fname in glob.glob(os.path.join(os.path.dirname(self.hepmc_file),'event-*')):
            model.enrich( fname, self.next_name(fname),
                           energy=self.energy, element=self.element, model=self.model)
            pass
        pass

    def next_name(self,fname):
        name = fname.split("-")[:-1]
        num  = int(fname.split("-")[-1])
        if self.options.regenerate:
            return os.path.join(self.path,'events',os.path.basename(fname))
        else:
            list_of_nums = [ int(item.split("-")[-1]) for item in glob.glob(os.path.join(self.path,'events','event-*')) ]
            count = 1
            while count in list_of_nums:
                count+=1
                pass
            return os.path.join( self.path, 'events', "%s-%i" % ( "-".join(os.path.basename(fname).split("-")[:-1]),count) )
        pass
    
    pass
