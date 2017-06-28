#!/usr/bin/env python

import os
from argparse import ArgumentParser

class SchoolParser(ArgumentParser):

    def __init__(self,description="This school allows to learn from data in .npy format."):
        ArgumentParser.__init__(self,description=description)
        ## add all the args here -> inherit them elsewhere
        # setup arg parser    
        self.add_argument("-f", "--file", default=[],
                            help="list of data files to be learned from (.npy format)",
                            required=True, nargs='+',
                            type=str)
        self.add_argument("-l", "--label", default=["1*1.0","1*0.0"],
                            help="cycle to be used for data labels in classification, understands multiplication",
                            required=True, nargs='+',
                            type=str)
        # main options
        self.add_argument(      "--random_state",      default=0,           type=int,    help="random state for machine learning")
        self.add_argument(      "--test_size",         default=0.25,        type=float,  help="realtive size of test sample")
        self.add_argument("-c", "--classifier",        default="svc",       type=str,    help="machine learning algorithm")
        self.add_argument("-p", "--path",              default=os.getcwd(), type=str,    help="where to save results")
        self.add_argument(      "--points",            default=2000,        type=int,    help="number of support points for probability map creation")
        self.add_argument(      "--zoom",              default=0.15,        type=float,  help="zoom values for probability map creation")
        self.add_argument("-e", "--explore",           action='store_true',              help="explore the classifier before training it")
        self.add_argument(      "--only_explore",      action='store_true',              help="explore the classifier without training it")
        self.add_argument(      "--signal_labels",     default=["1.0"],     type=str,    help="specify labels used as signal in ROC curve")
        self.add_argument(      "--background_labels", default=["0.0"],     type=str,    help="specify labels used as background in ROC curve")
        self.add_argument(      "--log_transform",     action='store_true',              help="use Log() on input data")
        self.add_argument("-j", "--jobs",              default=1,           type=int,    help="number of cores to be used")
        self.add_argument(      "--solver",            default='svd')
        self.add_argument(      "--shrinkage",         default=None)
        self.add_argument(      "--store_covariance",  action='store_true')
        self.add_argument(      "--tol",               default=0.0001)
        self.add_argument(      "--reg_param",         default=0.0)
        self.add_argument(      "--c_parameter",       default=1.0)
        self.add_argument(      "--kernel",            default='rbf', type=str)
        self.add_argument(      "--degree",            default=3)
        self.add_argument(      "--gamma",             default='auto')
        self.add_argument(      "--coef0",             default=0.0)
        self.add_argument(      "--shrinking",         action='store_false')
        self.add_argument(      "--probability",       action='store_true')
        self.add_argument(      "--cache_size",        default=200.)
        self.add_argument(      "--verbose",           action='store_true')
        self.add_argument(      "--max_iter",          default=-1)
        pass
        
    pass

    
