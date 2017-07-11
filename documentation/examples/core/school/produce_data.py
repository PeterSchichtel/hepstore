#!/usr/bin/env python

# global imports
import numpy as np
import os


def produce( seed=7, nevents1=10000, nevents2=5000 ):
    
    # fix a random seed
    np.random.seed(seed)

    # generate data set I
    mean  = np.array([0.0,0.0])
    cov   = np.array([[8.0,0.0],[0.0,8.0]])
    data1 = np.random.multivariate_normal(
        mean, cov, nevents1 )
    
    # generate data set II
    mean  = np.array([2.5,-2.5])
    cov   = np.array([[1.0,0.0],[0.0,1.0]])
    data2 = np.random.multivariate_normal(mean, cov, nevents2)
    mean  = np.array([-1.4,0.8])
    cov   = np.array([[0.02,1.2],[-1.7,0.01]])
    data2 = np.concatenate(
        ( data2,
          np.random.multivariate_normal(
              mean, cov, nevents2) ) )

    # return data sets
    return (data1,data2)

def main( seed     = 7,
          nevents1 = 10000,
          nevents2 = 5000,
          name1    = "data_1.npy",
          name2    = "data_2.npy" ):

    data1,data2 = produce( seed, nevents1, nevents2 )

    np.save( name1, data1 )
    np.save( name2, data2 )

    pass

if __name__ == "__main__":
    main()
    pass




