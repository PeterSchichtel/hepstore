#!/usr/bin/env python

import os
import parser
import framework
import sys
from hepstore.errors import *

############################################################################
## run the app
############################################################################
def main(args=None):

    # create arg parser for school
    arg_parser = parser.EasParser()

    # parse args
    parsed_args, unknown = arg_parser.parse_known_args(args)

    # don't allow unknown args
    if unknown != []:
        raise ParserError( "unknown arguments %s" % " ,".join(unknown) )

    # produce/analyse cosmic ray air showers
    app = framework.Steerer(parsed_args)
    try:
        app.run()
        pass
    except Exception as exc:
        raise exc
    
    pass # main
############################################################################

############################################################################
## make executable script
############################################################################
if __name__ == "__main__":
    main()
    pass
############################################################################


sys.exit()
#!/usr/bin/env python

import os

import steering
import analysis

############################################################################
## run the app
############################################################################
def run():

    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to run the EAS analysis frame work out of the box with python 2.7.")

    # setup arg parser    
    parser = argparse.ArgumentParser(description='main steering program for corsika shower and analysis handler')

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

    # if we want to generate events

    # if we want to shower
    if args.shower:
        steerer.begin()
        steerer.shower()
        pass

    # if we want to extract observables
    if args.analyse:
        steerer.run(analysis.analysis)
        pass #analysis

    # back to cdir
    os.chdir(cdir)
        
    pass # run
############################################################################
