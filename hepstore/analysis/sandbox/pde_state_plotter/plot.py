#!/usr/bin/env python

# global imports
import numpy as np
import os

# hepstore imports
from hepstore.core.plotter import main as plot
import hepstore.core.plotter

# convert to correct npy
with open('SolutionGrid.dat','r') as fin:
    time = 0.0
    data = []
    for line in fin.readlines():
        values    = map(float, line.strip().split())
        time     += values[0]
        values[0] = time
        data.append(values)
        pass
    pass
data = np.array(data)
np.save('grid_data.npy',np.array(data))

# some data information
xmax = np.amax(data[:,1:])
xmin = np.amin(data[:,1:])
tmax = np.amax(data[:,0] )
tmin = np.amin(data[:,0] )
print "--info: t_min = %.2f, t_max = %.2f, x_min = %.2f, x_max = %.2f" % (tmin,tmax,xmin,xmax)
                            
## plot scatter
for dim in range(1,data.shape[1]):
    args = [
        '-f', 'grid_data.npy', 
        '-k', 'line',
        '-a', '0', '%i' % dim,
        '-c', 'blue',
        '--xmin', '0.01', '--xmax', '0.199',
        '--xticks', '5', '--xticks_min', '0.0', '--xticks_max', '0.2', 
        '--xaxis_fontsize', '18',
        '--xaxis_format', r'%.2f',
        '--ymin', '0.01', '--ymax', '0.99',
        '--yticks', '5', '--yticks_min', '0.0', '--yticks_max', '1.0', 
        '--yaxis_fontsize', '18',
        '--yaxis_format', r'%.2f',
#       '--legend', 'state: %i' % (dim-1),
        '-w', '2.0',
        '--alpha', '0.6',
        '--title', 'State: %i' % (dim-1), 
        '--title_fontsize', '27', 
        '--xlabel', 't',
        '--xlabel_fontsize', '18',
        '--ylabel', r'St$(x_{%i},t)$' % (dim-1) ,
        '--ylabel_fontsize', '18',
        '--path', os.path.join(os.getcwd(),'state_%04d.pdf' % (dim-1)),
    ]
    plot(args)
    hepstore.core.plotter.plt.close('all')
pass



