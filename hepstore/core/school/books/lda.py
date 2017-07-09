#!/usr/bin/env python

# from general
import sklearn.discriminant_analysis
import numpy as np
import time
import os

# from hepstore
from hepstore.tools import *
from hepstore.statistics.distributions import Log10Flat as Log10Flat

# from local
import tuning

# out own LDA interface
class LinearDiscriminantAnalysis(sklearn.discriminant_analysis.LinearDiscriminantAnalysis):

    # constructor
    def __init__(self,
                 solver='svd', shrinkage=None, priors=None, n_components=None,
                 store_covariance=False, tol=0.0001, path=os.getcwd(),
                 random_state=None, jobs=1 ):
        if solver=='svd' and shrinkage is not None:
            print "--LDA: warning setting 'shrinkage' to 'None', for SVD"
            shrinkage=None
            pass
        sklearn.discriminant_analysis.LinearDiscriminantAnalysis.__init__(
            self,solver=solver, shrinkage=shrinkage, priors=priors,
            n_components=n_components, store_covariance=store_covariance, tol=tol
        )
        self.path         = path
        self.random_state = random_state
        self.jobs         = jobs
        pass

    # explore parameters of this algorithm
    def explore( self, X, y ):
        # generate unique path dependent on core algorithm
        path = os.path.join(self.path,self.solver)
        print "--LDA: explore"
        # specify parameters for exploration
        if self.solver == 'svd':
            param_dist = {
                'tol'      : Log10Flat(-10,-0.001)
            }
            pass
        else:
            param_dist = {
                'shrinkage': Log10Flat(-10,-0.001),
            }
            pass
        # tune classifier
        tuning.tune( self, X, y, param_dist,
                     path         = path,
                     jobs         = self.jobs,
                     random_state = self.random_state
        )
        pass
    
    pass

