#!/usr/bin/env python

# imports 
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import math,os,sys
from itertools import cycle
from hepstore.tools import *
import numpy as np


class subplot(object):
    
    def __init__(self,options,subnumber):
        self.subnumber   = subnumber
        self.options     = options
        self.color       = None
        self.linestyle   = None
        self.marker      = None
        self.markersize  = None
        self.linewidth   = None
        self.legend      = None
        self.title       = None
        try:
            self.title = options.title[subnumber]
            pass
        except Exception:
            self.title = None
            pass
        try:
            self.xlabel = options.xlabel[subnumber-1]
            pass
        except Exception:
            self.xlabel = 'x'
            pass
        try:
            self.ylabel = options.ylabel[subnumber-1]
            pass
        except Exception:
            self.ylabel = 'y'
            pass
        try:
            self.zlabel = options.zlabel[subnumber-1]
            pass
        except Exception:
            self.zlabel = 'z'
            pass
        pass
    
    def plot(self,x,y):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber) 
        plt.plot(x,y,
                 label      = self.label,
                 color      = self.color,
                 #linestyel  = self.linestyle,
                 marker     = self.marker,
                 #markersize = self.markersize,
        )
        pass

    def range(self):
        return [(float(self.options.xmin),float(self.options.xmax)),
                (float(self.options.ymin),float(self.options.ymax)),
                (float(self.options.zmin),float(self.options.zmax))]
    
    def histogram(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber) 
        plt.hist(data,bins=self.options.bins,normed=self.options.normed,range=self.range()[0],alpha=self.options.alpha,color=self.color)
        pass

    def errorbar(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber) 
        counts,bin_edges = np.histogram(data,bins=self.options.bins,range=self.range()[0],normed=self.options.normed)
        bin_centres      = (bin_edges[:-1] + bin_edges[1:])/2.
        err              = np.sqrt(counts)
        plt.errorbar(bin_centres, counts, yerr=err, fmt='o', color=self.color())
        pass

    def contour(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber)
        z = data[:,self.options.axis[0]]
        x = data[:,self.options.axis[1]]
        y = data[:,self.options.axis[2]]
        triang = tri.Triangulation(x, y)
        plt.tricontourf(x,y,z,
                        cmap=self.color, #cm.Blues_r,
                        V=self.options.contour_levels, #[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95],
                        alpha=self.options.alpha,
        )
        pass
    
    def scatter(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber) 
        x=data[:,self.options.axis[0]]
        y=data[:,self.options.axis[1]]
        plt.scatter(x, y,
                    c=self.color,
                    marker=self.marker, s=self.markersize,
                    alpha=self.options.alpha,
                    label=self.legend)
        pass

    def line(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber)
        x=data[:,self.options.axis[0]]
        y=data[:,self.options.axis[1]]
        plt.plot(x,y,
                 linestyle=self.linestyle,linewidth=self.linewidth,
                 label=self.legend)
        pass
        

    def finalize(self):
        subplot = plt.subplot(self.options.rows,self.options.columns,self.subnumber)
        plt.legend()
        if self.title!=None:
            plt.title(self.title)
            pass
        subplot.set_xlim([float(self.options.xmin),float(self.options.xmax)])
        subplot.set_ylim([float(self.options.ymin),float(self.options.ymax)])
        subplot.set_xlabel(self.xlabel)
        subplot.set_ylabel(self.ylabel)
        try:
            subplot.set_zlabel(self.zlabel)
            pass
        except AttributeError:
            pass
        pass
    
    pass

class figure(object):

    def __init__(self,options):
        # save all options
        self.options     = options
        # capture top level figure opbject
        # create cyclers for options in plot
        self.kind            = cycle(options_to_list(options.kind))
        self.subplot         = cycle(options_to_list(options.plot))
        self.colors          = cycle(options_to_list(options.color))
        self.linestyles      = cycle(options_to_list(options.linestyle))
        self.markers         = cycle(options_to_list(options.marker))
        self.markersizes     = cycle(options_to_list(options.markersize))
        self.linewidths      = cycle(options_to_list(options.linewidth))
        self.legends         = cycle(options_to_list(options.legend))
        # create grid of subplots
        plt.subplots(options.rows,options.columns)
        # create corresponding subplots
        self.subplots        = {}
        for i in range(1,options.rows*options.columns+1):
            self.subplots[i] = subplot(options,i)
            pass
        self.figure          = plt.figure( figsize=options.figure_size, dpi=options.dpi, facecolor=None, edgecolor=None, linewidth=0.0, frameon=None, subplotpars=None, tight_layout=None)
        pass
    
    def plot(self):
        for fin in self.options.file:
            try:
                # load data from file
                data           = np.load(fin)
                pass
            except IOError:
                continue
            if self.options.shake:
                data = shake(data)
                pass
            # determine subplot, set atributes
            subplot            = self.subplots[int(next(self.subplot))]
            subplot.color      = next(self.colors)
            subplot.linestyle  = next(self.linestyles)
            subplot.marker     = next(self.markers)
            subplot.markersize = float(next(self.markersizes))
            subplot.linewidth  = float(next(self.linewidths))
            subplot.legend     = next(self.legends)
            # determine kind of plot
            kind               = next(self.kind)
            if   kind == "histogram":
                subplot.histogram(data)
                pass
            elif kind == "errorbar":
                subplot.errorbar(data)
                pass
            elif kind == "contour":
                subplot.contour(data)
                pass
            elif kind == "scatter":
                subplot.scatter(data)
                pass
            elif kind == "line":
                subplot.line(data)
                pass
            else:
                raise ValueError("unknown kind of plot '%s'" % kind)
            pass
        self.save()
        pass

    def save(self):
        try:
            self.figure.suptitle(self.options.title[0])
            pass
        except IndexError:
            pass
        for subplot in self.subplots.values():
            subplot.finalize()
            pass
        print "--info: saving figure to %s" % self.options.path
        mkdir(os.path.dirname(self.options.path))
        self.figure.savefig(self.options.path, format=self.options.format, dpi=self.options.dpi)
        plt.close(self.figure)
        pass

    pass
