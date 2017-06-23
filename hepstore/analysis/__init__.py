#!/usr/bin/env python

import os
import machine_learning
from hepstore.errors import *
import sys


############################################################################
## run the app
############################################################################
def main(args=None):

    # we need to setup the arg parser
    arg_parser = machine_learning.MachineLearningParser()

    # parse args
    parsed_args, unknown = arg_parser.parse_known_args(args)

    # don't allow unknown args
    if unknown != []:
        raise ParserError( "unknown arguments %s" % " ,".join(unknown) )

    # learn from data
    app = machine_learning.Analysis(parsed_args)
    try:
        app.analyse()
        pass
    except LabelError as err:
        print err
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
