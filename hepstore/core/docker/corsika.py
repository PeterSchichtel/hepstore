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
# add particles to a corsika event file
############################################################################
def add_particles( filen_in, file_out, particles ):
    total_number  = len(particles)
    total_energy  = sum( [ p.energy for p in particles ] )    
    with open( fname_in, 'r' ) as fin:
        with open( fname_out, 'w' ) as fout:
            line_count = 0
            for i,line in enumerate( fin.readlines() ):
                if i==0:
                    count  = int(   line.split()[0] ) + total_number
                    energy = float( line.split()[0] ) + total_energy
                    fout.write("  %i %f \n" % ( count, energy ) )
                    pass
                else:
                    fout.write(line)
                    pass
                line_count += 1
                pass
            for p in particles:
                line_count += 1
                fout.write(
                    "%5i%5i%15.7e%15.7e%15.7e%15.7e \n" % (
                        line_count, p.pid, p.energy, p.pz, p.px, p.py ) )
                pass
            pass
        pass
    pass    
############################################################################

############################################################################
## run the app
############################################################################
def run(argv=None):

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
    args, unknown = arg_parser.parse_known_args(argv)
            
    # start app
    from interface import DockerIF as Corsika
    app = Corsika(
        image     = os.path.join( parsed_args.docker_repository,
                                  parsed_args.docker_image ),
        version   = parsed_args.docker_image_version,
        verbose   = parsed_args.docker_verbose
    )
    # run shower
    for runcard in args.file:
        app.run(
            directory=args.docker_directory,
            args=[ '/bin/bash',
                   '-c',
                   'corsikaLinker $(pwd) && corsika < %s ' % runcard,
            ],
        )
        pass #for runcard

    # convert files
    for n,datfile in enumerate(args.convert):
        # prepare input       
        with open(os.path.join(args.docker_directory,"convert.in"),'w') as fout:
            # spaces are MANDATORY!
            fout.write("%s                                                                                                                                     " % datfile )
            fout.close()
            pass
        # run app
        app.run(
            directory=args.directory,
            args=[ '/bin/bash',
                   '-c',
                   'corsikaread < convert.in'
            ],
        )
        # save file
        shutil.move( os.path.join(args.docker_directory,"fort.8"), os.path.join(args.docker_directory,"particle_file_%i" % n) )
        pass #for datfile
    
    pass # run
############################################################################
