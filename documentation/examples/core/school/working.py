#!/usr/bin/env python

# global imports
import numpy as np
import os

# hepstore imports
from hepstore.core.school import main as learn
from hepstore.core.plotter import main as plot
import produce_data as produce

# fix random seed
np.random.seed(56)

# produce data set
produce.main( seed     = 56,
              nevents1 = 10000,
              nevents2 = 250,
              name1    = "data_3.npy",
              name2    = "data_4.npy" )

## load classifier and classify
args = [
    "--load", os.path.join(os.getcwd(),"learning","qda.pkl"),
    "-f", os.path.join(os.getcwd(),"data_3.npy"),
    os.path.join(os.getcwd(),"data_4.npy"),
    "-l", "0.0", "1.0",
    "--path", os.path.join(os.getcwd(),"working"),
]
learn(args)

## plot blind output
args = [
    "-f",
    os.path.join( os.getcwd(),
                  "working","blind_classifier_output.npy"),
    "-k", "histogram",
    "-a", "1",
    "--bins", "20",
    "--legend", "blinded data",
    "-c", "green",
    "--alpha", "0.6",
    "--xmin", "-0.1", "--xmax", "1.1",
    "--ymax", "%i" % 3500,
    "--title", "QDA",
    "--xlabel", "classifier",
    "--ylabel", "N",
    "--path", os.path.join(os.getcwd(),"blind_distribution.pdf"),
]
plot(args)
