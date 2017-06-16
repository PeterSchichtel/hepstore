#!/usr/bin/env python

import numpy as np
import glob
import os

from hepstore.tools import *
from hepstore.eas.event import *

class useranalysis:
    def __init__(self):
        self.levels = 10
        self.data   = {}
        self.data["x_max"] = data("x_max")
        self.data["x_rho"] = data("x_rho")
        for i in range(0,self.levels):
            self.data["rho_weighted_%i" % i     ] = data("rho_weighted_%i" % i      ) 
            self.data["rho_unweighted_%i" %i    ] = data("rho_unweighted_%i" % i    ) 
            self.data["radius_weighted_%i" % i  ] = data("radius_weighted_%i" % i   ) 
            self.data["radius_unweighted_%i" % i] = data("radius_unweighted_%i" % i ) 
            pass
        pass
    def begin(self):
        for d in self.data.values():
            d.clear()
            pass
        pass
    def analyse(self,ev):
        ## create analysis objects
        muons     = [ev.find("muon",i) for i in range(0,self.levels)]
        antimuons = [ev.find("antimuon",i) for i in range(0,self.levels)]
        ## fill histograms with atmospheric levels
        x_max  = ev.xmax
        rho_0  = 0.0
        for i in range(0,self.levels):
            rho_weighted   = 0.0
            rho_unweighted = 0.0
            for p in (muons[i]+antimuons[i]):
                weight = p.weight
                radius  = p.radius()/100.0
                if radius>=500.0 and radius<=600.0:
                    rho_weighted  += weight
                    rho_unweighted+= 1.0
                    pass
                self.data["radius_weighted_%i"   % i].append([radius,weight])
                self.data["radius_unweighted_%i" % i].append(radius)
                pass
            self.data["rho_weighted_%i"   % i].append(rho_weighted  )
            self.data["rho_unweighted_%i" % i].append(rho_unweighted)
            if i==0:
                rho_0 = rho_unweighted
                pass
            pass
        self.data["x_max"].append(x_max)
        self.data["x_rho"].append([x_max,rho_0])
        pass
    def finalize(self):
        pass
    def save(self,path):
        for d in self.data.values():
            d.save( os.path.join(path,d.name) )
            pass
        pass
    pass

class analysis:
    def __init__(self,options=None,analyses=[]):
        self.options  = options
        self.analysis = [useranalysis()]
        for anlysis in analyses:
            #self.analysis = [useranalysis()]
            pass
        pass
    def save(self):
        path = os.path.join(os.path.dirname(self.path),"analysis")
        mkdir(path)
        for analysis in self.analysis:
            analysis.save(path) 
            pass
        pass
    def validate(self,path):
        if os.path.isdir(os.path.join(path,"showers")):
            self.path=os.path.join(path,"showers")
            pass
        else:
            return False
        for analysis in self.analysis:
            analysis.begin()
            pass
        return True
    def run(self):
        print "--info: analysing %s " % self.path
        # loop through events
        eventcounter=1
        for pfile,xfile in zip(glob.glob(os.path.join(self.path,"particle_file*")),glob.glob(os.path.join(self.path,"DAT*.long"))):
            if eventcounter%100==0:
                print "--analysis[%i]: at event %i" % (os.getpid(),eventcounter)
                pass
            # create event
            ev=event()
            ev.particles_from_file(pfile)
            ev.xmax_from_file(xfile)
            # analyse event
            for analysis in self.analysis:
                analysis.analyse(ev)
                pass
            if eventcounter>=self.options.nevents:
                break
            eventcounter+=1
            pass
        print "--analysis[%i]: analysed %i events" % (os.getpid(),eventcounter)
        pass
    def finalize(self):
        for analysis in self.analysis:
            analysis.finalize()
            pass
        self.save()
        pass
    pass
