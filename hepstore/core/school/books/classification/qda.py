#!/usr/bin/env python


import sklearn.neural_network
import sklearn.svm
import sklearn.discriminant_analysis

import numpy as np
import time
import os

from hepstore.core.utility import *
from hepstore.core.statistic.distribution import *

from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import classification_report

import sklearn.model_selection 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import ShuffleSplit
import scipy

import tuning

class QuadraticDiscriminantAnalysis(sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis):

    def __init__(self, priors=None, reg_param=0.0,
                 store_covariances=False, tol=0.0001, path=os.getcwd(),
                 random_state=None, jobs=1 ):
        sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis.__init__(
            self, priors=priors, reg_param=reg_param,
            store_covariances=store_covariances, tol=tol,
        )
        self.path         = path
        self.random_state = random_state
        self.jobs         = jobs
        pass

    def explore( self, X, y ):
        path = self.path
        # specify parameters for exploration
        param_dist = {
            'reg_param': Log10Flat(-10,-0.001),
            'tol'      : Log10Flat(-10,-0.001),
        }
        # tune classifier
        tuning.tune( self, X, y, param_dist,
              path         = path,
              jobs         = self.jobs,
              random_state = self.random_state
        )
        pass
    
    pass

