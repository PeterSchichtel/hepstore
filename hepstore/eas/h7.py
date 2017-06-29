

import os

class Card(object):

    def __init__(self,energy,process,final,path):
        self.energy  = energy
        self.process = process
        self.final   = final
        self.path    = path
        self.name    = 'herwig'
        pass

    def produce(self):
        with open(os.path.join(self.path,'%s.in' % self.name),'w') as fcard:
            fcard.write( "##################################################\n" )
            fcard.write( "## Collider type\n" )
            fcard.write( "read Matchbox/PPCollider.in\n" )
            fcard.write( "\n" )
            fcard.write( "##################################################\n" )
            fcard.write( "## Beam energy sqrt(s)\n" )
            fcard.write( "cd /Herwig/EventHandlers\n" )
            fcard.write( "set EventHandler:LuminosityFunction:Energy %.2f*GeV\n" % (self.energy+1.0) )
            fcard.write( "set EventHandler:LuminosityFunction:BeamEMaxA  %.2f*GeV\n" % self.energy )
            fcard.write( "set EventHandler:LuminosityFunction:BeamEMaxB     1.0*GeV\n")
            fcard.write( "\n" )
            fcard.write( "##################################################\n" )
            fcard.write( "## Model assumptions\n" )
            fcard.write( "read Matchbox/StandardModelLike.in\n" )
            fcard.write( "read Matchbox/DiagonalCKM.in\n" )
            fcard.write( "## Set the order of the couplings\n" )
            fcard.write( "cd /Herwig/MatrixElements/Matchbox\n" )
            if self.process == "qcd":
                fcard.write( "set Factory:OrderInAlphaS 2\n" )
                fcard.write( "set Factory:OrderInAlphaEW 0\n" )
                fcard.write( "## Select the process\n" )
                fcard.write( "do Factory:Process p p -> %s\n" % self.final )
                fcard.write( "\n" )
                fcard.write( "##################################################\n" )
                fcard.write( "## Cut selection\n" )
                fcard.write( "read Matchbox/DefaultPPJets.in\n" )
                fcard.write( "insert JetCuts:JetRegions 0 FirstJet\n" )
                fcard.write( "insert JetCuts:JetRegions 1 SecondJet\n" )
                pass
            elif self.process == "zlo":
                raise NotImplemented("unknown process '%s'" % self.process)
                #pass
            else:
                raise NotImplemented("unknown process '%s'" % self.process)
            fcard.write( "\n" )
            fcard.write( "##################################################\n" )
            fcard.write( "##Matrix element provider\n" )
            fcard.write( "read Matchbox/MadGraph-MadGraph.in\n" )
            fcard.write( "##################################################\n" )
            fcard.write( "## Scale choice\n" )
            fcard.write( "cd /Herwig/MatrixElements/Matchbox/\n" )
            fcard.write( "set Factory:ScaleChoice /Herwig/MatrixElements/Matchbox/Scales/SHatScale\n" )
            fcard.write( "\n" )
            fcard.write( "##################################################\n" )
            fcard.write( "## Matching and shower selection\n" )
            fcard.write( "read Matchbox/LO-DefaultShower.in\n" )
            fcard.write( "\n" )
            fcard.write( "##################################################\n" )
            fcard.write( "## PDF choice\n" )
            fcard.write( "read Matchbox/FourFlavourScheme.in\n" )
            fcard.write( "read Matchbox/MMHT2014.in\n" )
            fcard.write( "\n" )
            fcard.write( "##################################################\n" )
            fcard.write( "## HepMC output\n" )
            fcard.write( "insert /Herwig/Generators/EventGenerator:AnalysisHandlers 0 /Herwig/Analysis/HepMCFile\n" )
            fcard.write( "set /Herwig/Analysis/HepMCFile:PrintEvent 10000\n" )
            fcard.write( "set /Herwig/Analysis/HepMCFile:Format GenEvent\n" )
            fcard.write( "set /Herwig/Analysis/HepMCFile:Units GeV_mm\n" )
            fcard.write( "\n" )
            fcard.write( "##################################################\n" )
            fcard.write( "## Save the generator\n" )
            fcard.write( "do /Herwig/MatrixElements/Matchbox/Factory:ProductionMode\n" )
            fcard.write( "cd /Herwig/Generators\n" )
            fcard.write( "saverun %s EventGenerator\n" % self.name)
            pass #with
        pass

    pass
            
