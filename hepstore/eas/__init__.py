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
    app = framework.Captian(parsed_args)
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
