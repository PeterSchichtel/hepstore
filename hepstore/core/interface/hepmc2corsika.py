import os

############################################################################
## run the app
############################################################################
def run(args=None):

    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to run the Herwig code out of the box with python 2.7.")
    
    # specify version to run
    parser.add_argument("--repository"       , type=str, default="peterschichtel"  ,help="docker repo of the genrator")
    parser.add_argument("--generator"        , type=str, default="HepMC2Corsika"   ,help="which generator to run, default Herwig ")
    parser.add_argument("--generator-version", type=str, default="0.1"             ,help="which version to run, default 7.0.4")
    
    # mount a directory
    parser.add_argument("--directory"        , type=str, default=os.getcwd()       ,help="mount this directoy as /UserDirectory (automatic working dir!), default is PWD!")

    # files to be converted
    parser.add_argument("-f", "--file", default=[], nargs='+', help="list of files to be converted (must be .hepmc)")

    # prefix to be used for corsika file format
    parser.add_argument("-o", "--output", type=str, default="event", help="output file name (will be appended by event num)") 
    
    # parse args
    parsed_args, unknown = parser.parse_known_args(args)
            
    # run the app
    from interface import DockerIF as Hepmc2Corsika
    app=Hepmc2Corsika(
        image=os.path.join(parsed_args.repository.lower(),parsed_args.generator.lower()),
        version=parsed_args.generator_version
    )
    for name in parsed_args.file:
        app.run(
            directory=parsed_args.directory,
            args=[ '/bin/bash',
                   '-c',
                   'source $ACTIVATE && hepmc2corsika %s %s' % (name,parsed_args.output) 
            ]
        )
        pass
        
    pass # run
############################################################################

