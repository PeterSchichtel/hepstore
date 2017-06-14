#!/usr/bin/env python

import eas
import learn
import plot
import tools
import interface
import herwig

import os,sys

############################################################################
## main
############################################################################
def main():
    
    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to run all Hep MC Generators out of the box with python 2.7. and docker")

    parser.add_argument("generator", type=str, default=None, help="must be one of the following (herwig|corsika|sherpa|...)")

    # parse args
    args, unknown = parser.parse_known_args()
    
    # run
    import importlib
    sys.argv.remove(args.generator)
    generator = importlib.import_module("hepstore.%s" % args.generator)
    generator.run()
        
    pass # main
############################################################################
### a gui might be added here :)
