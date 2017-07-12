#!/usr/bin/env python
######################################################################################
# module   : hepstore.core.docker
# author(s): Peter Schichtel
# year     : 2017
# version  : 0.1
######################################################################################


######################################################################################
# global imports
######################################################################################
import os
######################################################################################

# local imports
import interface
import parser

######################################################################################
# an actual app
######################################################################################
def main(args=None):

    # we need to setup the arg parser
    arg_parser = parser.DockerParser()
    
    # parse args
    parsed_args, unknown = arg_parser.parse_known_args(args)
            
    # generate the app
    app = interface.DockerIF(
        image     = os.path.join( parsed_args.docker_repository,
                                  parsed_args.docker_image ),
        version   = parsed_args.docker_image_version,
        verbose   = parsed_args.docker_verbose
    )

    # run the app
    app.run(
        directory = parsed_args.docker_directory,
        args      = [ '/bin/bash',
                      '-c',
                      '%s' % " ".join( unknown ),
        ]
    )

    pass # main
######################################################################################

######################################################################################
# allow as executable file
######################################################################################
if __name__ == "__main__":
    main()
    pass
######################################################################################


