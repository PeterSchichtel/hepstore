#!/usr/bin/env python

# module: hepstore.core.docker.sherpa

# global imports
import os

# local imports
import parser
import interface

############################################################################
## run the app
############################################################################
def main(args=None):

    # we need to setup the arg parser
    arg_parser = parser.DockerParser()
    arg_parser.set_defaults(
        docker_repository    = "sherpamc",
        docker_image         = "sherpa",
        docker_image_version = "2.2.2",
    )
    
    # parse args
    parsed_args, unknown = parser.parse_known_args(args)
            
    # run the app
    from interface import DockerIF as Sherpa
    app = Sherpa(
        image     = os.path.join( parsed_args.docker_repository,
                                  parsed_args.docker_image ),
        version   = parsed_args.docker_image_version,
        verbose   = parsed_args.docker_verbose
    )
    app.run(
        directory = parsed_args.docker_directory,
        args      = [ '/bin/bash',
                      '-c',
                      '%s' % " ".join(['Sherpa'] + unknown )
        ]
    )
        
    pass # main
############################################################################

############################################################################
if __name__ == "__main__":
    main()
    pass
############################################################################

