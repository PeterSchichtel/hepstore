#!/usr/bin/env python

# module examples/hepstore_plot produce_data

# import for this module
import numpy as np

# number of events
nevents = 20000

# generate data set I
mean = np.array([0.0,0.0])
cov  = np.array([[1.0,0.0],[0.0,1.0]])
data = np.random.multivariate_normal(mean, cov, 2*nevents)
np.save('data_1.npy',data)

# generate data set II
mean = np.array([2.5,-2.5])
cov  = np.array([[1.0,0.0],[0.0,1.0]])
data = np.random.multivariate_normal(mean, cov, nevents)
mean = np.array([-1.4,0.8])
cov  = np.array([[0.02,1.2],[-1.7,0.01]])
data = np.concatenate((data,np.random.multivariate_normal(mean, cov, nevents)))
np.save('data_2.npy',data)
