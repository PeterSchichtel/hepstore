#!/usr/bin/env python

# global imports
import numpy as np
from scipy.optimize import leastsq

# hepstore imports
from hepstore.core.error import *

# fit a sample of normed pdfs to some data
# result should be pdf weight with error
# covariance if possible
def binned_pdfs( data, pdfs, start=1.0 ):

    # we need one parameter per pdf
    parameters_initial = np.array( [start]*len(pdfs) )
    
    ###################################################
    # we need a function returning the weighted sum
    # of the pdfs
    def function( parameters ):
        for i,parameter in enumerate(parameters):
            if i == 0:
                result  = parameter * pdfs["coef%i" % i]
                pass
            else:
                result += parameter * pdfs["coef%i" % i]
                pass
            pass
        return result
    ###################################################

    # error function to minimise
    # needs to be one dimensional
    # parameter , x, data
    ErrorFunc = lambda p,y: function(p)-y

    # fit the function
    parameter_fit,success = leastsq(
        ErrorFunc, parameters_initial[:],
        args        = ( data ),
        full_output = False, )

    if success not in [ 1, 2, 3, 4, ]:
        raise FitError("unsuccessful %i" % success)

    return parameter_fit
