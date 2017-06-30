#!/usr/bin/env python

import os,sys
import glob
import subprocess
import errno
import shutil
from hepstore.tools import *
import subprocess
import shutil
import random

pid_dict={"photon":1,"proton":14,"neutron":15,"helium":402,"lithium":703,"carbon":1206,"neon":2010,"iron":5626}

class Runcard(object):

    def __init__(self,path):
        self.name     = "runcard-0.dat"
        self.out      = "std-0.out"
        self.err      = "std-0.err"
        self.path     = path
        self.corsika  = "7.4_stackin"
        self.pid      = 1
        self.filename = None
        self.estart   = 1.0e+06
        self.estop    = 1.0e+06
        pass

    def set_element(self,element):
        self.pid=pid_dict[element]
        pass

    def set_seed(self,n):
        self.name = "runcard-%i.dat" % n
        self.out  = "std-%i.out"     % n
        self.err  = "std-%i.err"     % n
        self.seed = n
        pass

    def is_stackin(self):
        return "stackin" in self.corsika

    def create(self):
        mkdir(self.path)
        with open(os.path.join(self.path,self.name),'w') as fout:
            fout.write("RUNNR     %i                           run number                         \n" % self.seed)
            fout.write("EVTNR     %i                            number of first shower event      \n" % 1 )
            fout.write("NSHOW     %i                           number of showers to generate      \n" % 1 )
            fout.write("THETAP    0.  0.                       range of zenith angle (degree)     \n")
            fout.write("PHIP      -360.  360.                  range of azimuth angle (degree)    \n")
            if not self.is_stackin():
                fout.write("PRMPAR    %i                           particle type of prim. particle     \n" % self.pid)
                fout.write("* ESLOPE  -2.7                         slope of primary energy spectrum  \n")
                fout.write("ERANGE  %9.2e  %9.2e                   energy range of primary particle    \n" % (self.estart,self.estop) )
                pass
            else:
                fout.write("INFILE    %s                                                              \n" % self.filename )
                pass
            fout.write("FIXHEI   18300.E2      0                                                  \n")
            fout.write("* FIXCHI  0.                           starting altitude (g/cm**2) (* shouldnt be active with FIXHEI *) \n")
            fout.write("SEED    1%i   0   0                    seed for 1. random number sequence \n" % self.seed)
            fout.write("SEED    2%i   0   0                    seed for 2. random number sequence \n" % self.seed)
            fout.write("SEED    3%i   0   0                                                       \n" % self.seed)
            fout.write("OBSLEV  100.E2                         observation level (in cm) \n")
            fout.write("OBSLEV  1300.E2                        observation level (in cm) \n")
            fout.write("OBSLEV  1400.E2                        observation level (in cm) \n")
            fout.write("OBSLEV  1500.E2                        observation level (in cm) \n")
            fout.write("OBSLEV  1600.E2                        observation level (in cm) \n")
            fout.write("OBSLEV  5000.E2                        observation level (in cm) \n")
            fout.write("OBSLEV  7500.E2                        observation level (in cm) \n")
            fout.write("OBSLEV  10000.E2                       observation level (in cm) \n")
            fout.write("OBSLEV  12500.E2                       observation level (in cm) \n")
            fout.write("OBSLEV  15000.E2                       observation level (in cm) \n")
            fout.write("MAGNET  20.53   43.67                  magnetic field centr. Europe          \n")
            fout.write("HADFLG  0  0  0  0  0  2               flags hadr.interact.&fragmentation    \n")
            fout.write("ECUTS   0.3  0.2  0.003  0.003         energy cuts for particles             \n")
            fout.write("THIN    1.E-4 1.E30 0.E0               thinning of particle output file      \n")
            fout.write("*CASCADE T T T                                                               \n")
            fout.write("MUADDI  T                              additional info for muons             \n")
            fout.write("MUMULT  T                              muon multiple scattering angle        \n")
            fout.write("ELMFLG  T   T                          em. interaction flags (NKG,EGS)       \n")
            fout.write("STEPFC  1.0                            mult. scattering step length fact.    \n")
            fout.write("RADNKG  200.E2                         outer radius for NKG lat.dens.distr.  \n")
            fout.write("ARRANG  0.                             rotation of array to north            \n")
            fout.write("LONGI   T   10.  F  T                  longit.distr. & step size & fit & out \n")
            fout.write("ECTMAP  1.2345E9                       cut on gamma factor for printout      \n")
            fout.write("MAXPRT  1                              max. number of printed events         \n")
            fout.write("DIRECT  ' '                            output directory                      \n")
            fout.close()
            pass
        pass # create
    
    pass #runcards

class Shower(object):
    
    def __init__(self,options):
        self.options = options
        pass
    
    def shower(self):
        from hepstore.docker import corsika 
        args=[ '-d', '%s' % self.card.path, '--generator-version', self.options.corsika, '-f', self.card.name ]
        corsika.run(args)
        pass

    def next_seed(self):
        count=0
        while os.path.exists( os.path.join(self.card.path,"DAT%06i" % count) ):
            count+=1
            pass
        return count

    def next_file(self):
        return os.path.basename( self.files.pop( random.randrange(len(self.files)) ) )
    
    def run(self,path):
        print "--shower[%i]: working on %s" % ( os.getpid(), path )
        # split input 
        energy,element,process,generator,final,model = os.path.normpath(path).split('/')
        # setup the runcard
        self.card         = Runcard(os.path.join(path,'showers'))
        self.card.corsika = self.options.corsika
        self.card.set_element(element)
        self.card.estart  = float(energy)
        self.card.estop   = float(energy)+float(self.options.erange)
        # if stackin -> collect files 
        if self.card.is_stackin():
            for f in glob.glob(os.path.join(path,'events','event-*')):
                try:
                    os.link( f, os.path.join(path,'showers',os.path.basename(f)) )
                    pass
                except OSError:
                    pass
                pass
            self.files = glob.glob( os.path.join(path,'showers','event-*') )
            pass
        # run nevents showers
        for n in range(0,self.options.nevents):
            if n%50 == 0:
                print "--shower[%i]: showered %i out of %i events" % (os.getpid(),n,self.options.nevents)
                pass
            if self.card.is_stackin():
                self.card.filename = self.next_file()
                pass
            self.card.set_seed(self.next_seed())
            self.card.create()
            self.shower()
            pass
        # convert output
        self.convert()
        pass
    
    def convert(self):
        print "--shower[%i]: converting data formats" % os.getpid()
        from hepstore.docker import corsika 
        args = [
            '-d', '%s' % self.card.path, '--generator-version', self.options.corsika, '-c'
        ] + [
            os.path.basename(d) for d in glob.glob(os.path.join(self.card.path,'DAT*')) if not 'long' in d.lower()
        ]
        corsika.run(args)
        pass
    
    pass #shower
