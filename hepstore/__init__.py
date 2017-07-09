#!/usr/bin/env python

import sys
import subprocess

############################################################################
## main
############################################################################
def main(args=None):
    
    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(
        description = "This App allows to run all the hepstore tools with python 2.7. and docker"
    )

    # this is just a meta wrapper for all the different tools
    parser.add_argument( "tool",
                         type    = str,
                         default = None,
                         help    = "must be one of the following (herwig|corsika|sherpa|plotter|school|eas|...)"
    )

    # parse args
    parsed_args, unknown = parser.parse_known_args(args)
    
    # run
    subprocess.check_call(['hepstore-%s' % parsed_args.tool]+unknown)
        
    pass # main
############################################################################

############################################################################
if __name__=="__main__":
    main()
    pass
############################################################################

### a gui might be added here :)
