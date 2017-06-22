import os

############################################################################
## run the app
############################################################################
def run():

    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to run the Herwig code out of the box with python 2.7.")
    
    # specify version to run
    parser.add_argument("--repository"       , type=str, default="peterschichtel"  ,help="docker repo of the genrator")
    parser.add_argument("--generator"        , type=str, default="Herwig"          ,help="which generator to run, default Herwig ")
    parser.add_argument("--generator-version", type=str, default="7.0.4"           ,help="which version to run, default 7.0.4")
    
    # mount a directory
    parser.add_argument("--directory"        , type=str, default=os.getcwd()       ,help="mount this directoy as /UserDirectory (automatic working dir!), default is PWD!")
    
    # parse args
    args, unknown = parser.parse_known_args()
            
    # run the app
    from hepstore.interface import dockerIF as herwig
    app=herwig(
        image=os.path.join(args.repository.lower(),args.generator.lower()),
        version=args.generator_version
    )
    app.run(
        directory=args.directory,
        args=[ '/bin/bash',
               '-c',
               'source $ACTIVATE && %s ' % " ".join(['Herwig']+unknown)
        ]
    )
        
    pass # run
############################################################################

