#!/usr/bin/env python

import os
from argparse import ArgumentParser

class EasParser(ArgumentParser):

    def __init__(self,description="The Eas frame-work allows to produce cosmic ray air showers and extract observables"):
        ArgumentParser.__init__(self,description=description)
        ## add all the args here -> inherit them elsewhere
        # setup arg parser    
        parser.add_argument("-d", "--directory",   default=os.getcwd()     , type=str, help="top level starting point")
        parser.add_argument("-E", "--energy",      default=[]              , help="energies to be considered",     nargs='+')
        parser.add_argument(      "--erange",      default=0.0             , help="specify a energy range for production")
        parser.add_argument("-e", "--element",     default=[]              , help="elemens to be considered",      nargs='+')
        parser.add_argument("-p", "--process",     default=[]              , help="processes to be considered",    nargs='+')
        parser.add_argument("-g", "--generator",   default=[]              , help="genrators to be considered",    nargs='+')
        parser.add_argument("-m", "--model",       default=[]              , help="models to be considered",       nargs='+')
        parser.add_argument("-f", "--final",       default=[]              , help="final states to be considered", nargs='+')
        parser.add_argument("-G", "--generate",    action="store_true"     , help="generate hard interactions in allowed folders")
        parser.add_argument("-S", "--shower",      action="store_true"     , help="start showers in allowed folders") 
        parser.add_argument("-L", "--list",        action="store_true"     , help="list statistics")
        parser.add_argument("-A", "--analyse",     action="store_true"     , help="start analysis in all allowed folders")
        parser.add_argument("-C", "--corsika",     default="7.4_stackin"   , type=str    , help="which corsika (sub)version")
        parser.add_argument("-N", "--nevents",     default=1, type=int     , help="number of events to be considered")
        parser.add_argument("-j", "--job",         default=1, type=int     , help="number of threads")
