#!/usr/bin/env python

# hepstore imports
from hepstore.core.error import *

#local imports
from particle import *

class Process(object):

    def __init__( self,
                  initial = ( Particle(), Particle() ),
                  final   = ( Particle(), Particle() ),
                  process = 'qcd' ):
        self.initial = initial
        self.final   = final
        self.mass    = (0.0,0.0)
        if   process == 'qcd':
            self.qcd = len(final)
            self.qed = 0
            self.bsm = 0
            pass
        elif process == 'qed':
            self.qcd = 0
            self.qed = len(final)
            self.bsm = 0
            pass
        else:
            raise ModelError("")
        pass

    def set_mass( self, mass ):
        self.mass = mass
        pass
    
    pass
