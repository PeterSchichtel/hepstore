#!/usr/bin/env python

# module: hepstore.core.docker.herwig

# global imports
import os

# local imports
import interface
import parser

############################################################################
## run the app
############################################################################
def main(args=None):

    # we need to setup the arg parser
    arg_parser = parser.DockerParser()
    
    # parse args
    parsed_args, unknown = arg_parser.parse_known_args(args)
            
    # run the app
    from interface import DockerIF as Herwig
    app = Herwig(
        image     = os.path.join( parsed_args.docker_repository,
                                  parsed_args.docker_image ),
        version   = parsed_args.docker_image_version,
        verbose   = parsed_args.docker_verbose
    )
    app.run(
        directory = parsed_args.docker_directory,
        args      = [ '/bin/bash',
                      '-c',
                      'source $ACTIVATE && %s ' % " ".join(['Herwig'] + unknown )
        ]
    )
        
    pass # main
############################################################################

############################################################################
if __name__ == "__main__":
    main()
    pass
############################################################################

