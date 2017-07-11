#!/usr/bin/env python


import sklearn.neural_network
import sklearn.svm
import sklearn.discriminant_analysis

import numpy as np
import time
import os

from hepstore.core.tools import *
from hepstore.core.statistics.distribution import Log10Flat

from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import classification_report

import sklearn.model_selection 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import ShuffleSplit
import scipy

import tuning
        
class SVC(sklearn.svm.SVC):
    
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
    
    pass


class Book(object):

    def __init__(self,options):
        if options.classifier.lower() == 'svc':
            self.classifier = SVC(
                C=options.c_parameter, kernel=options.kernel, degree=options.degree,
                gamma=options.gamma, coef0=options.coef0,
                shrinking=options.shrinking, probability=True,
                tol=options.tol, cache_size=options.cache_size,
                class_weight=None, verbose=options.verbose, max_iter=options.max_iter,
                decision_function_shape=None, random_state=options.random_state,
                path=options.path, jobs=options.jobs)
            pass
        elif options.classifier.lower() == 'mlp':
            self.classifier = MLPClassifier(
                hidden_layer_sizes=options.hidden_layers, activation=options.activation, solver=options.solver,
                alpha=options.alpha, batch_size='auto', learning_rate='constant',
                learning_rate_init=0.001, power_t=0.5, max_iter=options.max_iter,
                shuffle=True, random_state=options.random_state, tol=options.tol, verbose=options.verbose,
                warm_start=False, momentum=0.9, nesterovs_momentum=True,
                early_stopping=False, validation_fraction=0.1, beta_1=0.9,
                beta_2=0.999, epsilon=1e-08,
                path=options.path, jobs=options.jobs )
            pass
        elif options.classifier.lower() == 'lda':
            self.classifier = LinearDiscriminantAnalysis(
                solver=options.solver, shrinkage=options.shrinkage,
                priors=None, n_components=None,
                store_covariance=options.store_covariance,
                tol=options.tol, random_state=options.random_state,
                path=options.path, jobs=options.jobs)
            pass
        elif options.classifier.lower() == 'qda':
            self.classifier = QuadraticDiscriminantAnalysis(
                priors=None, reg_param=options.reg_param,
                random_state=options.random_state,
                store_covariances=options.store_covariance, tol=options.tol,
                path=options.path, jobs=options.jobs)
            pass
        else:
            raise KeyError("unknown classifier '%s' " % options.classifier )
        pass

    pass
