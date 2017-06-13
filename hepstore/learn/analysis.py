#!/usr/bin/env python


import numpy as np
import sys,os

from hepstore.eas.tools import *

import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib import cm
from sklearn.preprocessing import StandardScaler 
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import validation_curve
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import random

class DataUnit:
    def __init__(self,crossection=0.0,label=[],data=None,name="signal"):
        self.crossection = crossection
        self.data        = data
        self.label       = label
        self.name        = name
        pass
    def __add__(self,other):
        result = DataUnit()
        result.crossection = self.crossection + other.crossection
        result.data        = np.concatenate((self.data,other.data))
        result.label       = (self.label+other.label)
        result.name        = self.name
        return result
    def train_test_split(self,test_size=0.25, random_state=0):
        return train_test_split(self.data,self.label,test_size=test_size,random_state=random_state)
        pass
    def oneD(self,axis=0):
        return self.data[:,axis]
    def twoD(self,axis=[0,1]):
        return self.data[:,axis[0]],self.data[:,axis[1]]
    def loadFromUnbinned(self,data,label):
        dlist      = []
        self.label = []
        for sdata in data.data:
            dlist.append(sdata.coordinates)
            self.label.append(label)
            pass
        self.data = np.array(dlist)
        pass
    def enhance(self,arg_list):
        num        = int(arg_list[0])
        if num>1:
            spread     = arg_list[1:]
            new_points = []
            new_labels = []
            for d,label in zip(self.data,self.label):
                for i in range(0,num):
                    coordinates=[]
                    for val,delta in zip(d,spread):
                        coordinates.append( random.uniform( val-abs(val*delta),val+abs(val*delta) ) )
                        pass
                    new_points.append(coordinates)
                    new_labels.append(label)
                    pass
                pass
            self.data = np.concatenate((self.data,np.array(new_points)))
            self.label= (self.label+new_labels)
            pass
        pass
    pass

class DataAnalysis:
    def __init__(self,random_state=0,test_size=0.25,classifier="svc",luminosity=20000.,crossection=[0.5,0.5]):
        self.data         = {}
        self.random_state = random_state
        self.test_size    = test_size
        self.luminosity   = luminosity
        self.crossection  = crossection
        if classifier.lower() == "svc":
            self.classifier = SVC(C=1.0,kernel='rbf',probability=True,random_state=self.random_state)
            pass
        elif classifier.lower() == "mlp":
            self.classifier = MLPClassifier()
        self.enhance    = 1
        self.ntotal     = 1
        self.use_labels = ['s','b']
        pass
    def addData(self,data):
        self.data[data.name] = data
        pass
    def prepare(self):
        # generate train and test data
        self.data_train  = None
        self.label_train = None
        self.data_test   = None
        self.label_test  = None
        alldata          = None
        for name in self.data:
            data=self.data[name]
            if alldata==None:
                alldata = data
                pass
            else:
                alldata = alldata + data
                pass
            pass
        self.data_train,self.data_test,self.label_train,self.label_test = alldata.train_test_split()
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
    def probabilityMap(self,axes=[0,1],zoom=0.15,npoints=2000):
        data=np.concatenate((self.data_train,self.data_test))
        field=[]
        rangex=[min(data[:,axes[0]]),max(data[:,axes[0]])]
        rangey=[min(data[:,axes[1]]),max(data[:,axes[1]])]
        lx=zoom*abs(rangex[1]-rangex[0])
        ly=zoom*abs(rangey[1]-rangey[0])
        rangex=[rangex[0]-lx,rangex[1]+lx]
        rangey=[rangey[0]-ly,rangey[1]+ly]
        for i in range(0,npoints):
            field.append([np.random.uniform(rangex[0],rangex[1]),np.random.uniform(rangey[0],rangey[1])])
            pass
        x=[]
        y=[]
        z=[]
        for classification,coordinates in zip(self.classifier.predict_proba(self.scaler.transform(field))[:,1:],field):
            x.append(coordinates[0])
            y.append(coordinates[1])
            z.append(classification[0])
            pass
        return x,y,z
    def ROC(self,nbins=1000,labels=['s','b']):
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
        y = [ 1.-sum(counts_background[:pos])*delta for pos in range(0,len(counts_background)) ]
        return x,y
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
    def getData(self,label='s'):
        result = []
        for data in self.data.values():
            for point,l in zip(data.data,data.label):
                if label==l:
                    result.append(point)
                pass
            pass
        return np.array(result)
    def plot(self,path):

        colors = ['red','blue','green','pink','purple','orange']
        
        print "--info: plotting"
        fig = plt.figure(1,figsize=(18.6, 6.2))
        
        ## plot training vs testing classifier
        plt.subplot(131)
        nbins=20
        for l,c in zip(self.use_labels,colors):
            plt.hist(self.train_results[l],bins=nbins,normed=True,range=(0,1),alpha=0.5,color=c)
        
            counts,bin_edges = np.histogram(self.test_results[l],bins=nbins,range=(0.,1.),normed=True)
            bin_centres      = (bin_edges[:-1] + bin_edges[1:])/2.
            err              = np.sqrt(self.enhance)*np.sqrt(counts)/np.sqrt(len(self.test_results[l]))
            plt.errorbar(bin_centres, counts, yerr=err, fmt='o', color=c)

            pass
        
        ## plot data vs learned function
        plt.subplot(132)
        for l,c in zip(self.use_labels,colors):
            data = self.getData(l)
            plt.plot(data[:,0],data[:,1],",",color=c,alpha=0.8)
            pass
        x,y,z = self.probabilityMap()
        triang = tri.Triangulation(x, y)
        plt.tricontourf(x,y,z,
                        cmap=cm.Blues_r,
                        V=[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95],
                        alpha=0.6,
        )
        
        ## plot ROC and significance
        plt.subplot(133)
        ax1 = plt.gca()
        ax2 = ax1.twinx()
        
        sig_effs,bkg_effs = self.ROC()
        ax1.plot(sig_effs,bkg_effs,linestyle="-",color='black')
        
        sig_effs,sig_pois = self.significance()
        ax2.plot(sig_effs,sig_pois,linestyle="-",color='green')
        
        mkdir(path)
        fig.savefig(os.path.join(path,"learn.pdf"),format="pdf",dpi=300)
        pass
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
        
