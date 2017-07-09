#!/usr/bin/env python

import numpy as np
import os
from hepstore.tools import *
import sklearn.model_selection 

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
        random_search = sklearn.model_selection.RandomizedSearchCV(classifier, param_distributions=parameters,
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
    cv = sklearn.model_selection.ShuffleSplit(n_splits=20, test_size=0.2, random_state=random_state)
    learning_curve( classifier , X, y, cv=cv, path=path, n_jobs=jobs)
    pass


