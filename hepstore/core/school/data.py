#!/usr/bin/env python

# global imports
import numpy as np
import sklearn.model_selection

# data class wrapper containing
# features and labels
class DataUnit(object):

    # constructor
    def __init__( self,
                  data           = None,
                  classification = None ):
        self.data                = data
        self.classification      = classification
        pass

    # allow addition
    def __add__( self, other ):
        result = DataUnit()
        result.data              = np.concatenate((self.data,           other.data))
        result.classification    = np.concatenate((self.classification, other.classification))
        return result

    # interface to sklearn train test split
    def train_test_split( self,
                          test_size    = 0.25,
                          random_state = 0):
        return sklearn.model_selection.train_test_split(
            self.data, self.classification,
            test_size    = test_size,
            random_state = random_state )

    # zip through data feature,label
    def zip( self ):
        return zip( self.data.tolist(),
                    self.classification.tolist() )

    # transform data (log)
    def log_transform( self ):
        new_data  = []
        new_label = []
        for data,label in self.zip():
            if any( d<=0.0 for d in data ):
                continue
            new_data.append(data)
            new_label.append(label)
            pass
        self.data           = np.log( np.array(new_data) )
        self.classification = np.array( new_label )
        pass

    pass


