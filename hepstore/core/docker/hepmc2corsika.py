#!/usr/bin/env python

# global imports
import os

# local imports
import parser

############################################################################
## run the app
############################################################################
def main(args=None):

    # we need to setup the arg parser
    arg_parser = parser.DockerParser()
    arg_parser.set_defaults(
        docker_repository    = "peterschichtel",
        docker_image         = "hepmc2corsika",
        docker_image_version = "0.1",
    )
    # files to be converted
    arg_parser.add_argument( "-f", "--file",
                             default = [],
                             nargs   = '+',
                             help    = "list of files to be converted (must be .hepmc)"
    )
    # prefix to be used for corsika file format
    arg_parser.add_argument( "-o", "--output",
                             type    = str,
                             default = "event",
                             help    = "output file name (will be appended by event num)"
    )
    
    # parse args
    parsed_args, unknown = arg_parser.parse_known_args(args)
            
    # run the app
    from interface import DockerIF as Hepmc2Corsika
    app = Hepmc2Corsika(
        image     = os.path.join( parsed_args.docker_repository,
                                  parsed_args.docker_image ),
        version   = parsed_args.docker_image_version,
        verbose   = parsed_args.docker_verbose
    )
    for fname in parsed_args.file:
        app.run(
            directory = parsed_args.docker_directory,
            args      = [ '/bin/bash',
                          '-c',
                          'source $ACTIVATE && hepmc2corsika %s %s' % (fname,parsed_args.output) 
            ]
        )
        pass
        
    pass # run
############################################################################

