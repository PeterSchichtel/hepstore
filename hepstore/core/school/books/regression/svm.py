#!/usr/bin/env python


import sklearn.neural_network
import sklearn.svm
import sklearn.discriminant_analysis

import numpy as np
import time
import os

from hepstore.core.utility import *
from hepstore.core.statistic.distribution import Log10Flat

from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import classification_report

import sklearn.model_selection 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import ShuffleSplit
import scipy

import tuning
        
class SVR(sklearn.svm.SVR):
    
    def __init__(self, C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0,
                 shrinking=True, probability=True, tol=0.001, cache_size=200,
                 class_weight=None, verbose=False, max_iter=-1,
                 decision_function_shape=None, random_state=None,
                 path=os.getcwd(), jobs=1 ):
        sklearn.svm.SVC.__init__(
            self, C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0,
            shrinking=shrinking, probability=probability, tol=tol, cache_size=cache_size,
            class_weight=class_weight, verbose=verbose, max_iter=max_iter,
            decision_function_shape=decision_function_shape, random_state=random_state
        )
        self.path = path
        self.jobs = jobs
        pass

    def explore( self, X, y ):
        path = os.path.join(self.path,self.kernel,'shrinking_%s' % str(self.shrinking))
        print '--SVC: explore'
        # specify parameters for exploration
        if self.kernel == 'rbf':
            param_dist = {
                'C'        : Log10Flat(-10,-0.001),
                'gamma'    : Log10Flat(-10,-0.001),
            }
            pass
        else:
            raise KeyError("explore unknown kernel '%s' " % self.kernel)
        # tune classifier
        tuning.tune( self, X, y, param_dist,
              path         = path,
              jobs         = self.jobs,
              random_state = self.random_state
        )
        pass

    def predict_proba( self, data ):
        return self.predict( data )
    
    pass
