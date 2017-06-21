#!/usr/bin/env python


import numpy as np
import sys,os

import hepstore.tools as tools


from itertools import cycle
from sklearn.preprocessing import StandardScaler 
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import validation_curve
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

class dataunit(object):

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

class student(object):

    def __init__(self,options,data):
        self.options      = options
        self.data         = data
        if options.classifier.lower() == "svc":
            self.classifier = SVC(C=1.0,kernel='rbf',probability=True,random_state=self.options.random_state)
            pass
        elif options.classifier.lower() == "mlp":
            self.classifier = MLPClassifier()
        pass

    def add_data(self,data):
        self.data += data
        pass

    def explore(self):
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

class analysis(object):

    def __init__(self,options):
        self.options = options
        self.student = None
        # create cyclers for options
        self.label = cycle(tools.options_to_list(options.label))
        pass

    def run(self):
        # load data
        for fin in self.options.file:
            raw_data = np.load(fin)
            data     = dataunit(raw_data,[next(self.label)]*len(raw_data))
            if self.student == None:
                self.student = student(self.options,data)
                pass
            else:
                self.student.add_data(data)
                pass
            pass
        # train student
        self.student.prepare()
        self.student.train()
        self.student.test()
        # save results and cross checks
        self.save()
        pass

    def save(self):
        tools.mkdir(self.options.path)

        # preparation results
        if self.options.explore:
            pass

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

        # significance
        
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
    
    def roc(self,bins=1000):
        data_scaled = np.concatenate((self.student.data_train_scaled, self.student.data_test_scaled))
        labels      = np.concatenate((self.student.label_train      , self.student.label_test))
        delta       = 1./float(bins) 
        data        = {}
        for label in np.unique(labels):
            data[label] = []
            pass
        for label,classification in zip( labels, self.student.classifier.predict_proba( data_scaled ) ):
            data[label].append(classification[0])
            pass
        # collect signal and background
        signal     = None
        background = None
        for label in data:
            if label in self.options.signal:
                if signal == None:
                    signal = data[label]
                    pass
                else:
                    signal = np.concatenate((signal,data[label]))
                    pass
                pass
            else:
                if background == None:
                    background = data[label]
                    pass
                else:
                    background = np.concatenate((background,data[label]))
                pass
            pass
        # compute signal and background efficiencies
        counts_signal,bin_edges_signal         = np.histogram(signal,    bins=bins,range=(0,1),normed=True)
        counts_background,bin_edges_background = np.histogram(background,bins=bins,range=(0,1),normed=True)
        points = []
        for i in range(0,bins):
            x = sum(counts_signal[:i])*delta
            y = 1.0 - sum(counts_background[:i])*delta
            points.append([x,y])
            pass
        return np.array(points)
    
    def significance(self,labels=['s','b'],nbins=1000):
        delta=1./float(nbins)
        data={labels[0]:[],labels[1]:[]}
        for label,classification in zip( np.concatenate((self.label_train,self.label_test)) , self.classifier.predict_proba( np.concatenate((self.data_train_scaled,self.data_test_scaled)) )):
            if label in data:
                data[label].append(classification[0])
                pass
            pass
        counts_signal,bin_edges_signal         = np.histogram(data[labels[0]],bins=nbins,range=(0,1),normed=True)
        counts_background,bin_edges_background = np.histogram(data[labels[1]],bins=nbins,range=(0,1),normed=True)
        x = [ sum(counts_signal[:pos])*delta        for pos in range(0,len(counts_signal    )) ]
        y = []
        for pos in range(0,len(counts_signal)):
            es  = sum(counts_signal[:pos]    )*delta
            eb  = sum(counts_background[:pos])*delta
            if es>0.0 or eb>0.0:
                sig = np.sqrt( (self.luminosity * es**2 * self.crossection[0]**2 )/( es * self.crossection[0]  +  eb * self.crossection[1] ) )
                pass
            else:
                sig = 0.0
                pass
            y.append(sig)
            pass
        return x,y

    
    def maxSignificance(self,labels=['s','b']):
        sig_effs,sig_pois = self.significance(labels=labels)
        use_s=[]
        for es,s in zip(sig_effs,sig_pois):
            if es>0.05:
                use_s.append([es,s])
                pass
            pass
        use_s = np.array(use_s)
        max_s   = max(use_s[:,1])
        index_s = use_s[:,1].tolist().index(max_s)
        max_es  = use_s[index_s,0]
        return max_s,max_es
    
    def twoSigmaLuminosity(self,labels=['s','b']):
        max_s,max_es = self.maxSignificance(labels=labels)
        es,eb        = self.ROC(labels=labels)
        index = es.index(max_es)
        return 4.0 * ( max_es * self.crossection[0]  +  eb[index] * self.crossection[1] ) / ( max_es**2 * self.crossection[0]**2 )
    
    def minCrossection(self,labels=['s','b']):
        old_xsec = self.crossection
        max_sign = []
        xsecs    = []
        step=1
        if self.ntotal>50:
            step = 2*self.ntotal/50
            pass
        for i in range(0,self.ntotal,step):
            try:
                xsec_sig = float(i)/float(self.luminosity)
                xsec_bkg = float(self.ntotal-i)/float(self.luminosity)
                self.crossection = [xsec_sig,xsec_bkg]
                max_s,max_es = self.maxSignificance(labels=labels)
                max_sign.append(max_s)
                xsecs.append(xsec_sig)
                pass
            except Exception:
                pass
            pass
        max_s = next(x for x in sorted(max_sign) if x > 1.999)
        xsec  = xsecs[max_sign.index(max_s)]
        return max_s,xsec
    
    def __str__(self):
        max_s,max_es = self.maxSignificance(self.use_labels)
        thestr = "--significance: sigma = %f at epsilon_s =  %f \n" % (max_s,max_es,)
        lumi         = self.twoSigmaLuminosity(self.use_labels)
        thestr+= "--significance: lumi  = %f at sigma     =  %f \n" % (lumi,2.0)
        max_s,xsec   = self.minCrossection(self.use_labels)
        thestr+= "--significance: xsec  = %f at sigma     =  %f \n" % (xsec,max_s)
        return thestr
    pass
 
