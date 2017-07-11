#!/usr/bin/env python

# imports 
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import math,os,sys
from itertools import cycle
from hepstore.core.tools import *
import numpy as np


class SubPlot(object):
    
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
        self.xmin        = 0.
        self.xmax        = 1.
        self.ymin        = 0.
        self.ymax        = 1.
        self.zmin        = 0.
        self.zmax        = 1.
        self.alpha       = 1.
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
    
    def histogram(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber) 
        plt.hist( data[:,self.options.axis[0]],
                  bins   = self.options.bins,
                  normed = self.options.normed,
                  range  = (float(self.xmin),float(self.xmax)),
                  alpha  = self.alpha,
                  color  = self.color,
                  label  = self.legend)
        pass

    def errorbar(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber)
        counts,bin_edges = np.histogram(data[:,self.options.axis[0]],
                                        bins   = self.options.bins,
                                        range  = (float(self.xmin),float(self.xmax)),
                                        normed = self.options.normed)
        bin_centres      = (bin_edges[:-1] + bin_edges[1:])/2.
        err              = np.sqrt(counts)
        if self.options.normed:
            err /= np.sqrt( float(len( data[:,self.options.axis[0]] )) )
            pass
        plt.errorbar( bin_centres, counts,
                      yerr  = err,
                      fmt   = 'o',
                      alpha = self.alpha,
                      color = self.color,
                      label = self.legend)
        pass

    def contour(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber)
        x = data[:,self.options.axis[0]]
        y = data[:,self.options.axis[1]]
        z = data[:,self.options.axis[2]]
        triang = tri.Triangulation(x, y)
        plt.tricontourf(x,y,z,
                        cmap=self.color, #cm.Blues_r,
                        V=self.options.contour_levels, #[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95],
                        alpha=self.alpha,
        )
        pass
    
    def scatter(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber) 
        x=data[:,self.options.axis[0]]
        y=data[:,self.options.axis[1]]
        plt.scatter(x, y,
                    c=self.color,
                    marker=self.marker, s=self.markersize,
                    alpha=self.alpha,
                    label=self.legend)
        pass

    def line(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber)
        x=data[:,self.options.axis[0]]
        y=data[:,self.options.axis[1]]
        if self.options.logx and self.options.logy:
            plt.loglog(x, y, 
                       linestyle=self.linestyle,linewidth=self.linewidth,
                       label=self.legend)
            pass
        elif self.options.logx:
            plt.semilogx(x, y, 
                       linestyle=self.linestyle,linewidth=self.linewidth,
                       label=self.legend)
            pass
        elif self.options.logy:
            plt.semilogy(x, y, 
                       linestyle=self.linestyle,linewidth=self.linewidth,
                       label=self.legend)
            pass
        else:
            plt.plot(x,y,
                     linestyle=self.linestyle,linewidth=self.linewidth,
                     label=self.legend)
            pass
        pass

    def errorband(self,data):
        plt.subplot(self.options.rows,self.options.columns,self.subnumber)
        x = data[:,self.options.axis[0]]
        y = data[:,self.options.axis[1]]
        try:
            dyp = data[:,self.options.axis[2]]
            dym = data[:,self.options.axis[3]]
            pass
        except IndexError:
            dyp = data[:,self.options.axis[2]]
            dym = dyp
            pass
        if self.options.logx and self.options.logy:
            plt.loglog(x, y, 
                       linestyle=self.linestyle,linewidth=self.linewidth,
                       label=self.legend)
            pass
        elif self.options.logx:
            plt.semilogx(x, y, 
                       linestyle=self.linestyle,linewidth=self.linewidth,
                       label=self.legend)
            pass
        elif self.options.logy:
            plt.semilogy(x, y, 
                       linestyle=self.linestyle,linewidth=self.linewidth,
                       label=self.legend)
            pass
        else:
            plt.plot(x,y,
                     linestyle=self.linestyle,linewidth=self.linewidth,
                     label=self.legend)
            pass
        plt.fill_between(x, y-dym, y+dyp,
                         linestyle=self.linestyle,linewidth=self.linewidth,
                         alpha=0.3*self.alpha,)
        pass
        
    def finalize(self):
        subplot = plt.subplot(self.options.rows,self.options.columns,self.subnumber)
        plt.legend()
        if self.title!=None:
            plt.title(self.title)
            pass
        subplot.set_xlim([float(self.xmin),float(self.xmax)])
        subplot.set_ylim([float(self.ymin),float(self.ymax)])
        subplot.set_xlabel(self.xlabel)
        subplot.set_ylabel(self.ylabel)
        try:
            subplot.set_zlabel(self.zlabel)
            pass
        except AttributeError:
            pass
        pass
    
    pass

