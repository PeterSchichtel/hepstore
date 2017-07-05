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
        raise NotImplemented("cannot explore method %s" % method)
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
    train_scores      = np.concatenate( (train_sizes,train_scores_mean,train_scores_std) )
    test_scores       = np.concatenate( (train_sizes,test_scores_mean, test_scores_std ) )
    mkdir(path)
    np.save(os.path.join(path,'learning_curve_train.npy'),train_scores)
    np.save(os.path.join(path,'learning_curve_text.npy' ),test_scores )
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
    
    def explore(self,X,y,mode="random",n_iter_search=200,n_splits=20):
        print "--LDA: explore"
        # specify parameters for exploration
        param_dists = [
            (n_iter_search,{"solver"   : [ 'eigen', 'lsqr' ],
             "shrinkage": scipy.stats.uniform(0,1),
             "tol"      : scipy.stats.uniform(0.00001,0.001),}),
            (n_iter_search,{"solver"   : [ 'eigen', 'lsqr' ],
             "shrinkage": [ None, 'auto' ],
             "tol"      : scipy.stats.uniform(0.00001,0.001),}),
            (1,{"solver"   : [ 'svd' ],
             "shrinkage": [ None ],}),
            ]
        # perform random search
        for param_dist in param_dists:
            parameter_search( self  ,param_dist[1], param_dist[0], X, y, mode=mode, jobs=self.jobs, random_state=self.random_state )
            pass
        # check for over/under-training
        for solver in [ 'eigen', 'lsqr']:
            for parameter in [ 'shrinkage' ]:
                param_range = np.logspace(-7, 0, n_iter_search)
                classifier  = sklearn.discriminant_analysis.LinearDiscriminantAnalysis( solver=solver )
                validation_curve( classifier, parameter, param_range, X, y, os.path.join(self.path,solver), jobs=self.jobs )
                pass
            pass
        # generate learning curve
        cv = ShuffleSplit(n_splits=n_splits, test_size=0.2, random_state=self.random_state)
        learning_curve( self , X, y, cv=cv, path=self.path, n_jobs=self.jobs)
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

    def explore(self,X,y,mode='random',n_iter_search=200,n_splits=20):
        print "--QDA: explore"
        # specify parameters for exploration
        param_dist = { 'reg_param': scipy.stats.uniform(0,1),
                       'tol'      : scipy.stats.uniform(0.00001,0.001),
                       }
        # perform random search
        parameter_search( self, param_dist, n_iter_search, X, y, mode=mode, jobs=self.jobs, random_state=self.random_state )
        # check for over/under-training
        for parameter in param_dist:
            param_range = np.logspace(-7,0,n_iter_search)
            classifier  = sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis()
            validation_curve( classifier, parameter, param_range, X, y, self.path, jobs=self.jobs )
            pass
        # generate learning curve
        cv = ShuffleSplit(n_splits=n_splits, test_size=0.2, random_state=self.random_state)
        learning_curve( self , X, y, cv=cv, path=self.path, n_jobs=self.jobs)
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

    def explore(self,X,y,mode='random',n_iter_search=20,n_splits=20):
        print '--MLP: explore'
        # specify parameters for exploration
        param_dist = {
            'alpha'    : scipy.stats.uniform(0,1),
            'tol'      : scipy.stats.uniform(0,1),
            'momentum' : scipy.stats.uniform(0,1),
        }
        # perform random search
        parameter_search( self, param_dist, n_iter_search, X, y, mode=mode, jobs=self.jobs, random_state=self.random_state )
        # check for over/under-training
        for parameter in param_dist:
            param_range = np.logspace(-7,0,n_iter_search)
            classifier  = sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis()
            validation_curve( classifier, parameter, param_range, X, y, os.path.join(self.path,self.solver,self.activation), jobs=self.jobs )
            pass
        # generate learning curve
        cv = ShuffleSplit(n_splits=n_splits, test_size=0.2, random_state=self.random_state)
        learning_curve( self , X, y, cv=cv, path=os.path.join(self.path,self.solver,self.activation), n_jobs=self.jobs)
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

    def explore(self,X,y,mode='random',n_iter_search=20,n_splits=20):
        print '--SVC: explore'
        # specify parameters for exploration
        param_dist = {
            'C'        : scipy.stats.uniform(0.001,1.0),
            'gamma'    : scipy.stats.uniform(0.001,1.0),
            'tol'      : scipy.stats.uniform(0.00001,0.01),
            'shrinking':  [ True , False ],
        }
        if self.kernel == 'poly':
            param_dist['degree']  = [ 1, 2, 3]
            pass
        # perform random search
        parameter_search( self, param_dist, n_iter_search, X, y, mode=mode, jobs=self.jobs )
        # check for over/under-training
        for shrinking in param_dist['shrinking']:
            for parameter in param_dist:
                if parameter is 'shrinking':
                    continue
                print param_dist[parameter]
                print param_dist[parameter].args
                param_range = np.logspace( param_dist[parameter].args[0],
                                           param_dist[parameter].args[1],
                                           n_iter_search)
                if parameter == 'degree':
                    param_range = np.linspace(1,3,3,dtype=int)
                    pass
                print param_range
                classifier  = sklearn.svm.SVC(
                    kernel=self.kernel, shrinking=shrinking, random_state=self.random_state)
                validation_curve( classifier, parameter, param_range, X, y, os.path.join(
                    self.path,self.kernel,'shrinking_%s' % str(shrinking)
                ), jobs=self.jobs )
                pass
            pass
        # generate learning curve
        cv = ShuffleSplit(n_splits=n_splits, test_size=0.2, random_state=self.random_state)
        learning_curve( self , X, y, cv=cv, path=self.path, n_jobs=self.jobs)
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
            if options.solver in [ 'sgd', 'adam', 'lbfgs' ]:
                solver = options.solver
                pass
            else:
                solver = 'adam'
                pass
            self.classifier = MLPClassifier(
                hidden_layer_sizes=(100, ), activation='relu', solver=solver,
                alpha=0.0001, batch_size='auto', learning_rate='constant',
                learning_rate_init=0.001, power_t=0.5, max_iter=200,
                shuffle=True, random_state=None, tol=0.0001, verbose=False,
                warm_start=False, momentum=0.9, nesterovs_momentum=True,
                early_stopping=False, validation_fraction=0.1, beta_1=0.9,
                beta_2=0.999, epsilon=1e-08,
                path=os.getcwd(), jobs=1 )
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
            raise NotImplemented("unknown classifier '%s' " % options.classifier )
        pass

    pass
