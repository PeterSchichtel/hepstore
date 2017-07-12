#!/usr/bin/env python

# globale imports
import numpy as np
from sklearn import preprocessing
import os

# hepstore imports
from hepstore.core.utility import *

# local imports
import fit
import limit
import significance


class Captain(object):

    def __init__( self, options ):
        self.options       = options
        self.bin_data      = None
        self.bin_pdfs      = None
        self.parameters    = None
        self.working_point = None
        pass

    def run( self ):

        # perform a fit on numeric pdfs
        if self.options.fit and self.options.pdf != [] :
            self.load_bin_data()
            self.load_bin_pdfs()
            self.parameters = fit.binned_pdfs( self.bin_data,
                                          self.bin_pdfs,
                                          start=self.options.start )
            for i,parameter in enumerate(self.parameters):
                print "--statistics: fitted %9.2e to pdf '%s' " % ( parameter, self.options.pdf[i] )
                pass
            pass

        # compute an upper bound from data
        if self.options.limit:
            self.working_point = limit.upper_bound(
                np.load( self.options.roc ),
                self.options.xsec_b,
                self.options.luminosity
            )
            xsec_s,es,eb = self.working_point
            print "--statistics: exclude cross sections above    xsec_s = %9.2e" % xsec_s
            print "--statistics: computed with L = %9.2e and xsec_b = %9.2e" % ( self.options.luminosity, self.options.xsec_b )
            print "--statistics: working point is  e_s = %9.2e, e_b = %9.2e" % ( es, eb )
            pass

        # compute poisonian significance as function
        # classifier output
        if self.options.significance != "":
            cls_distr_sig = np.load( self.options.cls_s )
            cls_distr_bkg = np.load( self.options.cls_b )
            significane,es,eb = significance.poisson(
                cls_distr_sig[:,self.options.axis[0]],
                cls_distr_bkg[:,self.options.axis[0]],
                self.options.xsec_s,
                self.options.xsec_b,
                self.options.luminosity,
                bins = self.options.bins,
            )
            mkdir( self.options.significance )
            np.save( os.path.join(
                self.options.significance,'significance.npy'),
                     significane )
            np.save( os.path.join(
                self.options.significance,'efficiency_s.npy'),
                     es )
            np.save( os.path.join(
                self.options.significance,'efficiency_b.npy'),
                     eb )
            pass
        
        pass

    def load_bin_data( self ):
        data = None
        # load data additive
        for path in self.options.data:
            if data == None:
                data  = np.load(path)
                pass
            else:
                data  = np.concatenate(
                    data,
                    np.load(path) )
                pass
            pass
        # do not normalise, only keep in entries
        self.bin_data = np.histogram( data[:,self.options.axis[0]],
                                      bins   = self.options.bins,
                                      range  = (-1,1),
                                      normed = False )[0]
        pass

    def load_bin_pdfs( self ):
        self.bin_pdfs = {}
        for i,path in enumerate(self.options.pdf):
            # load data
            data  = np.load(path)
            # create numerical pdf
            pdf   = np.histogram( data[:,self.options.axis[0]],
                                  bins   = self.options.bins,
                                  range  = (-1,1),
                                  normed = True )
            # normed includes bin width
            pdf = pdf[0]/sum(pdf[0])
            # save 
            self.bin_pdfs['coef%i' % i] = pdf
            pass
        pass