class Figure(object):

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
        self.xmins           = cycle(options_to_list(options.xmin))
        self.xmaxs           = cycle(options_to_list(options.xmax))
        self.ymins           = cycle(options_to_list(options.ymin))
        self.ymaxs           = cycle(options_to_list(options.ymax))
        self.zmins           = cycle(options_to_list(options.zmin))
        self.zmaxs           = cycle(options_to_list(options.zmax))
        self.alphas          = cycle(options_to_list(options.alpha))
        # create grid of subplots
        plt.subplots(options.rows,options.columns)
        # create corresponding subplots
        self.subplots        = {}
        for i in range(1,options.rows*options.columns+1):
            self.subplots[i] = SubPlot(options,i)
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
            subplot.xmin       = next(self.xmins)
            subplot.xmax       = next(self.xmaxs)
            subplot.ymin       = next(self.ymins)
            subplot.ymax       = next(self.ymaxs)
            subplot.zmin       = next(self.zmins)
            subplot.zmax       = next(self.zmaxs)
            subplot.alpha      = float(next(self.alphas))
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
            elif kind == "errorband":
                subplot.errorband(data)
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
        print "--plotter: saving figure to %s" % self.options.path
        mkdir(os.path.dirname(self.options.path))
        self.figure.savefig(self.options.path, format=self.options.format, dpi=self.options.dpi)
        plt.close(self.figure)
        pass

    pass


def main(args=None):
    
    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to plot data saved from numpy arrays")

    # setup arg parser
    parser.add_argument( "-f", "--file", default=[],
                        help     = "list of data files to be plotted (.npy format)",
                        required = True,
                        nargs    = '+')
    # main option
    parser.add_argument( "-k", "--kind", default=["1*histogram"],
                         help  = "cycle of kind of plot to be used, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "-p", "--plot", default=["1*1"],
                        help  = "cycle of subplots to be used, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "-c", "--color", default=['1*black'],
                         help  = "cycle of colors to be used for plotting, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "-m", "--marker", default=['1*,'],
                         help  = "cycle of markers to be used for plotting, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "-l", "--linestyle", default=['1*-'],
                         help  = "cycle of linestyles to be used for plotting, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "-s", "--markersize", default=['1*1.0'],
                         help  = "cycle of markersizes to be used for plotting, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "-w", "--linewidth", default=['1*1.0'],
                         help  = "cycle of linewidths to be used for contour, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "--legend", default=['1*data'],
                         help  = "cycle of legends to be used for contour, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "--xmin", default=['1*0.0'],
                         help  = "cycle of xmins, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "--xmax", default=['1*1.0'],
                         help  = "cycle of xmaxs, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "--ymin", default=['1*0.0'],
                         help  = "cycle of ymins, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "--ymax", default=['1*1.0'],
                         help  = "cycle of ymaxs, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "--zmin", default=['1*0.0'],
                         help  = "cycle of zmins, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "--zmax", default=['1*1.0'],
                         help  = "cycle of zmaxs, understands multiplication",
                         nargs = '+',
                         type  = str)
    parser.add_argument( "--alpha", default=['1*1.0'],
                         help  = "alpha parameter for plt.plot, understand multiplication",
                         nargs = '+',
                         type  = str)

    # further options
    parser.add_argument( "-b", "--bins", default=100,
                        help="how many bins for histograms",
                        type=int)
    parser.add_argument( "-n", "--normed", action="store_true",
                        help="normalize data before plotting")
    parser.add_argument( "-a", "--axis", default=[0,1,2],
                        type  = int,
                        help  = "select axis of data to be plotted (x,y,z)",
                        nargs = '+')
    parser.add_argument(      "--contour_levels", default=[],
                              help="levelsfor contour plot",
                              nargs='+')
    parser.add_argument(      "--figure_size", default=(6.2,6.2),
                              help="figure size",
                              type=tuple)
    parser.add_argument(      "--dpi", default=300,
                              help="dpi for plot")
    parser.add_argument(      "--format", default="pdf")
    parser.add_argument(      "--path", default=os.path.join(os.getcwd(),'figure.pdf'),
                              help="path and name of the file to save figure")
    parser.add_argument(      "--rows", default=1,
                              help="how many rows of plots")
    parser.add_argument(      "--columns", default=1,
                              help="how many columns of plots")
    parser.add_argument(      "--title", default=[],
                              help="figure title and subfigure titles as list",
                              nargs='+')
    parser.add_argument(      "--xlabel", default=[],
                              help="x axis label as list",
                              nargs='+')
    parser.add_argument(      "--ylabel", default=[],
                              help="y axis label as list",
                              nargs='+')
    parser.add_argument(      "--shake", action='store_true',
                              help="shake data")
    parser.add_argument(      "--logx", action="store_true")
    parser.add_argument(      "--logy", action="store_true")
    
    # parse args   
    parsed_args = parser.parse_args(args)

    # plot figures
    figure = Figure(parsed_args)
    figure.plot()
    
    pass #main


if __name__ == "__main__":
    main()
    pass
