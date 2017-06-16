#!/usr/bin/env python

from multiprocessing import Process, Pipe
import os


# contains worker classes for multiprocessing

class test(object):
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

class multipipeline(object):
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


def shower(num,pipe,options):
    filerror=False
    print "--shower[%i]: start subprocess" % num
    output_p, input_p = pipe
    ## load shower module
    app=shower.shower(num,options)
    while True:
        try:
            tfile    = output_p.recv()    # Read from the output pipe and do nothing
            if tfile=="DONE":
                print "--shower[%i]: leave subprocess" % num
                break
            pass
        except EOFError:
            break
        if not os.path.isfile(tfile):
            filerror=True
            break
        with open(tfile,'r') as fin:
            msg = fin.readline()
            fin.close()
            pass
        field  = msg.split(":")
        path   = field[0].split("=")[1]
        element= field[1].split("=")[1]
        energy = float(field[2].split("=")[1])
        files  = field[3].split("=")[1].split(";")
        print "--shower[%i]: %s %s %i" % (num,path,element,len(files))
        ## generate a run card for this shower
        card=runcard(path)
        card.corsika = options.corsika
        card.set_element(element)
        card.estart  = energy
        card.estop   = energy+options.erange
        ## run shower
        app.begin(card,options.nevents,files)
        app.run()
        app.convert()
        os.remove(tfile)
        pass #while
    if filerror:
        print "--error[%i]: file not found" % num
        pass
    # close pipes
    output_p.close()
    input_p.close()
    pass
