#!/usr/bin/env python

# global imports
import os

# hepstore imports
from hepstore.core.plotter import main as plot
from hepstore.core.school import main as school
from hepstore.framework.eas import main as eas

## generate / shower / observabls
nevents    = 250
args       = [
    '-d', os.path.join( os.getcwd(), 'data' ),
    '-E', '1.0e+06',
    '-e', 'proton', 'lithium', 'carbon', 'neon', 'iron',
    '-p', 'qcd',
    '-g', 'h7', 'corsika',
    '-f', 'dijet',
    '-m', 'frac',
    '-N', '%i' % nevents,
    '-j', '1',
    '-G', '-L',
    ]
eas(args)

## plot data

## learn from data

## classify some pseudo data

## statistical analysis
