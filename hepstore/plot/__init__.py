#!/usr/bin/env python

# run on  a server (ie no display)
#import matplotlib
#matplotlib.use('Agg')

# imports
import os
import plotter

def run():
    
    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to plot data saved from numpy arrays")

    # setup arg parser
    parser.add_argument("-f", "--file", default=[],
                        help="list of data files to be plotted (.npy format)",
                        required=True, nargs='+')
    # main option
    parser.add_argument("-k", "--kind", default=["1*histogram"],
                        help="cycle of kind of plot to be used, understands multiplication",
                        nargs='+',
                        type=str)
    parser.add_argument("-p", "--plot", default=["1*1"],
                        help="cycle of subplots to be used, understands multiplication",
                        nargs='+',
                        type=str)
    parser.add_argument("-c", "--color", default=['1*black'],
                        help="cycle of colors to be used for plotting, understands multiplication",
                        nargs='+',
                        type=str)
    parser.add_argument("-m", "--marker", default=['1*,'],
                        help="cycle of markers to be used for plotting, understands multiplication",
                        nargs='+',
                        type=str)
    parser.add_argument("-l", "--linestyle", default=['1*-'],
                        help="cycle of linestyles to be used for plotting, understands multiplication",
                        nargs='+',
                        type=str)
    parser.add_argument("-s", "--markersize", default=['1*1.0'],
                        help="cycle of markersizes to be used for plotting, understands multiplication",
                        nargs='+',
                        type=str)
    parser.add_argument("-w", "--linewidth", default=['1*1.0'],
                        help="cycle of linewidths to be used for contour, understands multiplication",
                        nargs='+',
                        type=str)
    parser.add_argument(      "--legend", default=['1*data'],
                        help="cycle of legends to be used for contour, understands multiplication",
                        nargs='+',
                        type=str)
    # further options
    parser.add_argument("-b", "--bins", default=100,
                        help="how many bins for histograms",
                        type=int)
    parser.add_argument("-n", "--normed", action="store_true",
                        help="normalize data before plotting")
    parser.add_argument("-a", "--axis", default=[0,1,2],
                        help="select axis of data to be plotted (x,y,z)",
                        nargs='+')
    parser.add_argument(      "--xmin", default=0.0,
                              help="x axes min")
    parser.add_argument(      "--ymin", default=0.0,
                             help="y axes min")
    parser.add_argument(      "--zmin", default=0.0,
                              help="z axes min")
    parser.add_argument(      "--xmax", default=1.0,
                              help="x axes max")
    parser.add_argument(      "--ymax", default=1.0,
                              help="y axes max")
    parser.add_argument(      "--zmax", default=1.0,
                              help="z axes max")
    parser.add_argument(      "--alpha", default=1.0,
                              help="alpha parameter for plt.plot",
                              type=float)
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
    
    # parse args   
    args = parser.parse_args()

    figure = plotter.figure(args)
    figure.plot()
    figure.save()
    
    pass #run


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
     
        with open(savepath+".txt",'w') as fout:
            self.write(fout)
            fout.close()
            pass
        pass
    pass
'''
