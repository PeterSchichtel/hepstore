

class Card(object):

    def __init__(self,energy,process,final,path):
        self.energy  = energy
        self.process = process
        self.final   = final
        self.path    = path
        self.name    = 'herwig'
        pass

    def produce(self):
        if self.process == "qcd":
            with open(os.path.join(self.path,'%s.in' % self.name),'w') as fcard:
                fcard.write( "##################################################\n" )
                fcard.write( "## Collider type\n" )
                fcard.write( "read Matchbox/PPCollider.in\n" )
                fcard.write( "\n" )
                fcard.write( "##################################################\n" )
                fcard.write( "## Beam energy sqrt(s)\n" )
                fcard.write( "cd /Herwig/EventHandlers\n" )
                fcard.write( "set EventHandler:LuminosityFunction:Energy %f*GeV\n" % self.energy )
                fcard.write( "\n" )
                fcard.write( "##################################################\n" )
                fcard.write( "## Model assumptions\n" )
                fcard.write( "read Matchbox/StandardModelLike.in\n" )
                fcard.write( "read Matchbox/DiagonalCKM.in\n" )
                fcard.write( "## Set the order of the couplings\n" )
                fcard.write( "cd /Herwig/MatrixElements/Matchbox\n" )
                fcard.write( "set Factory:OrderInAlphaS 2\n" )
                fcard.write( "set Factory:OrderInAlphaEW 0\n" )
                fcard.write( "## Select the process\n" )
                fcard.write( "do Factory:Process p p -> %s\n" % self.final )
                fcard.write( "\n" )
                fcard.write( "##################################################\n" )
                fcard.write( "## Cut selection\n" )
                fcard.write( "read Matchbiox/DefaultPPJets.in\n" )
                fcard.write( "insert JetCuts:JetRegions 0 FirstJet\n" )
                fcard.write( "insert JetCuts:JetRegions 1 SecondJet\n" )
                fcard.write( "\n" )
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
                pass
            pass
        else:
            raise NotImplemented("unknown process '%s'" % self.process)
        pass

    pass
            
