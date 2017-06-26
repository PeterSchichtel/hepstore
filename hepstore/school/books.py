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
def parameter_search(classifier,parameters,n_iter_search,X,y,mode="random"):
    if mode=="random":
        # run randomized search
        start = time.time()
        random_search = RandomizedSearchCV(classifier, param_distributions=parameters,
                                           n_iter=n_iter_search)
        random_search.fit(X,y)
        print("--info:: RandomizedSearchCV took %.2f seconds for %i candidates"
              " parameter settings." % ( (time.time() - start), n_iter_search )
        )
        report(random_search.cv_results_)
        pass
    else:
        raise NotImplemented("cannot explore method %s" % method)
    pass

# Utility function to create validation curve
def validation_curve(classifier,parameter,param_range,X,y,path=os.getcwd()):
    train_scores, test_scores = sklearn.model_selection.validation_curve(
        classifier, X, y, parameter, param_range,
        cv=10, scoring="accuracy", n_jobs=1,
    )
    train_scores = np.vstack( (param_range,np.mean(train_scores, axis=1),np.std(train_scores , axis=1)) ).T
    test_scores  = np.vstack( (param_range,np.mean(test_scores , axis=1),np.std(test_scores  , axis=1)) ).T
    # save for plotting
    mkdir(path)
    np.save(os.path.join(path,'train_scores_%s.npy' % parameter),train_scores)
    np.save(os.path.join(path,'test_scores_%s.npy'  % parameter),test_scores )
    pass
        
            
class LinearDiscriminantAnalysis(sklearn.discriminant_analysis.LinearDiscriminantAnalysis):

    def __init__(self,
                 solver='svd', shrinkage=None, priors=None, n_components=None,
                 store_covariance=False, tol=0.0001, path=os.getcwd() ):
        if solver=='svd' and shrinkage is not None:
            print "--LDA: warning setting 'shrinkage' to 'None', for SVD"
            shrinkage=None
            pass
        sklearn.discriminant_analysis.LinearDiscriminantAnalysis.__init__(
            self,solver=solver, shrinkage=shrinkage, priors=priors,
            n_components=n_components, store_covariance=store_covariance, tol=tol
        )
        self.path = path
        pass
    
    def explore(self,X,y,mode="random",n_iter_search=200):
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
            parameter_search( self  ,param_dist[1], param_dist[0], X, y, mode=mode )
            pass
        # check for over/under-training
        for solver in [ 'eigen', 'lsqr']:
            for parameter in [ 'shrinkage' ]:
                param_range =  np.logspace(-7, 0, n_iter_search)
                classifier  = sklearn.discriminant_analysis.LinearDiscriminantAnalysis( solver=solver )
                validation_curve(classifier,parameter,param_range,X,y,os.path.join(self.path,solver))
                pass
            pass
        pass
    
    pass

class QuadraticDiscriminantAnalysis(sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis):

    def __init__(self, priors=None, reg_param=0.0,
                 store_covariances=False, tol=0.0001, path=os.getcwd() ):
        sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis.__init__(
            self, priors=priors, reg_param=reg_param,
            store_covariances=store_covariances, tol=tol,
        )
        self.path = path
        pass

    def explore(self,X,y,mode="random",n_iter_search=200):
        # specify parameters for exploration
        param_dist = { "reg_param": scipy.stats.uniform(0,1),
                       "tol"      : scipy.stats.uniform(0.00001,0.001),
                       }
        # perform random search
        parameter_search( self, param_dist, n_iter_search, X, y, mode=mode)
        # check for over/under-training
        for parameter in param_dist:
            param_range = np.logspace(-7,0,n_iter_search)
            classifier  = sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis()
            validation_curve(classifier,parameter,param_range,X,y,self.path)
            pass
        pass
    
    pass

class SVC(sklearn.svm.SVC):

    def __init__(self,*args,**kwargs):
        sklearn.svm.SVC.__init__(self,*args,**kwargs)
        pass

    def explore(self,method=None):
        raise NotImplemented("SVC explore not implementd, yet!")
    
    pass

class MLPClassifier(sklearn.neural_network.MLPClassifier):

    def __init__(self,*args,**kwargs):
        sklearn.neural_network.MPLClassifier.__init__(self,*args,**kwargs)
        pass

    def explore(self,method=None):
        raise NotImplemented("MLP explore not implementd, yet!")
    
    pass


class Book(object):

    def __init__(self,options):
        if options.classifier.lower() == "svc":
            self.classifier = SVC(C=1.0,kernel='rbf',probability=True,random_state=options.random_state)
            pass
        elif options.classifier.lower() == "mlp":
            self.classifier = MLPClassifier()
            pass
        elif options.classifier.lower() == "lda":
            self.classifier = LinearDiscriminantAnalysis(
                solver=options.solver, shrinkage=options.shrinkage,
                priors=None, n_components=None,
                store_covariance=options.store_covariance,
                tol=options.tol,
                path=options.path)
            pass
        elif options.classifier.lower() == "qda":
            self.classifier = QuadraticDiscriminantAnalysis(
                priors=None, reg_param=options.reg_param,
                store_covariances=options.store_covariance, tol=options.tol,
                path=options.path)
            pass
        else:
            raise NotImplemented("unknown classifier '%s' " % options.classifier )
        pass

    pass
