#!/usr/bin/env python

# global imports
import numpy as np

# hepstore imports
from hepstore.core.utility          import *
from hepstore.core.physics.particle import *
from hepstore.core.physics.momentum import *


def fragment( mother ):
    particles = []
    for i in range( 0, mother.n_p+mother.n_n ):
        p = mother/mother.energy
        if i<mother.n_p:
            p.set_pid( 'proton' )
            pass
        else:
            p.set_pid( 'neutron' )
            pass
        p.add_on_shell_noise( width = 0.1 )
        particles.append( p )
        pass
    return particles


def remainder( mother, model='frac' ):
    if model == 'frac':
        particles = fragment( mother )
        for p in particles:
            if p.name == 'proton':
                incoming = p
                particles.remove(p)
                break
            pass
        return (incoming,particles)
    else:
        raise KeyError( "unknown model in remainder '%s' " % model )
    pass
