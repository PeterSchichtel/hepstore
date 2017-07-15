#!/usr/bin/env python

# global imports
import os

# import runcard
import runcard

# h7 generator
class Generator(object):

    def __init__( self, options ):
        self.options = options
        self.seed    = options.seed
        self.folder  = os.getcwd()
        self.name    = 'herwig'
        pass
    
    def card( self ):
        fpath = os.path.join( self.path, self.name )
        name  = os.path.basename(fpath)
        with open( os.path.join("%s.in" % fpath), 'w' ) as fcard:
            runcard.collider( fcard )
            runcard.beams(    fcard, energy1   = self.options.energy, energy2 = 1.0 )
            runcard.model(    fcard )
            runcard.final(    fcard, particles = self.final )
            runcard.process(  fcard, process   = self.process )
            runcard.cuts(     fcard, process   = self.process )
            runcard.provider( fcard )
            runcard.scale(    fcard )
            runcard.shower(   fcard )
            runcard.pdf(      fcard )
            runcard.hepmc(    fcard )
            runcard.save(     fcard, name      = self.name )
            pass #with
        pass

    def run( self, path ):
        args           = os.path.normpath(path).split('/')
        self.path      = path
        self.energy    = float(args[0])
        self.element   = args[1]
        self.process   = args[2]
        self.generator = args[3]
        self.model     = args[4]
        self.final     = args[5]
        print "--h7: working on '%s'" % path
        # create directory
        mkdir( path )
        # create runcard
        print "--h7: runcard"
        self.card()
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
    
    pass
            
