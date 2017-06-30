#!/usr/bin/env python

from multiprocessing import Process, Pipe
import os


# contains worker classes for multiprocessing

class Test(object):
    def __init__(self):
        self.pid = None
        pass
    def validate(self,data):
        if self.pid==None:
            self.pid = os.getpid()
            pass
        return True
    def run(self,data):
        if not self.validate(data):
            return False
        print self.pid
        return True
        pass
    pass

class Multipipeline(object):
    def __init__(self,app=None,args=None,job=1):
        #####################################
        # local worker
        def local_worker(app,pipe):
            output_p, input_p = pipe
            while True:
                data = output_p.recv()    # Read from the output pipe
                if data == "END":
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
            p = Process( target=local_worker,  args=(app(args),(output_p, input_p)) )
            p.start()
            self.processes.append([p, output_p, input_p])
            pass
        self.count = 0
        pass
    def send(self,data=None):
        self.processes[self.count%self.job][2].send(data)
        self.count+=1
        pass
    def close(self):
        for p in self.processes:
            p[2].send("END")
            p[1].close()
            p[2].close()
            p[0].join()
            pass
        pass


