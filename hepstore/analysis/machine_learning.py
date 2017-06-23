#!/usr/bin/env python

import numpy as np
import os

from hepstore.school.parser  import SchoolParser
from hepstore.school.teacher import Teacher


def crossection_type(args):
    try:
        x, y = map(float, args.split(','))
        return (x, y)
    except:
        raise TypeError("--crossection must be x,y")
    pass

class MachineLearningParser(SchoolParser):

    def __init__(self,description="This app utilizes the hepstore.school to learn and analyse typical hep physics data"):
        super(SchoolParser,self).__init__(description=description)
        ## add functionality
        self.add_argument(      "--luminosity",               default=20000.,      type=float,            help="luminosity for analysis")
        self.add_argument(      "--crossection",              default=(1.0,0.5),   type=crossection_type, help="crossection for signal and background")
        self.add_argument(      "--ntotal",                   default=1000,        type=int,              help="number of total expected events")
        self.add_argument(      "--minimal_signal_efficieny", default=0.1,         type=float,            help="define a minimal signal efficiency for statistical analysis")
        pass

    pass

class Analysis(Teacher):

    def __init__(self,args=None):
        arg_parser = MachineLearningParser()
        # parse args
        parsed_args, unknown = arg_parser.parse_known_args(args)
        super(Teacher,self).__init__(parsed_args)
        pass

    def analyse(self):
        self.teach()
        self.save()
        pass

    def save(self):
        super(Analysis, self).save()
        # significance
        np.save(os.path.join(self.options.path,"significance.npy")   ,self.significance())
        # info on screen
        print self
        pass
    
    def significance(self,bins=1000):
        delta       = 1./float(bins) 
        counts_signal    , bin_edges_signal     = self.efficiency(self.options.signal_labels    ,bins=bins) 
        counts_background, bin_edges_background = self.efficiency(self.options.background_labels,bins=bins)
        # generate significance curve
        points = []
        for i in range(0,bins):
            es  = sum(counts_signal[:i]    )*delta
            eb  = sum(counts_background[:i])*delta
            if es>0.0 or eb>0.0:
                sig = np.sqrt( (self.options.luminosity * es**2 * self.options.crossection[0]**2 )/( es * self.options.crossection[0]  +  eb * self.options.crossection[1] ) )
                pass
            else:
                sig = 0.0
                pass
            points.append([es,sig])
            pass
        return np.array(points)

    
    def maximum_significance(self,bins=1000):
        sig   = max(      self.significance(bins=bins)[:,1])
        index = np.argmax(self.significance(bins=bins)[:,1])
        es    =           self.significance(bins=bins)[index,0]
        return (sig,es,index)
    
    def two_sigma_luminosity(self,bins=1000):
        max_s,max_es,index = self.maximum_significance(bins=bins)
        max_eb             = self.efficiency(self.options.background_labels,bins=bins)[0][index]
        return 4.0 * ( max_es * self.options.crossection[0]  +  max_eb * self.options.crossection[1] ) / ( max_es**2 * self.options.crossection[0]**2 )
    
    def excluded_crossection(self,bins=1000):
        def distance(above=True):
            if above:
                return self.maximum_significance(bins=bins)[0]>=2.0
            else:
                return self.maximum_significance(bins=bins)[0]<=2.0
            pass
        def factor(above=True):
            if above:
                return 0.9
            else:
                return 1.1
            pass
        # save signal cross section
        old_signal_crossection           = self.options.crossection
        # scan signal modifier to find maximum significance of 2
        above = self.maximum_significance(bins=bins)[0]>=2.0
        while distance(above):
            self.options.crossection     = ( factor(above)*self.options.crossection[0], self.options.crossection[1] )
            pass
        exclusion_limit                  = self.options.crossection[0]
        self.options.crossection         = old_signal_crossection
        return exclusion_limit
    
    def __str__(self):
        thestr = "--analysis:                    Z = %9.2e at        epsilon_s = %9.2e  \n" % self.maximum_significance()[0:2]
        thestr+= "--analysis:           luminosity = %9.2e pb^(-1) at        Z =  2.0   \n" % self.two_sigma_luminosity()
        thestr+= "--analysis: excluded above xsec  = %9.2e pb  with luminosity = %9.2e pb^(-1) and background = %9.2e pb " % (self.excluded_crossection(),self.options.luminosity,self.options.crossection[1])
        return thestr
    
    pass
 
