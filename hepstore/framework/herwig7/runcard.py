#!/usr/bin/enc python

# hepstore imports
from hepstore.core.physics.process  import Process
from hepstore.core.physics.particle import Particle
from hepstore.core.error import *

h7_dict = {
    'jet' : 'j',
}

def collider( fcard, collider='pp' ):
    fcard.write( "##################################################\n" )
    fcard.write( "## Collider type                                  \n" )
    if collider=='pp':
        fcard.write( "read Matchbox/PPCollider.in                   \n" )
        pass
    else:
        raise ColliderError("")
    fcard.write( "                                                  \n" )
    pass

def beams( fcard, energy1=7000., energy2=7000. ) :
    fcard.write( "##################################################\n" )
    fcard.write( "## Beam energy sqrt(s)                            \n" )
    fcard.write( "cd /Herwig/EventHandlers                          \n" )
    fcard.write( "set EventHandler:LuminosityFunction:Energy     %.2f*GeV\n" % (energy1+energy2) )
    fcard.write( "set EventHandler:LuminosityFunction:BeamEMaxA  %.2f*GeV\n" %  energy1   )
    fcard.write( "set EventHandler:LuminosityFunction:BeamEMaxB  %.2f*GeV\n" %  energy2   )
    fcard.write( "                                                  \n" )
    pass

def model( fcard, model='sm' ):
    fcard.write( "##################################################\n" )
    fcard.write( "## Model assumptions                              \n" )
    if model=='sm':
        fcard.write( "read Matchbox/StandardModelLike.in            \n" )
        fcard.write( "read Matchbox/DiagonalCKM.in                  \n" )
        pass
    else:
        raise ModelError("")
    fcard.write( "                                                  \n" )
    pass

def final( particles = (Particle(),Particle()) ):
    names = [ h7_dict[p.name] for p in particles ]
    return " ".join(names)

def process( fcard, process=Process() ):
    fcard.write( "## Set the order of the couplings                 \n" )
    fcard.write( "cd /Herwig/MatrixElements/Matchbox                \n" )
    fcard.write( "set Factory:OrderInAlphaS  %i                     \n" % process.qcd)
    fcard.write( "set Factory:OrderInAlphaEW %i                     \n" % process.qed)
    fcard.write( "## Select the process                             \n" )
    fcard.write( "do Factory:Process p p -> %s                      \n" % final( particles=process.final ) )
    fcard.write( "                                                  \n" )
    pass

def cuts( fcard, process=Process() ):
    fcard.write( "##################################################\n" )
    fcard.write( "## Cut selection                                  \n" )
    fcard.write( "cd /Herwig/Cuts/                                  \n" )
    if process.qcd>0:
        fcard.write( "read Matchbox/DefaultPPJets.in                \n" )
        fcard.write( "insert JetCuts:JetRegions 0 FirstJet          \n" )
        pass
    if process.qcd>1:
        fcard.write( "insert JetCuts:JetRegions 1 SecondJet         \n" )
        pass
    if process.qcd>2:
        fcard.write( "insert JetCuts:JetRegions 2 ThirdJet          \n" )
        pass
    if process.qcd>3:
        fcard.write( "insert JetCuts:JetRegions 3 FourthJet         \n" )
        pass
    if process.qed>1:
        fcard.write( "set /Herwig/Cuts/ChargedLeptonPairMassCut:MinMass %.2f*GeV\n" % process.mass[0] )
        fcard.write( "set /Herwig/Cuts/ChargedLeptonPairMassCut:MaxMass %.2f*GeV\n" % process.mass[1])
        pass
    fcard.write( "                                                  \n" )
    pass

def provider( fcard, provider='mg-mg' ):
    fcard.write( "##################################################\n" )
    fcard.write( "##Matrix element provider                         \n" )
    if provider == 'mg-mg':
        fcard.write( "read Matchbox/MadGraph-MadGraph.in            \n" )
        pass
    else:
        raise ProviderError()
    fcard.write( "                                                  \n" )
    pass

def scale( fcard, scale='shatscale' ):
    fcard.write( "##################################################\n" )
    fcard.write( "## Scale choice                                   \n" )
    fcard.write( "cd /Herwig/MatrixElements/Matchbox/               \n" )
    if scale == 'shatscale':
        fcard.write( "set Factory:ScaleChoice /Herwig/MatrixElements/Matchbox/Scales/SHatScale\n" )
        pass
    else:
        raise ScaleError("")
    fcard.write( "                                                  \n" )
    pass

def shower( fcard, shower='lo-default' ):
    fcard.write( "##################################################\n" )
    fcard.write( "## Matching and shower selection                  \n" )
    if shower == 'lo-default':
        fcard.write( "read Matchbox/LO-DefaultShower.in             \n" )
        pass
    else:
        raise ShowerError()
    fcard.write( "                                                  \n" )
    pass

def pdf( fcard, pdf='mmht2014', flavor=4 ):
    fcard.write( "##################################################\n" )
    fcard.write( "## PDF choice                                     \n" )
    if flavor == 4:
        fcard.write( "read Matchbox/FourFlavourScheme.in                \n" )
        pass
    else:
        raise FlavorError()
    if pdf == 'mmht2014':
        fcard.write( "read Matchbox/MMHT2014.in                         \n" )
        pass
    else:
        raise PdfError()
    fcard.write( "                                                  \n" )
    pass

def hepmc( fcard, nevents=10000 ):
    fcard.write( "##################################################\n" )
    fcard.write( "## HepMC output                                   \n" )
    fcard.write( "insert /Herwig/Generators/EventGenerator:AnalysisHandlers 0 /Herwig/Analysis/HepMCFile\n" )
    fcard.write( "set /Herwig/Analysis/HepMCFile:PrintEvent %i   \n"  % nevents )
    fcard.write( "set /Herwig/Analysis/HepMCFile:Format GenEvent    \n" )
    fcard.write( "set /Herwig/Analysis/HepMCFile:Units GeV_mm       \n" )
    fcard.write( "                                                  \n" )
    pass

def save( fcard, name ):
    fcard.write( "##################################################\n" )
    fcard.write( "## Save the generator                             \n" )
    fcard.write( "do /Herwig/MatrixElements/Matchbox/Factory:ProductionMode\n" )
    fcard.write( "cd /Herwig/Generators                             \n" )
    fcard.write( "saverun %s EventGenerator                         \n" % name)
    pass
