#!/usr/bin/env python

import os
import teacher
import parser
import sys
from hepstore.core.errors import *

############################################################################
## run the app
############################################################################
def main(args=None):

    # create arg parser for school
    arg_parser = parser.SchoolParser()

    # parse args
    parsed_args, unknown = arg_parser.parse_known_args(args)

    # don't allow unknown args
    if unknown != []:
        raise ParserError( "unknown arguments %s" % " ,".join(unknown) )

    # learn from data
    app = teacher.Teacher(parsed_args)
    try:
        app.teach()
        app.save()
        pass
    except LabelError as err:
        print err
        pass
    
    pass # main
############################################################################

############################################################################
## make executable script
############################################################################
if __name__ == "__main__":
    main()
    pass
############################################################################

