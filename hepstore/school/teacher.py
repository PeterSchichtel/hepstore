#!/usr/bin/env python

import os

import numpy as np
import sys

import hepstore.tools as tools

from errors import *
from student import *
from data import *

from itertools import cycle
from sklearn.preprocessing import StandardScaler 
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import validation_curve
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis


class Teacher(object):

    def __init__(self,options):
        self.options = options
        self.student = None
        # create cyclers for options
        self.label = cycle(tools.options_to_list(options.label))
        pass

    def teach(self):
        # load data
        for fin in self.options.file:
            raw_data = np.load(fin)
            data     = DataUnit(raw_data,np.array([next(self.label)]*len(raw_data)))
            if self.student == None:
                self.student = Student(self.options,data)
                pass
            else:
                self.student.add_data(data)
                pass
            pass
        # explore classifier
        if self.options.explore or self.options.only_explore:
            self.student.explore()
            pass
        # train student
        if not self.options.only_explore:
            self.student.prepare()
            # check that training is allowed
            if len(np.unique(self.student.label_train))<=1:
                raise LabelError("not enough labels for training")
            self.student.train()
            self.student.test()
            pass
        pass

    def save(self):
        tools.mkdir(self.options.path)
        # preparation results
        if self.options.explore or self.options.only_explore:
            pass
        if not self.options.only_explore:
            self.student.save()
            pass
        pass

    pass
