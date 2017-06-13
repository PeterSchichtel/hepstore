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
from hepstore.eas.shower import *
from hepstore.eas.analysis import *
from hepstore.plot import *
import hepstore.tools

#######################################################################################
# set up dictinories for unambigous plotting
style_dict = {
    "sphaleron":{"color":"red"  ,"offset":-0.3},
    "qcd"      :{"color":"blue" ,"offset": 0.0},
    "zlo"      :{"color":"green","offset": 0.3}
}

marker_dict = {
    "proton" :["o","-"],
    "helium" :[",",":" ],
    "lithium":["+","--" ],
    "carbon" :["v","-."],
    "neon"   :["^",":" ],
    "iron"   :["x","--"]
}

process_dict = {
    "qcd"      :"QCD",
    "sphaleron":"Sphaleron",
    "zlo"      :"Z'"
}

element_dict = {
    "proton" :"P",
    "helium" :"He",
    "lithium":"Li",
    "carbon" :"C",
    "neon"   :"Ne",
    "iron"   :"Fe"
}

final_dict = {
    "lightquark"   :"jets",
    "chargedlepton":"e^{+}e^{-}/\mu^{+}\mu^{-}",
    "generic"      :"SM",
    "top"          :"t\overline{t}",
    "bottom"       :"b\overline{b}",
}
#######################################################################################

def listOfFolders(pathes=["./"],all_constrains=[]):
    fullList = []
    try:
        constrains = all_constrains[0]
        pass
    except IndexError:
        constrains = []
        pass
    try:
        remained_constrains = all_constrains[1:]
        pass
    except IndexError:
        remained_constrains = []
        pass
    # recursive step
    for path in pathes:
        folders=glob.glob(os.path.join(path,"*/"))
        # filter
        i=0
        while len(folders)>i:
            folder = folders[i]
            if (folder.strip('/').split('/')[-1] in ['events','showers','analysis']) or (constrains!=[] and folder.strip('/').split('/')[-1] not in constrains):
                folders.remove(folder)
                pass
            else:
                i+=1
                pass
            pass
        # add non existant constrains as would be folders
        for constrain in constrains:
            if not any(constrain in folder for folder in folders):
                folders.append(os.path.join(path,constrain))
                pass
            pass
        # check for end of recursion
        if folders==[]:
            fullList.append(path)
            pass
        else:
            fullList=(fullList+listOfFolders(folders,remained_constrains))
            pass
        pass
    return fullList



