#!/usr/bin/env python

# global imports
import numpy as np

# local imports
from momentum import *

PID_DICT = {
    # 'name'      : [ pid , mass, n_protons, n_neutrons ],
    'proton'      : [ 2212, 1.0, 1, 0 ],
    'anti-proton' : [-2212, 1.0, 1, 0 ],
    'jet'         : [ None, 0.0, 0, 0 ],
    'electron'    : [ 12  , 0.000511, 0, 0 ],
}

# particle ids
class Pid(object):
    
    def __init__(self, name = 'proton' ):
        self.name = name
        self.pid, self.mass, self.n_p, self.n_n = PID_DICT[name]
        pass
    
    def __eq__( self, other ):
        answer = True
        answer = answer and (self.name == other.name)
        answer = answer and (self.pid  == other.pid )
        answer = answer and (self.mass == other.mass)
        answer = answer and (self.n_p  == other.n_p )
        answer = answer and (self.n_n  == other.n_n )
        return answer
    
    def __ne__(self, other):
        return not ( self == other )
    

    pass


class Particle(FourMomentum):

    def __init__( self,
                  energy   = 0.0,
                  px       = 0.0,
                  py       = 0.0,
                  pz       = 0.0,
                  pid      = Pid() ):
        FourMomentum.__init__( self, energy = energy,
                               px = px,
                               py = py,
                               pz = pz )
        self.pid = pid
        pass

    def __add__( self, other ):
        momentum = FourMomentum.__add__( self, other )
        return Particle( pid    = self.pid ,
                         energy = momentum.energy,
                         px     = momentum.px,
                         py     = momentum.py,
                         pz     = momentum.pz, )
        
    
    def __eq__( self, other ):
        answer = True
        answer = answer and (self.pid    == other.pid   )
        answer = answer and (self.energy == other.energy)
        answer = answer and (self.px     == other.px    )
        answer = answer and (self.py     == other.py    )
        answer = answer and (self.pz     == other.pz    )
        return answer
    
    def __ne__(self, other):
        return not ( self == other )
    

    pass

class Primary(Particle):

    def __init__( self,
                  energy = 1.0,
                  pid    = Pid() ):
        Particle.__init__( self, pid = pid,
                           energy = energy,
                           px     = 0.0,
                           py     = 0.0,
                           pz     = np.sqrt( ennergy**2 - pid.mass**2 )
        )
        pass

    pass
