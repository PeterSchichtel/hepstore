#!/usr/bin/env python

# global imports
import numpy as np
import os

# hepstore imports
from hepstore.core.plotter import main as plot
import produce_data as produce

# produce data set
produce.main( seed     = 7,
              nevents1 = 30000,
              nevents2 = 5000,
              name1    = "data_1.npy",
              name2    = "data_2.npy" )

## plot scatter
args = [
    '-f', 'data_1.npy', 'data_2.npy',
    '-k', 'scatter',
    '-c', 'blue', 'red', 
    '--xmin', '-5', '--xmax', '5', 
    '--ymin', '-5', '--ymax', '5', 
    '--legend', 'single gaussian', 'double gaussian',
    '--alpha', '0.6',
    '--title', 'example plot a', 'scatter',
    '--path', os.path.join(os.getcwd(),'example_a.pdf'),
]
plot(args)

## plot histogram of x axis
args = [
    '-f', 'data_1.npy', 'data_2.npy',
    '-k', 'histogram',
    '-a', '0',
    '--normed',
    '--bins', '20',
    '-c', 'blue', 'red', 
    '--xmin', '-5', '--xmax', '5', 
    '--ymax', '0.6', 
    '--xlabel', 'x',
    '--ylabel', r'$\rho(x)$',
    '--legend', 'single gaussian', 'double gaussian',
    '--alpha', '0.6',
    '--title', 'example plot b', 'histogram in x',
    '--path', os.path.join(os.getcwd(),'example_b.pdf'),
]
plot(args)

## plot histogram of y axis
args = [
    '-f', 'data_1.npy', 'data_2.npy',
    '-k', 'histogram',
    '-a', '1',
    '--normed',
    '--bins', '20',
    '-c', 'blue', 'red', 
    '--xmin', '-5', '--xmax', '5', 
    '--ymax', '0.6', 
    '--xlabel', 'y',
    '--ylabel', r'$\rho(y)$',
    '--legend', 'single gaussian', 'double gaussian',
    '--alpha', '0.6',
    '--title', 'example plot c', 'histogram in y',
    '--path', os.path.join(os.getcwd(),'example_c.pdf'),
]
plot(args)




