#!/usr/bin/env python

import os
import argparse


class StatisticParser(argparse.ArgumentParser):

    def __init__( self,
                  description = "perform statistical analysis" ):
        argparse.ArgumentParser.__init__( self, description )

        # put arguments here
        self.add_argument("-f", "--fit",
                          action = "store_true",
                          help   = "fit distribution from numric pdf's",
        )
        self.add_argument( "--data",
                           default = [],
                           help    = "data to be used",
                           nargs   = '+',
        )
        self.add_argument( "--pdf",
                           default = [],
                           help    = "list of pdf's used for fitting",
                           nargs   = '+',
        )
        self.add_argument( "--bins",
                           default = 100,
                           type    = int,
                           help    = "numeric granularity for histograms",
        )
        self.add_argument( "--axis",
                           default = [ 0, 1, 2,],
                           type    = int,
                           help    = "specify axis for projections",
                           nargs   = '+',
        )
        self.add_argument( "--start",
                           default = 1.0,
                           type    = float,
                           help    = "init value for fit",
        )
        self.add_argument( "--limit",
                           action  = "store_true",
                           help    = "compute upper bound on xsec_s",
        )
        self.add_argument( "--roc",
                           default = os.path.join(os.getcwd(),'roc.npy'),
                           help    = "path to roc data",
        )
        self.add_argument( "--xsec_s",
                           default = 1.0,
                           type    = float,
                           help    = "signal cross section",
        )
        self.add_argument( "--xsec_b",
                           default = 1.0,
                           type    = float,
                           help    = "background cross section",
        )
        self.add_argument( "--luminosity",
                           default = 1.0,
                           type    = float,
                           help    = "set luminosity",
        )
        self.add_argument( "--significance",
                           default = "",
                           help    = "compute significance from classifier output, save at 'ARG'/significance.npy",
        )
        self.add_argument( "--cls_s",
                           default = os.path.join(os.getcwd(),'cls_s.npy'),
                           help    = "classifier output distribution for signal",
        )
        self.add_argument( "--cls_b",
                           default = os.path.join(os.getcwd(),'cls_b.npy'),
                           help    = "classifier output distribution for background",
        )
        
        pass
    
pass
