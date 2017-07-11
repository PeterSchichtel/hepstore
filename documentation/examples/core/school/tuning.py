#!/usr/bin/env python

# global imports
import numpy as np
import os

# hepstore imports
from hepstore.core.school import main as learn
from hepstore.core.plotter import main as plot
import produce_data as produce

# fix random seed
np.random.seed(7)

# produce data set
produce.main( seed     = 7,
              nevents1 = 10000,
              nevents2 = 5000,
              name1    = "data_1.npy",
              name2    = "data_2.npy" )

## tune quadratic linear discriminant
args = [
    "-c", "qda",
    "-f", os.path.join(os.getcwd(),"data_1.npy"),
    os.path.join(os.getcwd(),"data_2.npy"),
    "-l", "0.0", "1.0",
    "--only_explore",
    "--reg_param", "0.001",
    "--random_state", "7",
    "--path", os.path.join(os.getcwd(),"tuning"),
]
learn(args)

## which yields:
#--QDA: explore
#--info: RandomizedSearchCV took 2.72 seconds for 100 candidates parameter settings.
#--info: Model with rank: 1
#--info: Mean validation score:  8.12e-01 (std:  4.69e-03)
#--info: Parameters: {"reg_param": 0.011801565180308345, "tol": 2.6475644809055084e-09}
#--info: Model with rank: 1
#--info: Mean validation score:  8.12e-01 (std:  5.15e-03)
#--info: Parameters: {"reg_param": 0.01752128983692833, "tol": 0.000246259941676087}
#--info: Model with rank: 1
#--info: Mean validation score:  8.12e-01 (std:  4.57e-03)
#--info: Parameters: {"reg_param": 0.012059600364095596, "tol": 2.975620356682764e-10}

## plot cross validation
args = [
    "-f",
    os.path.join(os.getcwd(),"tuning","train_scores_reg_param.npy"),
    os.path.join(os.getcwd(),"tuning","test_scores_reg_param.npy"),
    os.path.join(os.getcwd(),"tuning","train_scores_tol.npy"),
    os.path.join(os.getcwd(),"tuning","test_scores_tol.npy"),
    "-k", "errorband",
    "--logx",
    "--legend", "train reg_parm",
    "test reg_param", "train tol", "test tol",
    "-c", "yellow", "blue ", "red", "green",
    "--title", "Cross validation QDA",
    "--ymax", "1.05",
    "--ymin", "0.55",
    "--xlabel", "parameter",
    "--ylabel", "score",
    "--path", os.path.join(os.getcwd(),"cross_validation.pdf"),
]
plot(args)

## plot learning curve
args = [
    "-f",
    os.path.join(os.getcwd(),"tuning","learning_curve_train.npy"),
    os.path.join(os.getcwd(),"tuning","learning_curve_test.npy"),
    "-k", "errorband",
    "--legend", "train", "test",
    "-c", "yellow", "blue ",
    "--xmin", "2500", "--xmax", "%s" % 23000,
    "--title", "Learning Curve QDA",
    "--ymax", "0.95",
    "--ymin", "0.65",
    "--xlabel", "sample size",
    "--ylabel", "score",
    "--path", os.path.join(os.getcwd(),"learning_curve.pdf"),
]
plot(args)

