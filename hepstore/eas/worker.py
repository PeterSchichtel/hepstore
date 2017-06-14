#!/usr/bin/env python

import interaction
import shower
import analysis

# contains workers for multi processed interaction/shower/analysis

def interact(num,pipe,options):
    output_p, input_p = pipe
    app=interaction.interaction(num=num)
    while True:
        try:
            path = output_p.recv()    # Read from the output pipe and do nothing
            if not app.begin(path,options):
                print "--info: skipping  %s" % path
                continue
            app.run()
            pass
        except EOFError:
            break
        pass
    input_p.close()
    output_p.close()
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

def analyse(num,pipe,options):
    output_p, input_p = pipe
    app=analysis.analysis(num=num)
    while True:
        try:
            path = output_p.recv()    # Read from the output pipe and do nothing
            if not app.begin(path,options):
                print "--info: skipping  %s" % path
                continue
            app.run()
            app.save()
            pass
        except EOFError:
            break
        pass
    input_p.close()
    output_p.close()
    pass
