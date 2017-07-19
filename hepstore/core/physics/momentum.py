#!/usr/bin/env python

# global imports
import numpy as np


class FourMomentum(object):

    def __init__( self, *args, **kwargs):
        try:
            self.energy,self.px,self.py,self.pz = args[0]
            pass
        except IndexError:
            self.energy   = kwargs.get('energy',0.0)
            self.px       = kwargs.get('px'    ,0.0)
            self.py       = kwargs.get('py'    ,0.0)
            self.pz       = kwargs.get('pz'    ,0.0)
            pass
        self.momentum = ( self.energy, self.px, self.py, self.pz )
        pass

    def __div__( self, scalar ) :
        return FourMomentum( energy = self.energy/scalar,
                             px     = self.px/scalar,
                             py     = self.py/scalar,
                             pz     = self.pz/scalar  )

    def __mul__( self, other ):
        try: 
            return FourMomentum( energy = self.energy*other,
                                 px     = self.px*other,
                                 py     = self.py*other,
                                 pz     = self.pz*other  )
        except TypeError:
            return ( self.energy * other.energy -
                     self.px     * other.px     -
                     self.py     * other.py     -
                     self.pz     * other.pz )
        pass

    def __rmul__( self, other ):
        return self.__mul__( other )

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

    def set_momentum( self, momentum ) :
        self.energy,self.px,self.py,self.pz = momentum
        self.momentum = momentum
        pass
    
    def m2( self ):
        return self.energy**2 - self.px**2 -self.py**2 - self.pz**2

    def m( self ):
        return np.sqrt( self.m2() )

    def mass( self ):
        return self.m()

    def add_on_shell_noise( self, width = 0.05 ):
        self.energy,self.px,self.py = np.random.normal(
            loc   =         np.array( [self.energy, self.px, self.py] ),
            scale = width * np.array( [self.energy, self.px, self.py] ),
        )
        self.pz = np.sqrt( self.energy**2 - self.px**2 - self.py**2 - self.m2() )
        self.set_momentum( (self.energy,self.px,self.py,self.pz) )
        pass

    pass
