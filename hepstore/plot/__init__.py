#!/usr/bin/env python

# run on  a server (ie no display)
import matplotlib
matplotlib.use('Agg')

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
from plotter import plotter as plotter

def make_contour(x,y,z):
    return [x,y,z]

def main():
    pass

if __name__ == "__main__":
    main()
    pass # main



'''
class plotter(object):
    def __init__(self,options=None):
        self.options = options
        self.figure  = plt.figure()
        pass
        
    def begin(self,config,options):
        self.options=options
        self.config={
            "name"      :"None",
            "xmin"      :"0.0",
            "xmax"      :"1.0",
            "ymin"      :"0.0",
            "ymax"      :"1.0",
            "fit"       :"None",
            "markersize":"4.0",
            "fontsize"  :"10.0",
            "title"     :"title",
            "xlabel"    :"X",
            "ylabel"    :"Y",
            "kind"      :"histogram",
        }
        self.lines=[]
        self.labels=[]
        for item in config.split(":"):
            words=item.split("=")
            self.config[words[0]]=words[1]
            pass
        print "--info: working on figure %s " % self.config["name"]
        plt.rcParams.update({'font.size': 4})
        plt.rcParams['legend.numpoints'] = 1
       # print options.color
        if options.color != []:
        #    print "nope"
            plt.rc( 'axes', prop_cycle=cycler('color', options.color) )
            self.cycle=cycle(options.color)
            pass
        else:
            self.cycle=None
            pass
        if options.line != []:
            self.lcycle=cycle(options.line)
            pass
        else:
            self.lcycle=None
            pass
        pass
    def load(self,path):
        print "--plot: adding %s" % path
        if self.config["kind"] == "histogram":
            self.histogram = histogram(self.config["name"])
            reader(path).read(self.histogram)
            pass
        elif self.config["kind"] == "unbinned":
            self.histogram = unbinned(self.config["name"])
            reader(path).read(self.histogram)
            pass
        else:
            raise Exception("unknown kind %s" % self.config["kind"])
        #print "--plot: adding %s" % path
        pass
    def plot(self,style,marker,label):
        ##print label
        sp = self.fig.add_subplot(1,1,1) 
        sp.set_ylim([ float(self.config["ymin"]),float(self.config["ymax"]) ])
        sp.set_xlim([ float(self.config["xmin"]),float(self.config["xmax"]) ]) 
        sp.set_xlabel(self.config["xlabel"], fontsize=int(1.5*float(self.config["fontsize"])))
        sp.set_ylabel(self.config["ylabel"], fontsize=int(1.5*float(self.config["fontsize"])))
        sp.xaxis.set_label_coords(1.0 , -0.05)
        sp.yaxis.set_label_coords(-0.08 , 1.0)
        # color
        if self.cycle==None:
            color=style['color']
            pass
        else:
            color=next(self.cycle)
            pass
        if self.lcycle==None:
            line=marker[1]
            pass
        else:
            line=next(self.lcycle).strip()
            pass
            pass
        if self.options.contour:
            try:
                x,y,z,xi,yi,zi,levels=self.histogram.contour(self.options.axis,self.options.level)
                #contour the gridded data, plotting dots at the nonuniform data points.
                CS = plt.contour(
                    xi, yi, zi, levels=levels, linewidths=0.8, 
                    colors=[color]
                )
                pass
            except Exception as err:
                print err
                raise err
            ##print label
            self.labels.append(label)
            try:
                for c in CS.collections:
                    c.set_linestyle(line)
                    pass
                #sp.clabel(CS, inline=0, fontsize=10)
                self.lines.append(CS.collections[0])
                pass
            except Exception as err:
                print err
                raise err
            pass
        else:
            legend = sp.legend(prop={'size':int(float(self.config["fontsize"]))},
                      loc='upper left',
                      bbox_to_anchor=(1.0025, 1.075),
                      ncol=1, #fancybox=True, shadow=True
                  )
            frame = legend.get_frame()
            frame.set_facecolor('white')
            frame.set_edgecolor('black')
            pass
        #print "--plot: plotted"
        pass
    def write(self,fout):
        for key in self.config:
            fout.write("%s=%s:" % (str(key),str(self.config[key])) )
            pass
    def save(self):
        ##print self.config["title"]
        if len(self.lines)>0:
            ##print self.labels
            legend = plt.legend(self.lines, self.labels,
                                prop={'size':int(float(self.config["fontsize"]))},
                                loc='upper left',
                                bbox_to_anchor=(1.0025, 1.075),
                                ncol=1, #fancybox=True, shadow=True,
                                frameon = 1,
                            )
            frame = legend.get_frame()
            frame.set_facecolor('white')
            frame.set_edgecolor('black')
            pass
        plt.title(r'%s' % self.config["title"], fontsize=int(1.5*float(self.config["fontsize"])) )
        plt.tick_params(axis='both', which='major', labelsize=int(float(self.config["fontsize"])))
        plt.tick_params(axis='both', which='minor', labelsize=int(0.8*float(self.config["fontsize"])))   
        plt.subplots_adjust(left=0.1, right=0.65, top=0.9, bottom=0.1)
        mkdir(self.figurepath)
        savepath = os.path.join(self.figurepath,self.config["name"])
        print "--info: saving figure to %s" % savepath
        tools.mkdir(self.figurepath)
        self.fig.savefig(savepath+"."+self.format, format=self.format, dpi=self.dpi)
        with open(savepath+".txt",'w') as fout:
            self.write(fout)
            fout.close()
            pass
        plt.close(self.fig)
        pass
    pass
'''
