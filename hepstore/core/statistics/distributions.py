#!/usr/bin/env python

import numpy as np
import os

# Utility class for flat log_10 random
class Log10Flat(object):

    def __init__(self,start=0,stop=1):
        self.start = start
        self.stop  = stop
        pass

    def rvs(self, loc=0, scale=1, size=1, random_state=None):
        if size==1:
            return 10**(np.random.uniform(low=self.start,high=self.stop))
        else:
            return 10**(np.random.uniform(low=self.start,high=self.stop,size=size))
        pass
    
    pass

