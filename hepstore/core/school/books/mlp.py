#!/usr/bin/env python


import sklearn.neural_network
import sklearn.svm
import sklearn.discriminant_analysis

import numpy as np
import time
import os

from hepstore.tools import *

from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import classification_report

import sklearn.model_selection 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import ShuffleSplit
import scipy

# Utility function to report best scores
def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("--info: Model with rank: {0}".format(i))
            print("--info: Mean validation score: {0:9.2e} (std: {1:9.2e})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("--info: Parameters: {0}".format(results['params'][candidate]))
            pass
        pass
    pass

# Utility function to perform parameter search
def parameter_search(classifier,parameters,n_iter_search,X,y,mode="random",jobs=1,random_state=None):
    if mode=="random":
        # run randomized search
        start = time.time()
        random_search = RandomizedSearchCV(classifier, param_distributions=parameters,
                                           n_iter=n_iter_search,
                                           n_jobs=jobs, random_state=random_state)
        random_search.fit(X,y)
        print("--info: RandomizedSearchCV took %.2f seconds for %i candidates"
              " parameter settings." % ( (time.time() - start), n_iter_search )
        )
        report(random_search.cv_results_)
        pass
    else:
        raise KeyError("cannot explore method %s" % method)
    pass

# Utility function to create validation curve
def validation_curve(classifier,parameter,param_range,X,y,path=os.getcwd(),jobs=1):
    train_scores, test_scores = sklearn.model_selection.validation_curve(
        classifier, X, y, parameter, param_range,
        cv=10, scoring="accuracy", n_jobs=jobs)
    train_scores = np.vstack( (param_range,np.mean(train_scores, axis=1),np.std(train_scores , axis=1)) ).T
    test_scores  = np.vstack( (param_range,np.mean(test_scores , axis=1),np.std(test_scores  , axis=1)) ).T
    # save for plotting
    mkdir(path)
    np.save(os.path.join(path,'train_scores_%s.npy' % parameter),train_scores)
    np.save(os.path.join(path,'test_scores_%s.npy'  % parameter),test_scores )
    pass

# Utility function to create learning curve
def learning_curve(classifier,X,y,cv=None,train_sizes=np.linspace(.1, 1.0, 5),path=os.getcwd(),n_jobs=1):
    train_sizes, train_scores, test_scores = sklearn.model_selection.learning_curve(
        classifier, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std  = np.std( train_scores, axis=1)
    test_scores_mean  = np.mean(test_scores,  axis=1)
    test_scores_std   = np.std( test_scores,  axis=1)
    train_scores = []
    for x,y,dy in zip(train_sizes.tolist(),train_scores_mean .tolist(),train_scores_std.tolist()):
        train_scores.append([x,y,dy])
        pass
    train_scores      = np.array(train_scores)
    test_scores = []
    for x,y,dy in zip(train_sizes.tolist(),test_scores_mean .tolist(),test_scores_std.tolist()):
        test_scores.append([x,y,dy])
        pass
    test_scores      = np.array(test_scores)
    mkdir(path)
    np.save(os.path.join(path,'learning_curve_train.npy'),train_scores)
    np.save(os.path.join(path,'learning_curve_test.npy' ),test_scores )
    pass

# Utility function to perfomr tuning/validation of classifier
def tune(classifier, X, y, param_dist, path=os.getcwd(), n_iter_search=100, jobs=1, random_state=None ):
    # perform random search
    parameter_search( classifier  , param_dist, n_iter_search, X, y, mode='random', jobs=jobs, random_state=random_state )
    # check for over/under-training
    for parameter in param_dist:
        param_range = np.logspace(-10, -0.001 , n_iter_search)
        validation_curve( classifier, parameter, param_range, X, y, path=path, jobs=jobs )
        pass
    # generate learning curve
    cv = ShuffleSplit(n_splits=20, test_size=0.2, random_state=random_state)
    learning_curve( classifier , X, y, cv=cv, path=path, n_jobs=jobs)
    pass

# Utility class for flat log_10 random
class Log10Flat(object):

    def __init__(self,start=0,stop=1):
        self.start = start
        self.stop  = stop
        pass

    def rvs(self, loc=0, scale=1, size=1, random_state=None):
        if size==1:
            return 10**(np.random.uniform(low=self.start,high=self.stop))
        else:
            return 10**(np.random.uniform(low=self.start,high=self.stop,size=size))
        pass
    
    pass

class LinearDiscriminantAnalysis(sklearn.discriminant_analysis.LinearDiscriminantAnalysis):

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
    
    def explore( self, X, y ):
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
        tune( self, X, y, param_dist,
              path         = path,
              jobs         = self.jobs,
              random_state = self.random_state
        )
        pass
    
    pass

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
        tune( self, X, y, param_dist,
              path         = path,
              jobs         = self.jobs,
              random_state = self.random_state
        )
        pass
    
    pass



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
        tune( self, X, y, param_dist,
              path          = path,
              jobs          = 1,  ## bug in MLPClassifier!!
              random_state  = self.random_state
        )
        pass
    
    pass

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
        tune( self, X, y, param_dist,
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
