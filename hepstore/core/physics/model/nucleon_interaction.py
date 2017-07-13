#!/usr/bin/env python

# global imports
import numpy as np

# hepstore imports
from hepstore.core.tool             import *
from hepstore.core.physics.particle import *
from hepstore.core.physics.momentum import *


def fragment( self, mother ):
    # how many protons and neutrons
    # do we have
    n_p       = mother.pid[1]
    n_n       = mother.pid[2]
    # generate particles
    particles = []
    # protons
    for i in range(0,n_p):
        particles.append(
            Particle(
                momentum = ( mother.momentum / float(n_p+n_n)
                ).on_shell_noise( width = 0.05 ),
                pid      = PID['proton'] ))
        pass
    # neutrons
    for i in range(0,n_n):
        particles.append(
            Particle(
                momentum = ( mother.momentum / float(n_p+n_n)
                ).on_shell_noise( width = 0.05 ),
                pid      = PID['neutron'] ))
        pass
    # return particles
    return particles


