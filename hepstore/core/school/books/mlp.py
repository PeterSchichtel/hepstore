#!/usr/bin/env python


import sklearn.neural_network
import sklearn.svm
import sklearn.discriminant_analysis

import numpy as np
import time
import os

from hepstore.core.tools import *
from hepstore.core.statistics.distributions import Log10Flat

from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import classification_report

import sklearn.model_selection 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import ShuffleSplit
import scipy

import tuning

class MLPClassifier(sklearn.neural_network.MLPClassifier):

    def __init__( self, hidden_layer_sizes=(100, ), activation='relu', solver='adam',
                  alpha=0.0001, batch_size='auto', learning_rate='constant',
                  learning_rate_init=0.001, power_t=0.5, max_iter=200,
                  shuffle=True, random_state=None, tol=0.0001, verbose=False,
                  warm_start=False, momentum=0.9, nesterovs_momentum=True,
                  early_stopping=False, validation_fraction=0.1, beta_1=0.9,
                  beta_2=0.999, epsilon=1e-08,
                  path=os.getcwd(), jobs=1 ):
        sklearn.neural_network.MLPClassifier.__init__( self, hidden_layer_sizes=hidden_layer_sizes,
                                              activation=activation, solver=solver,
                                              alpha=alpha, batch_size=batch_size,
                                              learning_rate=learning_rate,
                                              learning_rate_init=learning_rate_init, power_t=power_t,
                                              max_iter=200, shuffle=True, random_state=None,
                                              tol=tol, verbose=verbose, warm_start=warm_start,
                                              momentum=momentum, nesterovs_momentum=nesterovs_momentum,
                                              early_stopping=early_stopping, validation_fraction=validation_fraction,
                                              beta_1=beta_1, beta_2=beta_2, epsilon=epsilon )
        self.path = path
        self.jobs = jobs
        pass

    def explore( self, X, y ):
        path = os.path.join(self.path,self.solver,self.activation)
        print '--MLP: explore'
        # specify parameters for exploration
        if self.solver == 'lbfgs':
            param_dist = {
                'alpha'    : Log10Flat(-10,-0.001),
                'tol'      : Log10Flat(-10,-0.001),
            }
            pass
        elif self.solver == 'adam':
            param_dist = {
                'alpha'    : Log10Flat(-10,-0.001),
                'tol'      : Log10Flat(-10,-0.001),
                'beta_1'   : Log10Flat(-10,-0.001),
                'beta_2'   : Log10Flat(-10,-0.001),
            }
            pass
        else:
            raise KeyError("explore solver '%s' not implementd" % self.solver)
        # tune classifier
        tuning.tune( self, X, y, param_dist,
              path          = path,
              jobs          = 1,  ## bug in MLPClassifier!!
              random_state  = self.random_state
        )
        pass
    
    pass


