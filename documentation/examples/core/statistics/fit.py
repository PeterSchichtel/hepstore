#!/usr/bin/env python

# global imports
import numpy as np
import os

# hepstore imports
from hepstore.core.statistics import main as compute

args = [
    "--fit",
    "--data",
    os.path.join('..','school','working','blind_classifier_output.npy'),
    "--pdf",
    os.path.join('..','school','learning','classifier_distribution_train_0.0.npy'),
    os.path.join('..','school','learning','classifier_distribution_train_1.0.npy'),
    "--start", "100.0",
]
compute(args)
