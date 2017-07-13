#!/usr/bin/env python

# global imports
import numpy as np

# local imports
from momentum import *

PID_DICT = {
    # 'name'      : [ pid , mass, n_protons, n_neutrons ],
    'proton'      : [ 2212, 1.0, 1, 0 ],
    'anti-proton' : [-2212, 1.0, 1, 0 ],
}

# particle ids
class Pid(object):
    
    def __init__(self, name = 'proton' ):
        self.name = name
        self.pid, self.mass, self.n_p, self.n_n = PID_DICT[name]
        pass

    pass


class Particle(object):

    def __init__( self,
                  momentum = FourMomentum(),
                  pid      = Pid() ):
        self.momentum = momentum
        self.pid      = pid
        pass

    pass

class Primary(Particle):

    def __init__( self,
                  energy = 1.0,
                  pid    = Pid() ):
        Particle.__init__( self, pid = pid,
                           momentum  = FourMomentum(
                               energy = energy,
                               px     = 0.0,
                               py     = 0.0,
                               pz     = np.sqrt( ennergy**2 - pid.mass**2 )
                           ) )
        pass

    pass
