#!/usr/bin/env python

import os
import machine_learning
from hepstore.core.errors import *
import sys

import parser
import ship

############################################################################
## run the app
############################################################################
def main(args=None):

    # load parser
    arg_parser = parser.StatisticParser()

    # parse args
    parsed_args, unknown = arg_parser.parse_known_args(args)

    # do not allow unknown args
    if unknown != []:
        raise  ParserError("unknown args in statistic '%s'" % " ".join(unknown))

    # excute args
    app = ship.Captain(parsed_args)
    app.run()
    
    pass # main
############################################################################

############################################################################
## executable as script
############################################################################
if __name__ == '__main__':
    main()
    pass
############################################################################
