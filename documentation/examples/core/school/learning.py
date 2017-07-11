#!/usr/bin/env python

# global imports
import numpy as np
import os

# hepstore imports
from hepstore.core.school import main as learn
from hepstore.core.plotter import main as plot

# fix a random seed
np.random.seed(7)

# number of events
nevents = 5000

## perform the actuall machine learning
args = [
    "-c", "qda",
    "-f", os.path.join(os.getcwd(),"data_1.npy"),
    os.path.join(os.getcwd(),"data_2.npy"),
    "-l", "0.0", "1.0",
    "--reg_param", "0.0118",
    "--tol", "2.64e-9",
    "--random_state", "7",
    "--path", os.path.join(os.getcwd(),"learning"),
    "--save", os.path.join(os.getcwd(),"learning","qda.pkl"),
]
learn(args)

## ROC curve
args = [
    "-f", os.path.join(os.getcwd(),"learning","roc.npy"),
    "-k", "line",
    "--legend", "ROC",
    "-c", "blue",
    "--ymax", "1.1",
    "--title", "ROC curve QDA",
    "--xlabel", r"$\epsilon_{S}$",
    "--ylabel", r"$1-\epsilon_{B}$",
    "--path", os.path.join(os.getcwd(),"roc.pdf"),
]
plot(args)

## classifier output distribution
args = [
    "-f",
    os.path.join( os.getcwd(),
                  "learning",
                  "classifier_distribution_train_0.0.npy"),
    os.path.join( os.getcwd(),
                  "learning",
                  "classifier_distribution_test_0.0.npy"),
    os.path.join( os.getcwd(),
                  "learning",
                  "classifier_distribution_train_1.0.npy"),
    os.path.join( os.getcwd(),
                  "learning",
                  "classifier_distribution_test_1.0.npy"),
    "-k", "histogram", "errorbar",
    "-a", "1",
    "--bins", "20",
    "--normed",
    "--legend", "train background",
    "test background", "train signal", "test signal",
    "-c", "2*blue", "2*red",
    "--alpha", "0.6",
    "--xmin", "0.1", "--xmax", "1.1",
    "--ymin", "0.25", "--ymax", "11",
    "--title", "Classifier output QDA",
    "--xlabel", "classifier",
    "--ylabel", r"$\rho$(classifier)",
    "--path", os.path.join(os.getcwd(),"classifier_output.pdf"),
]
plot(args)

## probability map
args = [
    "-f", os.path.join(os.getcwd(),"data_1.npy"),
    os.path.join(os.getcwd(),"data_2.npy"),
    os.path.join(os.getcwd(),"learning","probability_map.npy"),
    "-a", "0", "1", "3",
    "-k", "2*scatter", "contour",
    "-c", "blue", "red", "Blues",
    "--xmin", "-5", "--ymin", "-5",
    "--xmax", "5", "--ymax", "5",
    "--alpha", "0.3",
    "--legend", "background", "signal",
    "--title", "probability map QDA",
    "--path", os.path.join(os.getcwd(),"probability_map.pdf"),
]
plot(args)
