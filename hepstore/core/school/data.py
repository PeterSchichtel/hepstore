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

from hepstore.errors import *

    
class DataUnit(object):

    def __init__(self,data=None,classification=None):
        self.data           = data
        self.classification = classification
        pass

    def __add__(self,other):
        result = DataUnit()
        result.data            = np.concatenate((self.data,           other.data))
        result.classification  = np.concatenate((self.classification, other.classification))
        return result

    def train_test_split(self,test_size=0.25,random_state=0):
        return train_test_split(self.data,self.classification,test_size=test_size,random_state=random_state)
        pass

    def zip(self):
        return zip(self.data.tolist(),self.classification.tolist())
    
    def log_transform(self):
        new_data = []
        new_label= []
        for data,label in self.zip():
            if any(d<=0.0 for d in data):
                continue
            new_data.append(data)
            new_label.append(label)
            pass
        self.data = np.log(np.array(new_data))
        self.classification = np.array(new_label)
        pass

    pass


