#!/usr/bin/env python

import os

import numpy as np
import sys

import hepstore.tools as tools

from itertools import cycle
from sklearn.preprocessing import StandardScaler 
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import validation_curve
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis

from errors import *
from data import *

class ClassifierInterface(object):

    def __init__(self,options):
        if options.classifier.lower() == "svc":
            self.classifier =  SVC(C=1.0,kernel='rbf',probability=True,random_state=options.random_state)
            pass
        elif options.classifier.lower() == "mlp":
            self.classifier =  MLPClassifier()
            pass
        elif options.classifier.lower() == "lda":
            self.classifier = LinearDiscriminantAnalysis(solver='eigen',shrinkage='auto')
            pass
        elif options.classifier.lower() == "qda":
            self.classifier = QuadraticDiscriminantAnalysis()
            pass
        else:
            raise NotImplemented("unknown classifier '%s' " % options.classifier )
        pass

    def explore(self):
        pass

    pass

class Student(ClassifierInterface):

    def __init__(self,options,data):
        ClassifierInterface.__init__(self,options)
        self.options      = options
        self.data         = data
        pass

    def add_data(self,data):
        self.data += data
        pass

    def prepare(self):
        if self.option.log_transform:
            self.data.log_transform()
            pass
        # generate train and test data
        self.data_train,self.data_test,self.label_train,self.label_test = self.data.train_test_split(test_size=self.options.test_size,random_state=self.options.random_state)
        # scale
        self.scaler            = StandardScaler()
        self.scaler.fit(self.data_train)
        self.data_train_scaled = self.scaler.transform(self.data_train)
        self.data_test_scaled  = self.scaler.transform(self.data_test)
        pass

    def train(self):
        self.classifier.fit(self.data_train_scaled,self.label_train)
        results_train={}
        for label,classification in zip(self.label_train,self.classifier.predict_proba(self.data_train_scaled)):
            if label in results_train:
                results_train[label].append(classification[0])
                pass
            else:
                results_train[label] = [classification[0]]
                pass
            pass
        self.train_results = results_train
        pass

    def test(self):
        results_test={}
        for label,classification in zip(self.label_test,self.classifier.predict_proba(self.data_test_scaled)):
            if label in results_test:
                results_test[label].append(classification[0])
                pass
            else:
                results_test[label] = [classification[0]]
                pass
            pass
        self.test_results = results_test
        pass

    pass

