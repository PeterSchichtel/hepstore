#!/usr/bin/env python

# imports 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math,os,sys
import scipy.optimize as opt
from matplotlib.mlab import griddata
from cycler import cycler
from itertools import cycle
import ..tools
import numpy as np

class plotter(object):
    def __init__(self):
        pass

    def setup(self,options):
        self.options     = options
        self.figure      = plt.figure() #figsize=None, dpi=None, facecolor=None, edgecolor=None, linewidth=0.0, frameon=None, subplotpars=None, tight_layout=None)
        self.colors      = iter(options.color)
        self.styles      = iter(options.style)
        self.markers     = iter(options.marker)
        self.markersizes = iter(options.markersize)
        pass

    def color(self):
        return 'red'

    def linestyle(self):
        return '-'

    def marker(self):
        return 'o'

    def markersize(self):
        return 1.0
    
    def plot(x,y):
        plt.plot(x,y,
                 label      = self.options.label,
                 color      = self.color(),
                 linestyel  = self.linestyle(),
                 marker     = self.marker(),
                 markersize = self.markersize(),
        )
        pass
    
    def histogram(data):
        plt.hist(data,bins=self.options.bins,normed=self.options.normed,range=self.options.range,alpha=self.options.alpha,color=self.color())
        pass

    def errorbar(data,error=1.0):
        counts,bin_edges = np.histogram(data,bins=self.options.bins,range=self.options.range,normed=self.options.normed)
        bin_centres      = (bin_edges[:-1] + bin_edges[1:])/2.
        err              = error*np.sqrt(counts)
        plt.errorbar(bin_centres, counts, yerr=err, fmt='o', color=self.color())
        pass

    def contour(self,data):
        x,y,z = data
        plt.contour(x, y, z, levels=self.options.levels, linewidths=0.8, colors=self.color())
        pass
    
    def scatter(data):
        x=data[:,self.options.axis[0]]
        y=data[:,self.options.axis[1]]
        self.plot(x,y)
        pass

    def save(self):
        pass

    pass
