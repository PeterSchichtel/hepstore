#!/usr/bin/env python

import numpy as np
import glob
import os

from hepstore.tools import *
from event import *

class Analysis(object):
    
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
        #self.statistic()
        pass

    def save(self,path):
        for d in self.data.values():
            d.save( os.path.join(path,d.name) )
            pass
        pass

    def statistic(self):
        size = 0
        for d in self.data.values():
            size += d.data().nbytes
            pass
        print "--size: %fMB" % (float(size)/1000000.)
        pass

    pass #UserAnalysis

