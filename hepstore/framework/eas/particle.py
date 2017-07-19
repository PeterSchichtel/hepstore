#!/usr/bin/env python

# global imports
import numpy as np

# hepstore imports
from hepstore.core.physics.particle import *

# special eas particles
class Primary(Particle):

    def __init__( self,
                  energy = 1.0,
                  name   = 'proton',
                  zsign  = 1.0      ):
        Particle.__init__( self, name = name ,
                           energy = energy,
                           px     = 0.0,
                           py     = 0.0,
                           pz     = 0.0 )
        self.set_momentum( (self.energy, self.px, self.py, zsign*np.sqrt( self.energy**2 - self.mass**2 )) )
        pass

    pass
