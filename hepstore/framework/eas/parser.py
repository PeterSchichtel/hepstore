#!/usr/bin/env python

# gloal imports
import os
from argparse import ArgumentParser

# our own arg parser
class EasParser(ArgumentParser):

    # constructor
    def __init__( self,
                  description = "The Eas frame-work allows to produce cosmic ray air showers and extract observables" ):
        # parent constructor
        ArgumentParser.__init__( self,
                                 description = description )
        # setup arg parser    
        self.add_argument( "-d", "--directory",
                           default = os.getcwd()     ,
                           type    = str,
                           help    = "top level starting point" )
        
        self.add_argument( "-E", "--energy",
                           default = []              ,
                           help    = "energies to be considered",
                           nargs   = '+')
        
        self.add_argument( "--erange",
                           default = 0.0             ,
                           help="specify a energy range for production")

        self.add_argument( "-e", "--element",
                           default = []              ,
                           help    = "elemens to be considered",
                           nargs   = '+')

        self.add_argument( "-p", "--process",
                           default = []              ,
                           help    = "processes to be considered",
                           nargs   = '+')

        self.add_argument( "-g", "--generator",
                           default = []              ,
                           help    = "genrators to be considered",
                           nargs   = '+')

        self.add_argument( "-m", "--model",
                           default = []              ,
                           help    = "models to be considered",
                           nargs   = '+')

        self.add_argument( "-f", "--final",
                           default = []              ,
                           help    = "final states to be considered",
                           nargs   = '+')

        self.add_argument( "-G", "--generate",
                           action  = "store_true"     ,
                           help    = "generate hard interactions in allowed folders")

        self.add_argument( "-S", "--shower",
                           action  = "store_true"     ,
                           help    = "start showers in allowed folders") 

        self.add_argument( "-L", "--list",
                           action  = "store_true"     ,
                           help    = "list statistics")

        self.add_argument( "-A", "--analyse",
                           action  = "store_true"     ,
                           help    = "start analysis in all allowed folders")

        self.add_argument( "-C", "--corsika",
                           default = "7.4_stackin"   ,
                           type    = str    ,
                           help    = "which corsika (sub)version")

        self.add_argument( "-N", "--nevents",
                           default = 1,
                           type    = int     ,
                           help    = "number of events to be considered" )

        self.add_argument( "-j", "--job",
                           default = 1,
                           type    = int     ,
                           help    = "number of threads" )

        self.add_argument( "-s", "--seed",
                           default = 1,
                           type    = int     ,
                           help    = "random number seed" )

        self.add_argument( "--regenerate",
                           action  = "store_true"     ,
                           help    = "regenerate existing events (default is append)" )

        self.add_argument( "-a", "--analysis",
                           default = [],
                           type    = str    ,
                           help    = "list of user analyses to be loaded dynamically",
                           nargs   = '+' )                   
        pass

    pass
