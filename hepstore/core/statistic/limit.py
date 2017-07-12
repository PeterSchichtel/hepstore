#!/usr/bin/env python

# global imports
import numpy as np

def upper_bound( roc_in, xsec_b, luminosity ):
    # only use non negative signal efficiencies
    roc_list = [
        [s,b] for s,b in zip( roc_in[:,0].tolist(),
                              roc_in[:,1].tolist() ) if s>0.0
    ]
    roc = np.array(roc_list)
    # compute all signal cross sections assuming Z=2
    xsec_s = 2.0 * (
        1.0 + np.sqrt( 1.0 + (1.0-roc[:,1]) * xsec_b * luminosity )
    ) / (
        roc[:,0] * luminosity
    )
    # find minimum
    index = np.argmin(xsec_s)
    return (xsec_s[index],roc[index,0],1.-roc[index,1])
