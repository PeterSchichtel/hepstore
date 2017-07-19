#!/usr/bin/env python

# global imports
import os
from multiprocessing import Process, Pipe
import docker

# definitions
PIPE_CLOSE = "END"
job = 2

##########################################################################
def one_docker_run():
    ## arguments
    IMAGE = 'peterschichtel/herwig'
    TAG   = '7.0.4'
    args  = [ '/bin/bash',
              '-c',
              'source $ACTIVATE && Herwig build herwig.in',
    ]
    containername = '%s:%s' % ( IMAGE, TAG )
    # get docker client
    client        = docker.from_env()
    # check if docker image exist otherwise try to pull
    if not len( client.images.list( name = IMAGE ) )>0:
        print '--%s: pull image' % IMAGE
        client.images.pull( IMAGE, tag = TAG )
        pass
    # see if there is a directory to be mounted from host machine
    try:
        folder    = os.getcwd()
        volume    = {folder: {'bind': '/UserVolume', 'mode': 'rw'}}
        pass
    except Exception:
        volume    = {}
        pass
    # run the command on the container
    container = client.containers.run( containername,
                                       command     = args,
                                       volumes     = volume,
                                       working_dir = '/UserVolume',
                                       detach      = True )
    # print the container output on screen
    for i,line in enumerate(
            container.logs( stdout=True, stderr=True, stream=True) ):
        print '%i: %s' % (i,line.strip())
        pass
    # remove container
    container.remove()
    pass
##########################################################################


##########################################################################
def multi_docker_run():
    ######################################
    # local worker
    def local_worker( output_p, input_p ):
        print "--worker[%i]" % os.getpid()
        while True:
            data = output_p.recv()    # Read from the output pipe
            if data == PIPE_CLOSE:
                break
            else:
                print "--worker[%i]: one" % os.getpid()
                one_docker_run()
                pass
            pass
        input_p.close()
        output_p.close()
        pass
    #####################################

    # fire up the processes
    processes = []
    for n in range(0,job):
        output_p, input_p = Pipe()
        p = Process(
            target = local_worker,
            args   = ( output_p, input_p )
        )
        p.start()
        processes.append( [p, output_p, input_p] )
        pass
    
    # send data to the next pipe (circular)
    data = 'hello'
    for n in range(0,4):
        processes[n%job][2].send(data)
        pass
    
    # close pipes and join processes
    for p in processes:
        p[2].send(PIPE_CLOSE)
        p[1].close()
        p[2].close()
        p[0].join()
        pass

    pass
##########################################################################


##########################################################################
def main():

    print "one docker run"
    one_docker_run()

    print "multi docker run"
    multi_docker_run()

    pass
##########################################################################


##########################################################################
if __name__ == "__main__":
    main()
    pass
##########################################################################
