#!/usr/bin/env python

# global imports
import numpy as np

# hepstore imports
from hepstore.core.physics.particle import *

# special eas particles
class Primary(Particle):

    def __init__( self, energy = 1.0, name = 'proton', zsign = 1.0 ):
        mass = Pid( name = name ).mass
        pz   = zsign * np.sqrt( energy**2 - mass**2 )
        Particle.__init__( self, name = name , energy = energy, pz = pz )
        pass

    pass
