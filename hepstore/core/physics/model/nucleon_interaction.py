#!/usr/bin/env python

# global imports
import numpy as np

# hepstore imports
from hepstore.core.utility          import *
from hepstore.core.physics.particle import *
from hepstore.core.physics.momentum import *


def fragment( mother ):
    momentum = mother.momentum / float(mother.pid.n_p+mother.pid.n_n)
    particles = []
    for i in range( 0, mother.pid.n_p+mother.pid.n_n ):
        if i<mother.pid.n_p:
            p = Particle( name = 'proton' )
            pass
        else:
            p = Particle( name = 'neutron' )
            pass
        p.momentum = momentum.on_shell_noise( (0.5,0.5,0.5) )
        particles.append( p )
        pass
    return particles


def remainder( mother, model='frac' ):
    if model == 'frac':
        particles = fragment( mother )
        for p in particles:
            if p.pid.name == 'proton':
                incoming = p
                particles.remove(p)
                break
            pass
        return (incoming,particles)
    else:
        raise KeyError( "unknown model in remainder '%s' " % model )
    pass
