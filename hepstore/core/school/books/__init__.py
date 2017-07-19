#!/usr/bin/env python

# gloabl imports
import os

# local imports
import classification
import regression

class Classifier(object):

    def __init__(self,options):
        
        if options.classifier.lower() == 'svm':
            self.classifier = classification.svm.SVC(
                C=options.c_parameter, kernel=options.kernel, degree=options.degree,
                gamma=options.gamma, coef0=options.coef0,
                shrinking=options.shrinking, probability=True,
                tol=options.tol, cache_size=options.cache_size,
                class_weight=None, verbose=options.verbose, max_iter=options.max_iter,
                decision_function_shape=None, random_state=options.random_state,
                path=options.path, jobs=options.jobs)
            pass
        
        elif options.classifier.lower() == 'mlp':
            self.classifier = classification.mlp.MLPClassifier(
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
            self.classifier = classification.lda.LinearDiscriminantAnalysis(
                solver=options.solver, shrinkage=options.shrinkage,
                priors=None, n_components=None,
                store_covariance=options.store_covariance,
                tol=options.tol, random_state=options.random_state,
                path=options.path, jobs=options.jobs)
            pass
        
        elif options.classifier.lower() == 'qda':
            self.classifier = classification.qda.QuadraticDiscriminantAnalysis(
                priors=None, reg_param=options.reg_param,
                random_state=options.random_state,
                store_covariances=options.store_covariance, tol=options.tol,
                path=options.path, jobs=options.jobs)
            pass

        elif options.classifier == None or options.classifier.lower() == '' :
            self.classifier = None
            pass
        
        else:    
            raise KeyError("unknown classifier '%s' " % options.classifier )
        
        pass

    pass


class Regressor(object):

    def __init__(self,options):
              
        if   options.regressor.lower() == 'mlp':
            self.regressor = regression.mlp.MLPRegressor(
                hidden_layer_sizes=options.hidden_layers, activation=options.activation, solver=options.solver,
                alpha=options.alpha, batch_size='auto', learning_rate='constant',
                learning_rate_init=0.001, power_t=0.5, max_iter=options.max_iter,
                shuffle=True, random_state=options.random_state, tol=options.tol, verbose=options.verbose,
                warm_start=False, momentum=0.9, nesterovs_momentum=True,
                early_stopping=False, validation_fraction=0.1, beta_1=0.9,
                beta_2=0.999, epsilon=1e-08,
                path=options.path, jobs=options.jobs )
            pass
        
        elif options.regressor.lower() == 'svm':
            self.regressor = regression.svm.SVR(
                C=options.c_parameter, kernel=options.kernel, degree=options.degree,
                gamma=options.gamma, coef0=options.coef0,
                shrinking=options.shrinking, probability=True,
                tol=options.tol, cache_size=options.cache_size,
                class_weight=None, verbose=options.verbose, max_iter=options.max_iter,
                decision_function_shape=None, random_state=options.random_state,
                path=options.path, jobs=options.jobs)
            pass
        
        #elif options.regressor.lower() == 'lda':
        #    self.regressor = regression.lda.LinearDiscriminantAnalysis(
        #        solver=options.solver, shrinkage=options.shrinkage,
        #        priors=None, n_components=None,
        #        store_covariance=options.store_covariance,
        #        tol=options.tol, random_state=options.random_state,
        #        path=options.path, jobs=options.jobs)
        #    pass
        
        #elif options.regressor.lower() == 'qda':
        #    self.regressor = regression.qda.QuadraticDiscriminantAnalysis(
        #        priors=None, reg_param=options.reg_param,
        #        random_state=options.random_state,
        #        store_covariances=options.store_covariance, tol=options.tol,
        #        path=options.path, jobs=options.jobs)
        #    pass

        elif options.regressor == None or options.regressor.lower() == '' :
            self.regressor = None
            pass
        
        
        else:    
            raise KeyError("unknown regressor '%s' " % options.regressor )
        
        pass

    pass

