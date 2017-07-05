#!/usr/bin/env python

# module: hepstore.docker.sherpa

# imports for this module
import os

############################################################################
## run the app
############################################################################
def main(args=None):

    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(
        description =
        "This App allows to run the Sherpa code out of the box with python 2.7." )
    # specify arguments for versioning
    parser.add_argument( "--repository"       ,
                         type    = str,
                         default = "sherpamc",
                         help    = "docker repo of the genrator" )
    parser.add_argument( "--generator"        ,
                         type    = str,
                         default = "sherpa",
                         help    = "which generator to run, default Sherpa " )
    parser.add_argument( "--generator-version",
                         type    = str,
                         default = "2.2.2",
                         help    = "which version to run, default 2.2.2" )
    
    # mount a directory
    parser.add_argument( "--directory",
                         type    = str,
                         default = os.getcwd(),
                         help    =
                         "mount this directoy as /UserDirectory (automatic working dir!), default is PWD!" )

    # verbose stdout
    parser.add_argument( "-v", "--verbose",
                         action  = "store_true",
                         help    = "print container stdout" )
    
    # parse args
    parsed_args, unknown = parser.parse_known_args(args)
            
    # run the app
    from interface import DockerIF as Sherpa
    app=Sherpa(
        image     = os.path.join( parsed_args.repository.lower(),
                                parsed_args.generator.lower() ),
        version   = parsed_args.generator_version,
        verbose   = parsed_args.verbose
    )
    app.run(
        directory = parsed_args.directory,
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

