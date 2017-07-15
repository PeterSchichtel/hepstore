#!/usr/bin/env python

# global imports
import numpy as np


class FourMomentum(object):

    def __init__( self, energy=0.0, px=0.0, py=0.0, pz=0.0 ):
        self.energy = energy
        self.px     = px
        self.py     = py
        self.pz     = pz
        pass

    def __div__( self, scalar ) :
        return FourMomentum( energy = self.energy/scalar,
                             px     = self.px/scalar,
                             py     = self.py/scalar,
                             pz     = self.pz/scalar  )

    def __add__( self, other ):
        return FourMomentum( energy = self.energy + other.energy,
                             px     = self.px     + other.px ,
                             py     = self.py     + other.px ,
                             pz     = self.pz     + other.px  )
        
    
    def __eq__( self, other ):
        answer = True
        answer = answer and (self.energy == other.energy)
        answer = answer and (self.px     == other.px    )
        answer = answer and (self.py     == other.py    )
        answer = answer and (self.pz     == other.pz    )
        return answer
    
    def __ne__(self, other):
        return not ( self == other )
    
    def m2( self ):
        return self.energy**2 - self.px**2 -self.py**2 - self.pz**2

    def m( self ):
        return np.sqrt( self.m2() )

    def mass( self ):
        return self.m()

    def on_shell_noise( self, width = 0.05 ):
        e,px,py = np.random.normal(
            loc   =         np.array( [self.energy, self.px, self.py] ),
            scale = width * np.array( [self.energy, self.px, self.py] ),
        )
        pz = np.sqrt( e**2 - px**2 - py**2 - self.m2() )
        return FourMomentum( energy = e,
                             px     = px,
                             py     = py,
                             pz     = pz, )

    pass
