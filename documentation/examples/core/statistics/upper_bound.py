#!/usr/bin/env python

# global imports
import numpy as np
import os

# hepstore imports
from hepstore.core.statistics import main as compute

args = [
    "--limit",
    "--roc",
    os.path.join('..','school','learning','roc.npy'),
    "--xsec_b", "10.0",
    "--luminosity", "100.0",
]
compute(args)
