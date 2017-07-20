#!/usr/bin/env python

# global imports
import numpy as np
import copy

# local imports
from momentum import *

PID_DICT = {
    # 'name'      : [ pid , mass, n_protons, n_neutrons, corsika_id ],
    'photon'      : [   22, 0.0     , 0 , 0 , 1    ],
    'proton'      : [ 2212, 1.0     , 1 , 0 , 14   ],
    'anti-proton' : [-2212, 1.0     , 0 , 0 , 15   ],
    'neutron'     : [ 2211, 1.0     , 0 , 1 , 13   ],
    'anti-neutron': [-2211, 1.0     , 0 , 0 , 25   ],
    'lithium'     : [ None, 7.0     , 3 , 4 , 703  ],
    'carbon'      : [ None, 12.0    , 6 , 6 , 1206 ],
    'neon'        : [ None, 20.0    , 10, 10, 2010 ],
    'iron'        : [ None, 56.0    , 26, 30, 5626 ],
    'jet'         : [ None, 0.0     , 0 , 0 , None ],
    'electron'    : [ 12  , 0.000511, 0 , 0 , 3    ],
    'positron'    : [ -12 , 0.000511, 0 , 0 , 2    ],
}

# particle ids
class Pid(object):
    
    def __init__( self, *args, **kwargs):
        try:
            self.name = args[0]
            pass
        except IndexError:
            self.name = kwargs.get('name', 'proton')
            pass
        self.pid, self.mass, self.n_p, self.n_n, self.corsika = PID_DICT[self.name]
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

    def set_pid( self, name ):
        self.name = name
        self.pid, self.mass, self.n_p, self.n_n, self.corsika = PID_DICT[name]
        pass

    pass


class Particle(FourMomentum, Pid):

    def __init__( self, *args, **kwargs):
        try:
            self.momentum = FourMomentum( *args, **kwargs )
            self.pid      = Pid( *args, **kwargs )      
            pass
        except IndexError:
            energy        = kwargs.get('energy', 0.0)
            px            = kwargs.get('px'    , 0.0)
            py            = kwargs.get('py'    , 0.0)
            pz            = kwargs.get('pz'    , 0.0)
            name          = kwargs.get('name'  , 'proton' )
            self.momentum = FourMomentum( energy = energy,
                                         px = px, py = py, pz = pz )
            self.pid      = Pid( name = name )
            pass
        pass

    def __add__( self, other ):
        p = Particle( name = self.pid.name )
        p.momentum = self.momentum + other.momentum
        return p
        
    
    def __eq__( self, other ):
        answer = True
        answer = answer and self.momentum == other.momentum
        answer = answer and self.pid      == other.pid
        return answer
    
    def __ne__(self, other):
        return not ( self == other )

    def __div__( self, other ):
        p          = Particle( name = self.pid.name )
        p.momentum = self.momentum/other
        return p

    def __mul__( self, other ):
        p          = Particle( name = self.pid.name )
        mul        = self.momentum * other.momentum
        if isinstance(mul,float):
            return mul
        else:
            p.momentum = mul
            return p
        pass

    def __rmul__( self, other ):
        return self.__mul__( other )

    pass

