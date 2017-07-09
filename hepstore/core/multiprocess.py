#!/usr/bin/env python

# global import
from multiprocessing import Process, Pipe
import os

# define our own pipe close (trouble with EOF)
PIPE_CLOSE = "END"

# managing several pipes in parrallel
class MultiPipe(object):

    # constructor
    def __init__( self,
                  app  = None,
                  args = None,
                  job  = 1 ):
        #####################################
        # local worker
        def local_worker( app, pipe ):
            output_p, input_p = pipe
            while True:
                data = output_p.recv()    # Read from the output pipe
                if data == PIPE_CLOSE:
                    break
                elif not app.run(data):
                    continue
                pass
            input_p.close()
            output_p.close()
            pass
        ######################################
        self.job       = job
        self.processes = []
        # fire up the processes
        for n in range(0,job):
            output_p, input_p = Pipe()
            p = Process(
                target = local_worker,
                args   = ( app(args), (output_p, input_p) )
            )
            p.start()
            self.processes.append( [p, output_p, input_p] )
            pass
        self.count = 0
        pass

    # send data to the next pipe (circular)
    def send( self,
              data = None ):
        self.processes[self.count%self.job][2].send(data)
        self.count+=1
        pass

    # close pipes and join processes
    def close(self):
        for p in self.processes:
            p[2].send(PIPE_CLOSE)
            p[1].close()
            p[2].close()
            p[0].join()
            pass
        pass

    pass #MultiPipe
