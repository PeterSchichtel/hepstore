#!/usr/bin/env python

import os,sys
import glob
import subprocess
import errno
import shutil
from hepstore.tools import *
import subprocess
import shutil

pid_dict={"photon":1,"proton":14,"neutron":15,"helium":402,"lithium":703,"carbon":1206,"neon":2010,"iron":5626}

class runcard:
    def __init__(self,path):
        self.name     = "runcard-0.dat"
        self.out      = "std-0.out"
        self.err      = "std-0.err"
        self.path     = os.path.join(path,"showers")
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
    def isStackin(self):
        return "stackin" in self.corsika
    def create(self):
        mkdir(self.path)
        with open(os.path.join(self.path,self.name),'w') as fout:
            fout.write("RUNNR     %i                           run number                         \n" % self.seed)
            fout.write("EVTNR     1                            number of first shower event       \n")
            fout.write("NSHOW     %i                           number of showers to generate      \n" % 1 )
            fout.write("THETAP    0.  0.                       range of zenith angle (degree)     \n")
            fout.write("PHIP      -360.  360.                  range of azimuth angle (degree)    \n")
            fout.write("PRMPAR    %i                           particle type of prim. particle     \n" % self.pid)
            if not self.isStackin():
                fout.write("* ESLOPE  -2.7                         slope of primary energy spectrum  \n")
                fout.write("ERANGE  %9.2e  %9.2e                   energy range of primary particle    \n" % (self.estart,self.estop) )
                pass
            else:
                fout.write("INFILE    %s                                                              \n" % os.path.relpath(self.filename,self.path) )
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

class corsikashower:
    def __init__(self,num,options):
        self.num     = num
        self.options = options
        pass
    def begin(self,card,nevents,files):
        self.card    = card
        self.nevents = nevents
        self.files   = files
        pass
    def filename(self,n):
        try:
            return self.files[n]
        except IndexError:
            return None
        pass
    def one_shower(self):
        ## corsika only works from within the folder
        cdir=os.getcwd()
        os.chdir(self.card.path)
        command=['corsika','--generator-version',self.options.corsika,'-f',self.card.name,'-v']
        with open(self.card.out,'w') as fout:
            with open(self.card.err,'w') as ferr:
                subprocess.call(command, stdout=fout, stderr=ferr)
                ferr.close()
                pass
            fout.close()
            pass
        os.chdir(cdir)
        pass
    def run(self):
        print "--shower[%i]: working on %s" % (self.num,self.card.path)
        ## create folder and runcard
        oldnevents=len(glob.glob(os.path.join(self.card.path,"DAT00*")))/2
        print "--shower[%i]: already generated %i events" % (self.num,oldnevents)
        for n in range(oldnevents,self.nevents):
            if n%50==0:
                print "--shower[%i]: at event %i " % (self.num,n)
                pass
            ## setup runcard
            self.card.filename = self.filename(n)
            self.card.set_seed(n)
            self.card.create()
            ## run shower
            self.one_shower()
            pass #for
        pass
    def convert(self):
        ## corsika only works from within the folder
        cdir=os.getcwd()
        if not os.path.isdir(self.card.path):
            return
        os.chdir(self.card.path)
        command = ['corsika','-v','--generator-version',self.options.corsika,'-c']
        for item in glob.glob("DAT*"):
            if not "long" in item.lower():
                if not os.path.exists("particle_file_%i" % int(item[3:])):
                    command.append(item)
                    pass
                pass
            pass
        with open(self.card.out,'w') as fout:
            with open(self.card.err,'w') as ferr:
                subprocess.call(command, stdout=fout, stderr=ferr)
                ferr.close()
                pass
            fout.close()
            pass
        os.chdir(cdir)
        pass
    pass #shower
