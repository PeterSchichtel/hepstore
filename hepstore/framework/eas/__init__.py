#!/usr/bin/env python

# global imports
import os
import sys

# hepstore imports
from hepstore.errors import *

# local imports
import parser
import ship

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
    app = ship.Captian(parsed_args)
    app.run()
    
    pass # main
############################################################################

############################################################################
## make executable script
############################################################################
if __name__ == "__main__":
    main()
    pass
############################################################################
