#!/usr/bin/env/ python

import os

from hepstore.tools import *
import energy,element,process,final,model
import h7

class Generator(object):
    
    def __init__(self,options):
        self.options   = options
        self.path      = os.getcwd()
        self.energy    = energy.Energy(1.0e+06)
        self.element   = element.Element('proton')
        self.process   = process.Process('qcd')
        self.generator = 'h7'
        self.final     = final.Final('lightquark')
        self.model     = model.Model('frac')
        pass
    
    def run(self,path):
        args           = os.path.normpath(path).split('/')
        self.path      = path
        self.energy    = energy.Energy(args[0])
        self.element   = element.Element(args[1])
        self.process   = process.Process(args[2])
        self.generator = args[3]
        self.final     = final.Final(args[4])
        self.model     = model.Model(args[5])
        # generate runcard
        mkdir(os.path.join(path,'mc_generation'))
        self.run_card()
        # perfom MC genaration
        self.generate()
        # convert hepmc -> corsika
        self.convert()
        # do we need to boost(?)
        self.boost()
        # apply nucleus model
        mkdir(os.path.join(path,'events'))
        self.enriche()
        pass

    def target_energy(self):
        return self.energy.value/self.element.nucleons

    def run_card(self):
        if self.generator == "h7":
            self.run_card = h7.Card( centre_of_mass(self.target_energy()), self.process.process, self.final.h7(), self.path )
            self.run_card.produce()
            pass
        else:
            raise NotImplemented("unknown generator '%s'" % self.generator)
        pass

    def generate(self):
        if self.generator == 'h7':
            import hepstore.docker.herwig as herwig
            #build
            herwig.run([ '--directory', self.path, 'build', '%s.in' % self.run_card.name ])
            #integrate
            herwig.run([ '--directory', self.path, 'integrate', '%s.run' % self.run_card.name ])
            #run
            herwig.run([ '--directory', self.path, 'run', '%s.run' % self.run_card.name ])
            pass
        else:
            raise NotImplemented("unknown generator '%s'" % self.generator)
        pass

    def convert(self):
        pass

    def boost(self):
        pass

    def enriche(self):
        pass
    
    pass
