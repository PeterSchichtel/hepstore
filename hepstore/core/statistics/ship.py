#!/usr/bin/env python

# globale imports
import numpy as np
from sklearn import preprocessing

# local imports
import fit


class Captain(object):

    def __init__( self, options ):
        self.options = options
        self.data    = None
        self.pdfs    = None
        pass

    def run( self ):

        # perform a fit on numeric pdfs
        if self.options.fit and self.options.pdf != [] :
            self.load_data()
            self.load_pdfs()
            parameters = fit.pdfs( self.data, self.pdfs, start=self.options.start )
            print parameters
            pass
        
        pass

    def load_data( self ):
        data = None
        # load data additive
        for path in self.options.data:
            if data == None:
                data = np.load(path)
                pass
            else:
                data = np.concatenate(
                    data,
                    np.load(path) )
                pass
            pass
        # do not normalise, only keep in entries
        self.data =  np.histogram( data[:,self.options.axis[0]],
                                   bins   = self.options.bins,
                                   range  = (-1,1),
                                   normed = False )[0]
        pass

    def load_pdfs( self ):
        self.pdfs = {}
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
            self.pdfs['coef%i' % i] = pdf
            pass
        pass
