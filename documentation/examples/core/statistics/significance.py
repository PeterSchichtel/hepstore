#!/usr/bin/env python

# global imports
import numpy as np
import os

# hepstore imports
from hepstore.core.statistics import main as compute
from hepstore.core.plotter    import main as plot

args = [
    "--significance",
    os.path.join( os.getcwd(), 'significance'),
    "--cls_b",
    os.path.join('..','school','learning','classifier_distribution_train_0.0.npy'),
    "--cls_s",
    os.path.join('..','school','learning','classifier_distribution_train_1.0.npy'),
    "--xsec_s", "0.5",
    "--xsec_b", "10.0",
    "--luminosity", "100.0",
    "--bins", "1000",
]
compute(args)

# plot
args = [
    "-f",
    "significance/efficiency_b.npy",
    "significance/efficiency_s.npy",
    "significance/significance.npy",
    "-k", "line",
    "--legend", r"$\epsilon_B$", r"$\epsilon_S$", "significance",
    "--ymax", "3",
    "--path", os.path.join(os.getcwd(),"significance.pdf"),
    "--xlabel", "classifier",
]
plot(args)
