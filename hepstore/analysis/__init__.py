#!/usr/bin/env python

import os
import machine_learning
from hepstore.errors import *
import sys
import argparser

############################################################################
## run the app
############################################################################
def main(args=None):

    # we need to setup the arg parser
    arg_parser = argparser.ArgumentParser(description="Meta code to analyse typical hep data in .npy format")
    arg_parser.add_argument("mode", type=str, nargs='+', required=True, help="specify the analyses which should be performed")

    # parse args
    parsed_args, unknown = arg_parser.parse_known_args(args)

    # learn from data
    if "learn" in parsed_args:
        analysis = machine_learning.Analysis(unknown)
        analysis.analyse()
        pass
    
    pass # main
############################################################################

############################################################################
## executable as script
############################################################################
if __name__ == "__main__":
    main()
    pass
############################################################################
