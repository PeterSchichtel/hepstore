#!/usr/bin/env python

# global imports
import numpy as np

# compute the poissonian significance
# from 1D signal and background pdfs
def poisson( pdf_sig, pdf_bkg, xsec_s, xsec_b, luminosity,
             bins = 100 ):
    # binned normalized
    min_x        = min( np.amin(pdf_sig), np.amin(pdf_bkg) )
    max_x        = max( np.amax(pdf_sig), np.amax(pdf_bkg) )
    signal,edges = np.histogram( pdf_sig, bins = bins,
                           range=(min_x,max_x),
                           normed = True )
    signal       = signal/sum(signal)
    background,_ = np.histogram( pdf_bkg, bins = bins,
                           range=(min_x,max_x),
                           normed = True )
    background   = background/sum(background)
    # prepare results
    significance = []
    es           = []
    eb           = []
    # loop through data compute results
    int_s = 0.0
    int_b = 0.0
    for edge,s,b in zip( edges.tolist(), signal.tolist(), background.tolist() ):
        int_s += s
        int_b += b
        es.append( [ edge, 1.0 - int_s ] )
        eb.append( [ edge, 1.0 - int_b ] )
        z      = (
            (1.0 - int_s) * xsec_s * np.sqrt(luminosity)
        )/(
            np.sqrt( (1.0 - int_s) * xsec_s + (1.0-int_b) * xsec_b )
        )
        significance.append( [ edge, z ] )
        pass
    # return results
    return ( np.array(significance),
             np.array(es)          ,
             np.array(eb)          )
