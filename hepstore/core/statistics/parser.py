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
        
        pass
    
pass