class steer:
    def __init__(self,options):
        print "--info: initialising folder structure, this may take some time"
        self.options = options
        self.path    = None
        self.files   = None
        self.pathes  = {}
        self.element = "proton"
        self.energy  = 1.0e+06
        ## init path arrays
        all_constrains=[
            options.energy,
            options.element,
            options.process,
            options.generator,
            options.model,
            options.final,
        ]
        for path in listOfFolders(["./"],all_constrains):
            self.pathes[path] = [
                glob.glob( os.path.join(os.path.abspath(os.path.join(path,"events")),"event-*") ),
                [path.split("/")[1],path.split("/")[2]]
            ]
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
            self.files   = self.pathes[self.path][0]
            self.energy  = float(self.pathes[self.path][1][0])
            self.element = self.pathes[self.path][1][1]
            if os.path.isdir(self.path):
                return True
            else:
                return self.next()
            pass
        except StopIteration:
            return False
        pass
    def isStackin(self):
        return "stackin" in self.options.corsika
    def shower(self):
        ## start a corsika shower in each available file path
        self.begin()
        ################################
        # this is massive so use multi processing
        # this is our worker
        def worker(num,pipe,options):
            filerror=False
            print "--shower[%i]: start subprocess" % num
            output_p, input_p = pipe
            ## load shower module
            shower=corsikashower(num,options)
            while True:
                try:
                    tfile    = output_p.recv()    # Read from the output pipe and do nothing
                    if tfile=="DONE":
                        print "--shower[%i]: leave subprocess" % num
                        break
                    pass
                except EOFError:
                    break
                if not os.path.isfile(tfile):
                    filerror=True
                    break
                with open(tfile,'r') as fin:
                    msg = fin.readline()
                    fin.close()
                    pass
                field  = msg.split(":")
                path   = field[0].split("=")[1]
                element= field[1].split("=")[1]
                energy = float(field[2].split("=")[1])
                files  = field[3].split("=")[1].split(";")
                print "--shower[%i]: %s %s %i" % (num,path,element,len(files))
                ## generate a run card for this shower
                card=runcard(path)
                card.corsika = options.corsika
                card.set_element(element)
                card.estart  = energy
                card.estop   = energy+options.erange
                ## run shower
                shower.begin(card,options.nevents,files)
                shower.run()
                shower.convert()
                os.remove(tfile)
                pass
            pass #while
            if filerror:
                print "--error[%i]: file not found" % num
                pass
            # close pipes
            output_p.close()
            input_p.close()
        pass
        ###############################
        processes=[]
        # fire up the processes
        for n in range(0,self.options.job):
            output_p, input_p = Pipe()
            p = Process(target=worker, args=(n,(output_p, input_p),self.options))
            p.start()
            processes.append([p, output_p, input_p])
            pass
        #output_p.close()       # We no longer need this part of the Pipe()
        # feed the data into the processes
        count=0
        while self.next():
            msg  = "path=%s:" % self.path
            msg += "element=%s:" % self.element
            msg += "energy=%9.2e:" % self.energy
            ##print msg
            msg += "files="
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
            pass
        for p in processes:
            p[1].close()
            p[2].close()
            p[0].join()
            pass
        pass #shower
    def analyse(self):
        ## start an analysis in each available file path
        self.begin()
        ################################
        # this is massive so use multi processing
        # this is our worker
        def worker(num,pipe,options):
            output_p, input_p = pipe
            input_p.close()    # We are only reading
            analysis=analysis(num=num)
            while True:
                try:
                    path = output_p.recv()    # Read from the output pipe and do nothing
                    if not analysis.begin(path,options):
                        print "--info: skipping  %s" % path
                        continue
                    analysis.run()
                    analysis.save()
                    pass
                except EOFError:
                    break
                pass
            pass
        ##########
        output_p, input_p = Pipe()
        processes=[]
        # fire up the processes
        for n in range(0,self.options.job):
            p = Process(target=worker, args=(n,(output_p, input_p),self.options))
            p.start()
            processes.append(p)
            pass
        output_p.close()       # We no longer need this part of the Pipe()
        # feed the data into the processes
        while self.next():
            input_p.send(self.path)
            pass #while
        # wait for processes to finish
        input_p.close()  
        for p in processes:
            p.join()
            pass
        pass #analyse
    def list(self):
        ## list all folders and the progress within in nice color code
        self.begin()
        print bcolors.UNDERLINE + " %67s ||%54s" % ("  "," ") + bcolors.END
        print bcolors.UNDERLINE + "--list: %-60s || %12s %12s %12s %12s" % ("process-path","hard events","showered","attempted","analysed") + bcolors.END
        while self.next():
            eventfiles  = len(glob.glob(os.path.join(self.path,"events","event-*")))
            showerfiles = len(glob.glob(os.path.join(self.path,"showers","particle*")))
            longfiles   = len(glob.glob(os.path.join(self.path,"showers","*long")))
            analyses    = len(glob.glob(os.path.join(self.path,"analysis","histograms.dat")))
            if eventfiles==0:
                evstr = bcolors.FAIL    + "%12i" % eventfiles + bcolors.END
                pass
            elif eventfiles<self.options.nevents:
                evstr = bcolors.WARNING + "%12i" % eventfiles + bcolors.END
                pass
            else:
                evstr = bcolors.OKGREEN + "%12i" % eventfiles + bcolors.END
                pass
            if showerfiles==0:
                shstr = bcolors.FAIL    + "%12i" % showerfiles + bcolors.END
                pass
            elif showerfiles<self.options.nevents:
                shstr = bcolors.WARNING + "%12i" % showerfiles + bcolors.END
                pass
            else:
                shstr = bcolors.OKGREEN + "%12i" % showerfiles + bcolors.END
                pass
            if longfiles==0:
                lstr = bcolors.FAIL     + "%12i" % longfiles + bcolors.END
                pass
            elif longfiles<self.options.nevents:
                lstr = bcolors.WARNING  + "%12i" % longfiles + bcolors.END
                pass
            else:
                lstr = bcolors.OKGREEN  + "%12i" % longfiles + bcolors.END
                pass
            if analyses==0:
                astr = bcolors.WARNING + "          no" + bcolors.END
                pass
            elif analyses==1:
                astr = bcolors.OKGREEN + "         yes" + bcolors.END
                pass
            else:
                astr = bcolors.FAIL + "%i" % analyses + bcolors.END
                pass 
            print "--list: %-60s || %12s %12s %12s %12s" % (self.path,evstr,shstr,lstr,astr)
            pass #while
        pass #list
    pass #steer
