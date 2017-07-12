import os
import shutil
import sys
############################################################################
## run the app
############################################################################
def run(argv=None):

    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to run the Corsika code (and corsikaread) out of the box with python 2.7.")
    
    # specify version to run
    parser.add_argument("--repository"       , type=str, default="peterschichtel"  ,help="docker repo of the genrator")
    parser.add_argument("--generator"        , type=str, default="Corsika"         ,help="which generator to run, default Herwig ")
    parser.add_argument("--generator-version", type=str, default="7.4"             ,help="which version to run, default 7.0.4")
    
    # mount a directory
    parser.add_argument("-d", "--directory"  , type=str, default=os.getcwd()       ,help="mount this directoy as /UserDirectory (automatic working dir!), default is PWD!")

    # specify a runcard
    parser.add_argument("-f", "--file"       , type=str, default=[], nargs='+'     ,help="specify list of runcards")

    # convert to human readable
    parser.add_argument("-c", "--convert"    , type=str, default=[], nargs='+'     ,help="list of files to be converted from binary")

    # verbose stdout
    parser.add_argument("-v", "--verbose", action="store_true", help="print container stdout" )
    
    # parse args
    args, unknown = parser.parse_known_args(argv)
            
    # start app
    from interface import DockerIF as Corsika
    app=Corsika(
        image=os.path.join(args.repository.lower(),args.generator.lower()),
        version=args.generator_version,
        verbose=args.verbose
    )

    # run shower
    for runcard in args.file:
        app.run(
            directory=args.directory,
            args=[ '/bin/bash',
                   '-c',
                   'corsikaLinker $(pwd) && corsika < %s ' % runcard,
            ],
        )
        pass #for runcard

    # convert files
    for n,datfile in enumerate(args.convert):
        # prepare input       
        with open(os.path.join(args.directory,"convert.in"),'w') as fout:
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
        shutil.move( os.path.join(args.directory,"fort.8"), os.path.join(args.directory,"particle_file_%i" % n) )
        pass #for datfile
    
    pass # run
############################################################################
