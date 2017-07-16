#!/usr/bin/env python

# imports
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.ticker import FormatStrFormatter
import math,os,sys
from itertools import cycle
from hepstore.core.utility import *
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
        self.legend_fontsize = 12.
        self.title       = None
        self.title_fontsize       = 'medium'
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
        try:
            self.title_fontsize = options.title_fontsize[subnumber]
            pass
        except Exception:
            self.title_fontsize = 12.
            pass
        try:
            self.xaxis_fontsize = options.xaxis_fontsize[subnumber-1]
            pass
        except Exception:
            self.xaxis_fontsize = 12.
            pass
        try:
            self.yaxis_fontsize = options.yaxis_fontsize[subnumber-1]
            pass
        except Exception:
            self.yaxis_fontsize = 12
            pass
        try:
            self.zaxis_fontsize = options.zaxis_fontsize[subnumber-1]
            pass
        except Exception:
            self.zaxis_fontsize = 12.
            pass
        try:
            self.xlabel_fontsize = options.xlabel_fontsize[subnumber-1]
            pass
        except Exception:
            self.xlabel_fontsize = 12.
            pass
        try:
            self.ylabel_fontsize = options.ylabel_fontsize[subnumber-1]
            pass
        except Exception:
            self.ylabel_fontsize = 12
            pass
        try:
            self.zlabel_fontsize = options.zlabel_fontsize[subnumber-1]
            pass
        except Exception:
            self.zlabel_fontsize = 12.
            pass
        try:
            self.xticks = options.xticks[subnumber-1]
            pass
        except Exception:
            self.xticks = 4
            pass
        try:
            self.yticks = options.yticks[subnumber-1]
            pass
        except Exception:
            self.yticks = 4
            pass
        try:
            self.zticks = options.zticks[subnumber-1]
            pass
        except Exception:
            self.zticks = 4
            pass
        try:
            self.xticks_max = options.xticks_max[subnumber-1]
            pass
        except Exception:
            self.xticks_max = self.xmax
            pass
        try:
            self.yticks_max = options.yticks_max[subnumber-1]
            pass
        except Exception:
            self.yticks_max = self.ymax
            pass
        try:
            self.zticks_max = options.zticks_max[subnumber-1]
            pass
        except Exception:
            self.zticks_max = self.zmax
            pass
        try:
            self.xticks_min = options.xticks_min[subnumber-1]
            pass
        except Exception:
            self.xticks_min = self.xmin
            pass
        try:
            self.yticks_min = options.yticks_min[subnumber-1]
            pass
        except Exception:
            self.yticks_min = self.ymin
            pass
        try:
            self.zticks_min = options.zticks_min[subnumber-1]
            pass
        except Exception:
            self.zticks_min = self.zmin
            pass
        pass
        try:
            self.xaxis_format = options.xaxis_format[subnumber-1]
            pass
        except Exception:
            self.xaxis_format = None
            pass
        try:
            self.yaxis_format = options.yaxis_format[subnumber-1]
            pass
        except Exception:
            self.yaxis_format = None
            pass
        try:
            self.zaxis_format = options.zaxis_format[subnumber-1]
            pass
        except Exception:
            self.zaxis_format = None
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
            plt.title(self.title,fontsize=self.title_fontsize)
            pass
        subplot.set_xlabel(self.xlabel,fontsize=self.xlabel_fontsize)
        subplot.set_ylabel(self.ylabel,fontsize=self.ylabel_fontsize)
        for tick in subplot.xaxis.get_major_ticks():
            tick.label.set_fontsize(self.xaxis_fontsize)
            pass    
        for tick in subplot.yaxis.get_major_ticks():
            tick.label.set_fontsize(self.yaxis_fontsize)
            pass
        try:
            for tick in subplot.zaxis.get_major_ticks():
                tick.label.set_fontsize(self.zaxis_fontsize)
                pass
            pass
        except AttributeError:
            pass
        subplot.xaxis.set_major_formatter(FormatStrFormatter(self.xaxis_format))
        subplot.yaxis.set_major_formatter(FormatStrFormatter(self.yaxis_format))
        try:
            subplot.zaxis.set_major_formatter(FormatStrFormatter(self.zaxis_format))
            pass
        except AttributeError:
            pass
        plt.xticks( np.linspace( float(self.xticks_min), float(self.xticks_max), num=int(self.xticks) ) )
        plt.yticks( np.linspace( float(self.yticks_min), float(self.yticks_max), num=int(self.yticks) ) )
        try:
            plt.linspace( np.arange( float(self.zticks_min), float(self.zticks_max), num=int(self.zticks) ) )
            pass
        except AttributeError:
            pass
        subplot.set_xlim([float(self.xmin),float(self.xmax)])
        subplot.set_ylim([float(self.ymin),float(self.ymax)])
        try:
            subplot.set_zlabel(self.zlabel,fontsize=self.zlabel_fontsize)
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
        self.legends_fontsize= cycle(options_to_list(options.legend_fontsize))
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
            subplot.legend_fontsize     = float(next(self.legends_fontsize))
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
            self.figure.suptitle(self.options.title[0], fontsize=int(self.options.title_fontsize[0]))
            pass
        except IndexError:
            pass
        for subplot in self.subplots.values():
            subplot.finalize()
            pass
        print "--plotter: saving figure to %s" % self.options.path
        mkdir(os.path.dirname(self.options.path))
        plt.tight_layout()
        plt.subplots_adjust(top=0.85)
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
    parser.add_argument( "--legend", default=[None],
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
    parser.add_argument(      "--title", default=[],
                              help="figure title and subfigure titles as list",
                              nargs='+')
    parser.add_argument(      "--xlabel", default=[],
                              help="x axis label as list",
                              nargs='+')
    parser.add_argument(      "--ylabel", default=[],
                              help="y axis label as list",
                              nargs='+')
    parser.add_argument( "--title_fontsize", default=[12],
                         nargs='+')
    parser.add_argument( "--xlabel_fontsize", default=[12],
                         nargs='+')
    parser.add_argument( "--ylabel_fontsize", default=[12],
                         nargs='+')
    parser.add_argument( "--legend_fontsize", default=["1*12"],
                         nargs='+')
    parser.add_argument( "--xaxis_fontsize", default=[12],
                         nargs='+')
    parser.add_argument( "--yaxis_fontsize", default=[12],
                         nargs='+')
    parser.add_argument( "--zaxis_fontsize", default=[12],
                         nargs='+')
    parser.add_argument( "--xaxis_format", default=[r'%.2f'],
                         nargs='+')
    parser.add_argument( "--yaxis_format", default=[r'%.2f'],
                         nargs='+')
    parser.add_argument( "--zaxis_format", default=[r'%.2f'],
                         nargs='+')
    parser.add_argument( "--xticks", default=[],
                         nargs='+')
    parser.add_argument( "--yticks", default=[],
                         nargs='+')
    parser.add_argument( "--zticks", default=[],
                         nargs='+')
    parser.add_argument( "--xticks_max", default=[],
                         nargs='+')
    parser.add_argument( "--xticks_min", default=[],
                         nargs='+')
    parser.add_argument( "--yticks_max", default=[],
                         nargs='+')
    parser.add_argument( "--yticks_min", default=[],
                         nargs='+')
    parser.add_argument( "--zticks_max", default=[],
                         nargs='+')
    parser.add_argument( "--zticks_min", default=[],
                         nargs='+')

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
