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


class MetaClassifier(object):

    def __init__(self,options):
        if options.classifier.lower() == "svc":
            self.classifier =  SVC(C=1.0,kernel='rbf',probability=True,random_state=options.random_state)
            pass
        elif options.classifier.lower() == "mlp":
            self.classifier =  MLPClassifier()
        else:
            raise NotImplemented("unknown classifier '%s' " % options.classifier )
        pass

    def explore(self):
        pass

    pass
    
class DataUnit(object):

    def __init__(self,data=None,classification=None):
        self.data           = data
        self.classification = classification
        pass

    def __add__(self,other):
        result = dataunit()
        result.data            = np.concatenate((self.data,           other.data))
        result.classification  = np.concatenate((self.classification, other.classification))
        return result

    def train_test_split(self,test_size=0.25,random_state=0):
        return train_test_split(self.data,self.classification,test_size=test_size,random_state=random_state)
        pass

    def zip(self):
        return zip(self.data,self.classification)

    pass

class Student(object):

    def __init__(self,options,data):
        self.options      = options
        self.data         = data
        self.classifier   = MetaClassifier(options)
        pass

    def add_data(self,data):
        self.data += data
        pass

    def explore(self):
        self.classifier.explore()
        pass

    def prepare(self):
        # generate train and test data
        self.data_train,self.data_test,self.label_train,self.label_test = self.data.train_test_split(test_size=self.options.test_size,random_state=self.options.random_state)
        # scale
        self.scaler            = StandardScaler()
        self.scaler.fit(self.data_train)
        self.data_train_scaled = self.scaler.transform(self.data_train)
        self.data_test_scaled  = self.scaler.transform(self.data_test)
        # explore the classifier
        if self.options.explore:
            self.explore()
            pass
        pass

    def train(self):
        self.classifier.classifier.fit(self.data_train_scaled,self.label_train)
        results_train={}
        for label,classification in zip(self.label_train,self.classifier.classifier.predict_proba(self.data_train_scaled)):
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
        for label,classification in zip(self.label_test,self.classifier.classifier.predict_proba(self.data_test_scaled)):
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
            data     = DataUnit(raw_data,[next(self.label)]*len(raw_data))
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
            self.student.train()
            self.student.test()
            pass
        # save results and cross checks
        self.save()
        pass

    def save(self):
        tools.mkdir(self.options.path)
        # preparation results
        if self.options.explore or self.options.only_explore:
            pass
        if not self.options.only_explore:
            # training data
            np.save(os.path.join(self.options.path,"data_train.npy")     ,self.student.data_train)
            np.save(os.path.join(self.options.path,"label_train.npy")    ,self.student.label_train)
            # testing data
            np.save(os.path.join(self.options.path,"data_test.npy")      ,self.student.data_test)
            np.save(os.path.join(self.options.path,"label_test.npy")     ,self.student.label_test)
            # classifier map
            np.save(os.path.join(self.options.path,"probability_map.npy"),self.probability_map())
            # ROC
            np.save(os.path.join(self.options.path,"roc.npy")            ,self.roc())
            pass
        pass

    def probability_map(self):
        data   = np.concatenate((self.student.data_train,self.student.data_test))
        field  = []
        ranges = []
        # define a range with x% zoom for better plotting
        for i in range(0,data.shape[1]):
            values = [min(data[:,i]),max(data[:,i])]
            zoom   = self.options.zoom*abs(values[1]-values[0])
            values = [values[0]-zoom,values[1]+zoom]
            ranges.append(values)
            pass
        # create support points randomly
        for i in range(0,self.options.points):
            point = []
            for arange in ranges:
                point.append(np.random.uniform(arange[0],arange[1]))
                pass
            field.append(point)
            pass
        # fill field with classifier responce
        result = []
        for classification,coordinates in zip(self.student.classifier.predict_proba(self.student.scaler.transform(field))[:,1:],field):
            result.append(([classification[0]]+coordinates))
            pass
        return np.array(result)

    def efficiency(self,is_signal,bins=1000):
        # load data
        data_scaled = np.concatenate((self.student.data_train_scaled, self.student.data_test_scaled))
        labels      = np.concatenate((self.student.label_train      , self.student.label_test))
        data        = {}
        for label in np.unique(labels):
            data[label] = []
            pass
        for label,classification in zip( labels, self.student.classifier.predict_proba( data_scaled ) ):
            data[label].append(classification[0])
            pass
        # collect signal and background
        results     = None
        for label in data:
            if not is_signal or label in self.options.signal:
                if results == None:
                    results = data[label]
                    pass
                else:
                    results = np.concatenate((results,data[label]))
                    pass
                pass
            pass
        # compute signal and background efficiencies
        return np.histogram(results,bins=bins,range=(0,1),normed=True)
        
    def roc(self,bins=1000):
        delta       = 1./float(bins) 
        counts_signal    , bin_edges_signal     = self.efficiency(True ,bins=bins)
        counts_background, bin_edges_background = self.efficiency(False,bins=bins)
        # generate ROC
        points = []
        for i in range(0,bins):
            x = sum(counts_signal[:i])*delta
            y = 1.0 - sum(counts_background[:i])*delta
            points.append([x,y])
            pass
        return np.array(points)

    pass
