#!/usr/bin/env/ python

import os
import glob
import shutil

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
        self.model     = 'frac'
        self.final     = final.Final('lightquark')
        pass
    
    def run(self,path):
        print "--generator: working on '%s'" % path
        args           = os.path.normpath(path).split('/')
        self.path      = path
        self.energy    = energy.Energy(args[0])
        self.element   = element.Element(args[1])
        self.process   = process.Process(args[2])
        self.generator = args[3]
        self.model     = args[4]
        self.final     = final.Final(args[5])
        if self.options.regenerate:
            shutil.rmtree(os.path.join(path,'mc_generation'))
            shutil.rmtree(os.path.join(path,'events'))
            pass
        mkdir(os.path.join(path,'mc_generation'))
        mkdir(os.path.join(path,'mc_generation',self.next_runfolder()))
        mkdir(os.path.join(path,'events'))
        # generate runcard
        self.run_card()
        # perfom MC genaration
        self.generate()
        # convert hepmc -> corsika
        self.convert()
        # apply nucleus model
        self.enrich()
        pass

    def next_runfolder(self):
        try:
            count=0
            while count in [ int(item.split("_")[-1]) for item in glob.glob(os.path.join(self.path,'mc_generation','run_*'))]:
                count+=1
                pass
            self.run_folder = "run_%i" % count
            return self.run_folder
        except ValueError as err:
            print [ item.split("_")[-1] for item in glob.glob(os.path.join(self.path,'mc_generation','run_*'))]
            print err
            raise err
        pass

    def target_energy(self):
        return self.energy.value/self.element.nucleons

    def run_card(self):
        if self.generator == "h7":
            self.run_card = h7.Card( self.target_energy(), self.process.process, self.final.h7(), os.path.join(self.path,'mc_generation') )
            self.run_card.produce()
            pass
        else:
            raise NotImplemented("unknown generator '%s'" % self.generator)
        pass

    def next_seed(self):
        # use the given random seed
        if self.options.regenerate or not os.path.exists(os.path.join(self.path,'mc_generation','seeds.dat')):
            with open(os.path.join(self.path,'mc_generation','seeds.dat'),'w') as fout:
                fout.write("%i\n" % self.options.seed)
                pass
            return self.options.seed
        # generate a new random seed 
        else:
            count=1
            with open(os.path.join(self.path,'mc_generation','seeds.dat'),'r') as fin:
                while count in map(int, fin.readlines() ):
                    count+=1
                    pass
                pass
            with open(os.path.join(self.path,'mc_generation','seeds.dat'),'a') as fout:
                fout.write("%i\n" % count)
                pass
            return count
        pass

    def generate(self):
        if self.generator == 'h7':
            from  hepstore.docker import herwig as herwig
            #build
            print "--generator: herwig build"
            herwig.run([ '--directory', os.path.join(self.path,'mc_generation'),
                         'build'    , '%s.in'  % self.run_card.name, ])
            #integrate
            print "--generator: herwig integrate"
            herwig.run([ '--directory', os.path.join(self.path,'mc_generation'),
                         'integrate', '%s.run' % self.run_card.name, ])
            #run
            copy( os.path.abspath( os.path.join(self.path,'mc_generation','Herwig-scratch') ),
                  os.path.abspath( os.path.join(self.path,'mc_generation',self.run_folder,'Herwig-scratch') )
            )
            copy( os.path.abspath( os.path.join(self.path,'mc_generation','%s.run' % self.run_card.name) ),
                  os.path.abspath( os.path.join(self.path,'mc_generation',self.run_folder,'%s.run' % self.run_card.name) )
            )
            print "--generator: herwig run"
            herwig.run([ '--directory', os.path.join(self.path,'mc_generation',self.run_folder),
                         'run'      , '%s.run' % self.run_card.name, '-N', '%i' % self.options.nevents, '-s', '%i' % self.next_seed() ])
            pass
        else:
            raise NotImplemented("unknown generator '%s'" % self.generator)
        pass

    def convert(self):
        from hepstore.docker import hepmc2corsika as converter
        converter.run([ '--directory', os.path.join(self.path,'mc_generation',self.run_folder), '-f', '%s.hepmc' % self.run_card.name, '-o', 'event' ])
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
            ##print  os.path.join( self.path, 'events', "%s-%i" % ( "-".join(os.path.basename(fname).split("-")[:-1]),count) )
            return os.path.join( self.path, 'events', "%s-%i" % ( "-".join(os.path.basename(fname).split("-")[:-1]),count) )
        pass

    def enrich(self):
        print "--generator: apply nucleon interaction model"
        for fname in glob.glob(os.path.join(self.path,'mc_generation',self.run_folder,'event-*')):
            model.enrich( fname, self.next_name(fname),
                           energy=self.energy, element=self.element, model=self.model)
            pass
        pass
    
    pass
