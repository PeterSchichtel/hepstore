#!/usr/bin/env python

# global imports
import numpy as np
import os
import itertools

# hepstore imports
from hepstore.core.plotter import main as plot
from hepstore.core.physics.particle import *
from hepstore.core.physics.momentum import *

# local imports
import produce_data as produce

# fix random seed
np.random.seed(7)

# produce data set
produce.main( seed     = 7,
              nevents1 = 10000,
              nevents2 = 5000,
              name1    = "data_1.npy",
              name2    = "data_2.npy" )

# load data
d1 = np.load("data_1.npy")
d2 = np.load("data_2.npy")

# fix the incident energy
fixed_energy = 10.

# interpret d1 as jets
print "load jets"
jets = []
for (px,py) in d1:
    energy   = np.random.normal( fixed_energy, 0.2*fixed_energy )
    pid      = Pid( name = 'jet' )
    pz       = np.sqrt( energy**2 - px**2 - py**2 - pid.mass**2 )
    jets.append( Particle( pid=pid, energy=energy, px=px, py=py, pz=pz ) )
    pass

# interpret d2 as leptons
leptons = []
print "load leptons"
for (px,py) in d1:
    energy   = np.random.normal( fixed_energy/2., 0.05*fixed_energy/2. )
    pid      = Pid( name = 'electron' )
    pz       = np.sqrt( energy**2 - px**2 - py**2 - pid.mass**2 )
    leptons.append( Particle( pid=pid, energy=energy, px=px, py=py, pz=pz ) )
    pass

# generate invariant mass of all jet
jet_mass = []
print "compute jet mass"
count    = 0
for p1,p2 in itertools.combinations(jets,2):
    jet_mass.append( (p1+p2).mass() )
    count+=1
    if count%100000==0 :
        break
    pass
jet_mass = np.reshape( np.array( jet_mass ), (len(jet_mass),1) )
np.save("jet_mass.npy",jet_mass)

# respectively lepton pairs
lepton_mass = []
print "compute lepton mass"
count    = 0
for p1,p2 in itertools.combinations(leptons,2):
    lepton_mass.append( (p1+p2).mass() )
    count+=1
    if count%100000==0 :
        break
    pass
lepton_mass = np.reshape( np.array( lepton_mass ), (len(lepton_mass),1) )
np.save("lepton_mass.npy",lepton_mass)

# plot them
print "figure"
args = [
    '-f', 'jet_mass.npy', 'lepton_mass.npy',
    '-k', 'histogram',
    '-a', '0',
    '--normed',
    '--bins', '100',
    '-c', 'blue', 'red', 
    '--xmin', '0', '--xmax', '30', 
    '--ymax', '0.8', 
    '--xlabel', 'm',
    '--ylabel', r'$\rho(m)$',
    '--legend', 'jets', 'leptons',
    '--alpha', '0.6',
    '--title', 'particles', 'histogram in m',
    '--path', os.path.join(os.getcwd(),'mass.pdf'),
]
plot(args)