if __name__=='__main__': 
        
    analysis =  DataAnalysis()
    
    
    ## generate data
    nsig        = 600
    signal      = DataUnit(name="signal")
    signal.data = np.vstack((np.random.multivariate_normal([1.,-2.5],[[1,-0.5],[-0.5,1]], 3*nsig/4),np.random.multivariate_normal([-4.,3.5],[[1,-0.5],[-0.5,1]], nsig/4)))
    signal.label= ['s']*nsig
    
    nbkg            = 600
    background      = DataUnit(name="background")
    background.data = np.random.multivariate_normal([0.,0.],[[4.,0],[0,25.]], nbkg)
    background.label= ['b']*nbkg
    
    ## add data
    analysis.addData(signal)
    analysis.addData(background)
    
    ## prepare run
    analysis.prepare()
    
    ## train and test
    analysis.train()
    analysis.test()
    
    print "plotting"
    fig = plt.figure(1,figsize=(18.6, 6.2))
    
    ## plot training vs testing classifier
    print "a"
    plt.subplot(131)
    nbins=20
    
    plt.hist(analysis.train_results['s'],bins=nbins,normed=True,range=(0,1),alpha=0.5,color='red')
    plt.hist(analysis.train_results['b'],bins=nbins,normed=True,range=(0,1),alpha=0.5,color='blue')
    
    counts_sig,bin_edges_sig = np.histogram(analysis.test_results['s'],bins=nbins,range=(0.,1.),normed=True)
    bin_centres_sig = (bin_edges_sig[:-1] + bin_edges_sig[1:])/2.
    err_sig = np.sqrt(counts_sig)/np.sqrt(nsig)
    plt.errorbar(bin_centres_sig, counts_sig, yerr=err_sig, fmt='o', color='red')
    
    counts_bkg,bin_edges_bkg = np.histogram(analysis.test_results['b'],bins=nbins,range=(0.,1.),normed=True)
    bin_centres_bkg = (bin_edges_bkg[:-1] + bin_edges_bkg[1:])/2.
    err_bkg = np.sqrt(counts_bkg)/np.sqrt(nbkg)
    plt.errorbar(bin_centres_bkg, counts_bkg, yerr=err_bkg, fmt='o', color='blue')
    
    ## plot data vs learned function
    print "b"
    plt.subplot(132)
    plt.plot(background.oneD(axis=0),background.oneD(axis=1),",",color="black",alpha=0.8)
    plt.plot(signal.oneD(axis=0),signal.oneD(axis=1)        ,",",color="red"  ,alpha=0.8)
    x,y,z = analysis.probabilityMap()
    triang = tri.Triangulation(x, y)
    plt.tricontourf(x,y,z,
                    cmap=cm.Blues_r,
                    V=[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95],
                    alpha=0.6,
    )
    
    ## plot ROC and significance
    print "c"
    plt.subplot(133)
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    sig_effs,bkg_effs = analysis.ROC()
    ax1.plot(sig_effs,bkg_effs,linestyle="-",color='black')
    
    sig_effs,sig_pois = analysis.significance(luminosity=1000,crossection=[0.1,20])
    ax2.plot(sig_effs,sig_pois,linestyle="-",color='green')
    
    
    fig.savefig("plot.pdf",format="pdf",dpi=300)
    
