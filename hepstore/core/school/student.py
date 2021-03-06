#!/usr/bin/env python

# global imports 
import os
import numpy as np
from sklearn.externals import joblib
import sklearn.preprocessing

# hepstore imports
from hepstore.core.utility import *
from hepstore.core.error import *

# local imports
from data import *
import books

# our student class
class Student(object): ##books.Classifier,books.Regressor):

    def __init__( self, options, data=None ):
        self.options      = options
        self.data         = data
        if   options.classifier != '' and options.classifier != None:
            self.brain    = books.Classifier( options ).classifier
            pass
        elif options.regressor != '' and options.regressor != None:
            self.brain    = books.Regressor(  options ).regressor
            pass
        else:
            raise KeyError("brainless student")
        pass

    def add_data(self,data):
        self.data += data
        pass

    def prepare(self):
        if self.options.log_transform:
            self.data.log_transform()
            pass
        # generate train and test data
        self.data_train,self.data_test,self.label_train,self.label_test = self.data.train_test_split(test_size=self.options.test_size,random_state=self.options.random_state)
        # scale
        self.scaler            = sklearn.preprocessing.StandardScaler()
        self.scaler.fit(self.data_train)
        self.data_train_scaled = self.scaler.transform(self.data_train)
        self.data_test_scaled  = self.scaler.transform(self.data_test)
        pass

    def explore(self):
        self.brain.explore(self.data_train_scaled,self.label_train)
        pass

    def train(self):
        self.brain.fit(self.data_train_scaled,self.label_train)
        results_train = {}
        for label,prediction in zip(self.label_train,self.brain.predict_proba(self.data_train_scaled)):
            if label in results_train:
                results_train[label].append(prediction)
                pass
            else:
                results_train[label] = [prediction]
                pass
            pass
        self.train_results = np.array(results_train)
        pass

    def test(self):
        results_test={}
        for label,prediction in zip(self.label_test,self.brain.predict_proba(self.data_test_scaled)):
            if label in results_test:
                results_test[label].append(prediction)
                pass
            else:
                results_test[label] = [prediction]
                pass
            pass
        self.test_results = np.array(results_test)
        pass

    def save(self):
        dtrain = self.data_train
        ltrain = self.label_train
        dtest  = self.data_test
        ltest  = self.label_test
        if self.options.log_transform:
            dtrain = np.exp(dtrain)
            dtest  = np.exp(dtest)
            pass
        # training data
        np.save(os.path.join(self.options.path,"data_train.npy")     ,dtrain)
        np.save(os.path.join(self.options.path,"label_train.npy")    ,ltrain)
        # testing data
        np.save(os.path.join(self.options.path,"data_test.npy")      ,dtest)
        np.save(os.path.join(self.options.path,"label_test.npy")     ,ltest)
        # probability map
        np.save(os.path.join(self.options.path,"probability_map.npy"),self.probability_map())
        # ROC
        np.save(os.path.join(self.options.path,"roc.npy")            ,self.roc())
        # prediction distributions
        for label in np.unique(np.concatenate((ltrain,ltest))):
            np.save( os.path.join(self.options.path,'prediction_distribution_train_%s.npy' % str(label) ),
                     self.brain_distribution(label,True) )
            np.save( os.path.join(self.options.path,'prediction_distribution_test_%s.npy' % str(label) ),
                     self.brain_distribution(label,False) )
            pass
        # save brain as pkl
        joblib.dump( (self.brain,self.scaler) , self.options.save ) 
        pass

    def load(self):
        self.brain,self.scaler = joblib.load( self.options.load ) 
        pass

    def predict(self):
        # produce scaled data
        scaled_data              = self.scaler.transform( self.data.data )
        # predicted data
        probability_distribution = self.brain.predict_proba( scaled_data )
        # save output
        mkdir( self.options.path )
        np.save(
            os.path.join( self.options.path, "blind_predicted_output.npy" ),
            probability_distribution )
        pass 

    def prediction_distribution(self,label,train=True):
        # load data
        data_scaled = self.data_train_scaled 
        data_labels = self.label_train  
        if not train:
            data_scaled = self.data_test_scaled
            data_labels = self.label_test
            pass
        # generate distribution
        distr = []
        for prediction,true_label in zip( self.brain.predict_proba(data_scaled), data_labels):
            if label == true_label:
                distr.append(prediction)
                pass
            pass
        # return as np array
        return np.array(distr)

    def probability_map(self):
        data   = np.concatenate((self.data_train,self.data_test))
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
        # fill field with responce
        result = []
        for prediction,coordinates in zip(
                self.brain.predict_proba(self.scaler.transform(field)),
                field ):
            if self.options.log_transform:
                coordinates = np.exp(np.array(coordinates)).tolist()
                pass
            result.append( coordinates + prediction.tolist() )
            pass
        return np.array(result)

    def efficiency(self,labels,bins=1000):
        # load data
        data_scaled = np.concatenate((self.data_train_scaled, self.data_test_scaled))
        data_labels = np.concatenate((self.label_train      , self.label_test))
        data        = {}
        for label in np.unique(data_labels):
            data[label] = []
            pass
        for label,prediciton in zip( data_labels, self.brain.predict_proba( data_scaled ) ):
            data[label].append(prediction)
            pass
        # collect signal and background
        results     = None
        for label in data:
            if label in labels:
                if results == None:
                    results = data[label]
                    pass
                else:
                    results = np.concatenate((results,data[label]))
                    pass
                pass
            pass
        # compute signal and background efficiencies
        return np.histogram(results[:,0],bins=bins,range=(0,1),normed=True)
        
    def roc(self,bins=1000):
        delta                                   = 1./float(bins)
        counts_signal    , bin_edges_signal     = self.efficiency(self.options.signal_labels    ,bins=bins)
        counts_background, bin_edges_background = self.efficiency(self.options.background_labels,bins=bins)
        # generate ROC
        points = []
        for i in range(0,bins):
            x = sum(counts_signal[:i])*delta
            y = 1.0 - sum(counts_background[:i])*delta
            points.append([x,y])
            pass
        return np.array(points)
    
    pass

