#!/usr/bin/env python

import numpy as np
import glob
import os

from hepstore.core.utility import *
from event import *

class Extractor(object):
    
    def __init__(self,options=None,analyses=[]):
        self.options  = options
        self.analysis = []
        for name in options.analysis:
            try:
                module = importlib.import_module(name)
                pass
            except ImportError:
                print "--eas: make sure user analysis '%s' is in PYTHONPATH!" % name
                continue
            self.analysis.append(module.Analysis())
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

    def run(self,path):
        if not self.validate(path):
            return False
        print "--analysis[%i]: working on '%s' " % (os.getpid(),self.path)
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
            del ev
            eventcounter+=1
            pass
        print "--analysis[%i]: analysed %i events" % (os.getpid(),eventcounter)
        self.finalize()
        return True

    def finalize(self):
        path = os.path.join(os.path.dirname(self.path),"observables")
        mkdir(path)
        for analysis in self.analysis:
            analysis.finalize()
            analysis.save(path)
            pass
        pass
    
    pass
