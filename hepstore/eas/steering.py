#!/usr/bin/env python

#######################################################################################
#
# This file is part of the cosmic ray air shower analysis frame work. It generates the
# folder structure needed for this study and manages the different analysis steps
#
# author(s): Peter Schichtel
#
#######################################################################################

## python imports
import os,sys
import glob
import multiprocessing as mp
import scipy
from multiprocessing import Process, Pipe
import time
import collections

## user imports
import interaction
import shower
import analysis
from ..tools import *
from ..multiprocess import multipipeline

class steer:
    def __init__(self,options):
        print "--info: initialising folder structure, this may take some time"
        self.options   = options
        self.path      = None
        self.files     = None
        self.pathes    = {}
        self.energy    = 1.0e+06
        self.element   = "proton"
        self.process   = "qcd"
        self.generator = "corsika"
        self.final     = "lightquark"
        self.model     = "frac"
        ## init path arrays
        all_constrains=[
            options.energy,
            options.element,
            options.process,
            options.generator,
            options.model,
            options.final,
        ]
        for path in listoffolders(["./"],all_constrains):
            self.pathes[path] = glob.glob( os.path.join(os.path.abspath(os.path.join(path,"events")),"event-*") )
            pass # for path
        pass # init
    def begin(self):
        ## we need an iterator on all these different file pathes
        self.iter_pathes=iter(sorted(self.pathes.keys()))
        pass
    def next(self):
        ## go to the next availbale file path
        try:
            self.path    = self.iter_pathes.next()
            self.files   = self.pathes[self.path]
            try:
                self.energy,self.element,self.process,self.generator,self.final,self.model = os.path.normpath(self.path).split('/')
                pass
            except ValueError:
                return self.next()
            return True
        except StopIteration:
            return False
        pass
    def isStackin(self):
        return "stackin" in self.options.corsika.lower()
    def process(self,app):
        # set itaretors to start
        self.begin()
        # create multiprocessing processes
        processes = multipipeline( app=app, args=self.options, job=self.options.job )
        # feed the data into the processes
        while self.next():
            processes.send(self.path)
            pass #while
        # finalize processes
        processes.close()
        pass #analyse
    def interaction(self):
        pass
    def shower(self):
        ## start a corsika shower in each available file path
        self.begin()
        processes=[]
        # fire up the processes
        for n in range(0,self.options.job):
            output_p, input_p = Pipe()
            p = Process(target=worker.shower, args=(n,(output_p, input_p),self.options))
            p.start()
            processes.append([p, output_p, input_p])
            pass
        #output_p.close()       # We no longer need this part of the Pipe()
        # feed the data into the processes
        count=0
        while self.next():
            msg  = "path=%s:element=%s:energy=%9.2e:files=" % (self.path,self.element,self.energy)
            for f in self.files:
                msg += "%s;" % f
                pass
            with open("tmp-%i.dat" % count,'w') as fout:
                fout.write(msg)
                fout.close()
                pass
            processes[count%self.options.job][2].send("tmp-%i.dat" % count) 
            count+=1
            pass #while
        # wait for processes to finish
        for i,p in enumerate(processes):
            print "--info: send finish to %i" % i
            p[2].send("DONE")
            p[1].close()
            p[2].close()
            p[0].join()
            pass
        pass #shower
    def list(self):
        ## list all folders and the progress within in nice color code
        self.begin()
        print bcolors.UNDERLINE + " %67s ||%54s" % ("  "," ") + bcolors.END
        print bcolors.UNDERLINE + "--list: %-60s || %12s %12s %12s %12s" % ("process-path","hard events","showered","attempted","analysed") + bcolors.END
        while self.next():
            nums = []
            nums.append(len(glob.glob(os.path.join(self.path,"events","event-*"   ))))
            nums.append(len(glob.glob(os.path.join(self.path,"showers","particle*"))))
            nums.append(len(glob.glob(os.path.join(self.path,"showers","*long"    ))))
            nums.append(len(glob.glob(os.path.join(self.path,"analysis","*npy"    ))))
            print_strings =[]
            for num in nums:
                if num==0:
                    pstr = bcolors.FAIL    + "%12i" % num + bcolors.END
                    pass
                elif num<self.options.nevents:
                    pstr = bcolors.WARNING + "%12i" % num + bcolors.END
                    pass
                else:
                    pstr = bcolors.OKGREEN + "%12i" % num + bcolors.END
                    pass
                print_strings.append(pstr)
                pass
            evstr,shstr,lstr,astr = print_strings
            print "--list: %-60s || %12s %12s %12s %12s" % (self.path,evstr,shstr,lstr,astr)
            pass #while
        pass #list
    pass #steer
