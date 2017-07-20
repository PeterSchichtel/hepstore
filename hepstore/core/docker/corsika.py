#!/usr/bin/env python

# module: hepstore.core.docker.sherpa

# global imports
import os
import sys
import shutil

# hepstore imports
from hepstore.core.physics.particle import *

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
        docker_image         = "corsika",
        docker_image_version = "7.4",
    )

    # specify a runcard
    arg_parser.add_argument("-f", "--file"       , type=str, default=[], nargs='+'     ,help="specify list of runcards")

    # convert to human readable
    arg_parser.add_argument("-c", "--convert"    , type=str, default=[], nargs='+'     ,help="list of files to be converted from binary")
    
    # parse args
    parsed_args, unknown = arg_parser.parse_known_args(args)
            
    # start app
    from interface import DockerIF as Corsika
    app = Corsika(
        image     = os.path.join( parsed_args.docker_repository,
                                  parsed_args.docker_image ),
        version   = parsed_args.docker_image_version,
        verbose   = parsed_args.docker_verbose
    )
    # run shower
    for runcard in parsed_args.file:
        app.run(
            directory = parsed_args.docker_directory,
            args      = [ '/bin/bash',
                          '-c',
                          'corsikaLinker $(pwd) && corsika < %s ' % runcard,
            ],
        )
        pass #for runcard

    # convert files
    for datfile in parsed_args.convert:
        # prepare input       
        with open(os.path.join(parsed_args.docker_directory,"convert.in"),'w') as fout:
            # spaces are MANDATORY!
            fout.write("%s                                                                                                                                     " % datfile )
            fout.close()
            pass
        # run app
        app.run(
            directory = parsed_args.docker_directory,
            args      = [ '/bin/bash',
                          '-c',
                          'corsikaread < convert.in'
            ],
        )
        # save file
        num = int(datfile.split('T')[1])
        try:
            shutil.move( os.path.join(parsed_args.docker_directory,"fort.8"), os.path.join(parsed_args.docker_directory,"particle_file_%i" % num) )
            pass
        except IOError as err:
            print err
            pass
        pass #for datfile
    
    pass # run
############################################################################
