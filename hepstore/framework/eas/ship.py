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
import time
import collections

# hepstore imports
from hepstore.tools import *
from hepstore.multiprocess.pipes import Multipipeline


## project imports
import generator
import shower
import observables

class Captian:
    
    def __init__(self,options):
        print "--eas: initialising folder structure, this may take some time"
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
        ## go to working directory
        self.current = os.getcwd()
        os.chdir(options.directory)
        for path in list_of_folders(["./"],all_constrains,exclude=['mc_generation','events','showers','observables','analysis']):
            self.pathes[path] = glob.glob( os.path.join(os.path.abspath(os.path.join(path,"events")),"event-*") )
            pass # for path
        pass # init

    def __del__(self):
        os.chdir(self.current)
        pass
    
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
    
    def run(self):
        # if we want to generate events
        if self.options.generate:
            self.begin()
            self.execute(generator.Generator)
            pass
        # if we want to shower
        if self.options.shower:
            self.begin()
            self.execute(shower.Shower)
            pass
        # if we want to extract observables
        if self.options.analyse:
            self.begin()
            self.execute(observables.Extractor)
            pass 
        # if we want to list stats
        if self.options.list:
            self.begin()
            self.list()
            pass
        # go back
        pass
    
    def execute(self,app):
        # create multiprocessing processes
        processes = Multipipeline( app=app, args=self.options, job=self.options.job )
        # feed the data into the processes
        while self.next():
            processes.send(self.path)
            pass #while
        # finalize processes
        processes.close()
        pass

    
    def list(self):
        ## list all folders and the progress within in nice color code
        self.begin()
        print bcolors.UNDERLINE + " %67s ||%54s" % ("  "," ") + bcolors.END
        print bcolors.UNDERLINE + "--list: %-60s || %12s %12s %12s %12s  " % ( "process-path %s" % os.path.join( *os.getcwd().split('/')[-2:] ),
                                                                               "hard events","attempted","showered","observables") + bcolors.END
        while self.next():
            nums = []
            nums.append(len(glob.glob(os.path.join(self.path,"events","event-*"   ))))
            nums.append(len(glob.glob(os.path.join(self.path,"showers","*long"    ))))
            nums.append(len(glob.glob(os.path.join(self.path,"showers","particle*"))))
            nums.append(len(glob.glob(os.path.join(self.path,"observables","*npy"    ))))
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
    
    pass #captian


