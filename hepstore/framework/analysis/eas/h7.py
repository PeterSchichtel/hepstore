#!/usr/bin/env python

import os
import hepstore.docker.herwig as herwig

import element,final`

def runcard(fpath,energy,process,final):
    name = os.path.basename(fpath)
    with open( os.path.join("%s.in" % fpath), 'w' ) as fcard:
        fcard.write( "##################################################\n" )
        fcard.write( "## Collider type                                  \n" )
        fcard.write( "read Matchbox/PPCollider.in                       \n" )
        fcard.write( "                                                  \n" )
        fcard.write( "##################################################\n" )
        fcard.write( "## Beam energy sqrt(s)                            \n" )
        fcard.write( "cd /Herwig/EventHandlers                          \n" )
        fcard.write( "set EventHandler:LuminosityFunction:Energy     %.2f*GeV\n" % (energy+1.0) )
        fcard.write( "set EventHandler:LuminosityFunction:BeamEMaxA  %.2f*GeV\n" %  energy      )
        fcard.write( "set EventHandler:LuminosityFunction:BeamEMaxB  1.0*GeV \n"                )
        fcard.write( "                                                  \n" )
        fcard.write( "##################################################\n" )
        fcard.write( "## Model assumptions                              \n" )
        fcard.write( "read Matchbox/StandardModelLike.in                \n" )
        fcard.write( "read Matchbox/DiagonalCKM.in                      \n" )
        fcard.write( "## Set the order of the couplings                 \n" )
        fcard.write( "cd /Herwig/MatrixElements/Matchbox                \n" )
        if process == "qcd":
            fcard.write( "set Factory:OrderInAlphaS 2                       \n" )
            fcard.write( "set Factory:OrderInAlphaEW 0                      \n" )
            fcard.write( "## Select the process                             \n" )
            fcard.write( "do Factory:Process p p -> %s                      \n" % final )
            fcard.write( "                                                  \n" )
            fcard.write( "##################################################\n" )
            fcard.write( "## Cut selection                                  \n" )
            fcard.write( "read Matchbox/DefaultPPJets.in                    \n" )
            fcard.write( "insert JetCuts:JetRegions 0 FirstJet              \n" )
            fcard.write( "insert JetCuts:JetRegions 1 SecondJet             \n" )
            pass
        elif process == "zlo":
            raise NotImplemented("unknown process '%s'" % process)
        #pass
        else:
            raise NotImplemented("unknown process '%s'" % process)
        fcard.write( "                                                  \n" )
        fcard.write( "##################################################\n" )
        fcard.write( "##Matrix element provider                         \n" )
        fcard.write( "read Matchbox/MadGraph-MadGraph.in                \n" )
        fcard.write( "##################################################\n" )
        fcard.write( "## Scale choice                                   \n" )
        fcard.write( "cd /Herwig/MatrixElements/Matchbox/               \n" )
        fcard.write( "set Factory:ScaleChoice /Herwig/MatrixElements/Matchbox/Scales/SHatScale\n" )
        fcard.write( "                                                  \n" )
        fcard.write( "##################################################\n" )
        fcard.write( "## Matching and shower selection                  \n" )
        fcard.write( "read Matchbox/LO-DefaultShower.in                 \n" )
        fcard.write( "                                                  \n" )
        fcard.write( "##################################################\n" )
        fcard.write( "## PDF choice                                     \n" )
        fcard.write( "read Matchbox/FourFlavourScheme.in                \n" )
        fcard.write( "read Matchbox/MMHT2014.in                         \n" )
        fcard.write( "                                                  \n" )
        fcard.write( "##################################################\n" )
        fcard.write( "## HepMC output                                   \n" )
        fcard.write( "insert /Herwig/Generators/EventGenerator:AnalysisHandlers 0 /Herwig/Analysis/HepMCFile\n" )
        fcard.write( "set /Herwig/Analysis/HepMCFile:PrintEvent 10000   \n" )
        fcard.write( "set /Herwig/Analysis/HepMCFile:Format GenEvent    \n" )
        fcard.write( "set /Herwig/Analysis/HepMCFile:Units GeV_mm       \n" )
        fcard.write( "                                                  \n" )
        fcard.write( "##################################################\n" )
        fcard.write( "## Save the generator                             \n" )
        fcard.write( "do /Herwig/MatrixElements/Matchbox/Factory:ProductionMode\n" )
        fcard.write( "cd /Herwig/Generators                             \n" )
        fcard.write( "saverun %s EventGenerator                         \n" % name)
        pass #with
    pass

class Generator(object):

    def __init__(self,options):
        self.options = options
        self.seed    = options.seed
        self.folder  = os.getcwd()
        self.name    = 'herwig'
        pass

    def run(self,path):
        args           = os.path.normpath(path).split('/')
        self.path      = path
        self.energy    = float(args[0])
        self.element   = element.Element(args[1])
        self.process   = args[2]
        self.generator = args[3]
        self.model     = args[4]
        self.final     = final.Final(args[5])
        print "--h7: working on '%s'" % path
        # create directory
        mkdir( path )
        # create runcard
        print "--h7: runcard"
        runcard( os.path.join(path,self.name), self.target_energy(), self.process, self.final.h7() )
        #build
        print "--h7: build"
        herwig.run([ '--directory', path,
                     'build'    , '%s.in'  % self.name, ])
        #integrate
        print "--h7: integrate"
        herwig.run([ '--directory', path,
                     'integrate', '%s.run' % self.name, ])
        # find a clean generation folder
        self.next()
        mkdir( os.path.join( path, self.folder))
        os.link( os.path.abspath( os.path.join(path,'Herwig-scratch') ),
                 os.path.abspath( os.path.join(path,self.folder,'Herwig-scratch') )
        )
        os.link( os.path.abspath( os.path.join(path,'%s.run' % self.name) ),
                 os.path.abspath( os.path.join(path,self.folder,'%s.run' % self.name) )
        )
        # run
        print "--h7: run"
        herwig.run([ '--directory', os.path.join(path,self.folder),
                     'run'      , '%s.run' % self.name, '-N', '%i' % self.options.nevents, '-s', '%i' % self.seed ])
        # return the path to the hepmc file
        return os.path.join( path, self.folder, '%s.hepmc' % self.name )

    def next(self):
        # use the given random seed
        if self.options.regenerate or not os.path.exists(os.path.join(self.path,'seeds.dat')):
            with open(os.path.join(self.path,'seeds.dat'),'w') as fout:
                fout.write("%i\n" % self.options.seed)
                pass
            self.seed = self.options.seed
        # generate a new random seed 
        else:
            count=1
            with open(os.path.join(self.path,'seeds.dat'),'r') as fin:
                while count in map(int, fin.readlines() ):
                    count+=1
                    pass
                pass
            with open(os.path.join(self.path,'seeds.dat'),'a') as fout:
                fout.write("%i\n" % count)
                pass
            self.seed = count
            pass
        # find a clean folder to run
        count=0
        while count in [ int(item.split("_")[-1]) for item in glob.glob(os.path.join(self.path,'run_*'))]:
            count+=1
            pass
        self.folder = "run_%i" % count
        pass

    def target_energy(self):
        return self.energy/self.element.nucleons
    
    pass
            
