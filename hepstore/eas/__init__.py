#!/usr/bin/env python

import os

import steering

############################################################################
## run the app
############################################################################
def run():

    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to run the EAS analysis frame work out of the box with python 2.7.")

    # setup arg parser    
    parser = argparse.ArgumentParser(description='main steering program for corsika shower and analysis handler')
    parser.add_argument("-d", "--directory",   default=os.getcwd()     , type=str, help="top level starting point")
    parser.add_argument("-E", "--energy",      default=[]              , help="energies to be considered",     nargs='+')
    parser.add_argument(      "--erange",      default=0.0             , help="specify a energy range for production")
    parser.add_argument("-e", "--element",     default=[]              , help="elemens to be considered",      nargs='+')
    parser.add_argument("-p", "--process",     default=[]              , help="processes to be considered",    nargs='+')
    parser.add_argument("-g", "--generator",   default=[]              , help="genrators to be considered",    nargs='+')
    parser.add_argument("-m", "--model",       default=[]              , help="models to be considered",       nargs='+')
    parser.add_argument("-f", "--final",       default=[]              , help="final states to be considered", nargs='+')
    parser.add_argument("-S", "--shower",      action="store_true"     , help="start showers in allowed folders") 
    parser.add_argument("-L", "--list",        action="store_true"     , help="list statistics")
    parser.add_argument("-A", "--analyse",     action="store_true"     , help="start analysis in all allowed folders")
    parser.add_argument("-C", "--corsika",     default="7.4_stackin"   , type=str    , help="which corsika (sub)version")
    parser.add_argument("-N", "--nevents",     default=1, type=int     , help="number of events to be considered")
    parser.add_argument("-j", "--job",         default=1, type=int     , help="number of threads")
    parser.add_argument("-P", "--plot",        default=[]              , help="create plots from histograms",  nargs='+')
    parser.add_argument("-F", "--figure",      default="", type=str    , help="where to save figures")
    parser.add_argument(      "--histogram",   action="store_true"     , help="plot a histogram")
    parser.add_argument(      "--fit",         action="store_true"     , help="plot a fit")
    parser.add_argument(      "--interpolate", action="store_true"     , help="interpolate histogram")
    parser.add_argument(      "--contour",     action="store_true"     , help="draw 2d contour plot")
    parser.add_argument(      "--heat",        action="store_true"     , help="draw 2d heat plot")
    parser.add_argument(      "--scatter",     action="store_true"     , help="scatter unbinned data")
    parser.add_argument("-a", "--axis",        default=[0,1], type=int , help="which axis to be considered",  nargs='+')
    parser.add_argument("-l", "--level",       default=[1.], type=float, help="which sigma levels to plot for contour",  nargs='+')
    parser.add_argument("-c", "--color",       default=[]  , type=str  , help="list of colors to be used instead of default",  nargs='+')
    parser.add_argument(      "--line",        default=[]  , type=str  , help="list of line styles to be used instead of default",  nargs='+')
    parser.add_argument(      "--normalised",  action="store_true"     , help="normalise data")

    # parse args   
    args = parser.parse_args()

    # correctly normlaize figure path's
    args.figure = os.path.realpath(args.figure)

    # goto working dir
    cdir=os.getcwd()
    os.chdir(args.directory)

    # prepare folder/steering structure
    steerer=steering.steer(args)

    # if we want to list stats
    if args.list:
        steerer.begin()
        steerer.list()
        pass

    # if we want to shower sth
    if args.shower:
        steerer.begin()
        steerer.shower()
        pass

    # if we want to analyse sth
    if args.analyse:
        steerer.begin()
        steerer.analyse()
        pass #analysis

    # if we want to plot sth
    if args.plot:
        steerer.plot()
        pass

    # back to cdir
    os.chdir(cdir)
        
    pass # run
############################################################################
