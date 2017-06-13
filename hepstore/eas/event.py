#!/usr/bin/env python

import numpy as np
import glob

mass_dict={ 1  :[0.0,"photon"],
            2  :[0.000511,"positron"],
            3  :[0.000511,"electron"],  
            5  :[0.106,"muon"],  
            6  :[0.106,"antimuon"],  
            7  :[0.1350,"pion"],  
            8  :[0.1396,"piplus"],  
            9  :[0.1396,"piminus"],  
            10 :[0.4976,"klong"],  
            11 :[0.4937,"kplus"],  
            12 :[0.4937,"kminus"],  
            13 :[0.9396,"neutron"],  
            14 :[0.9383,"proton"],  
            15 :[0.9383,"antiproton"],
            16 :[0.4976,"kshort"],
            18 :[1.115,"lambda"],
            19 :[1.189,"sigmaplus"],
            21 :[1.197,"sigmaminus"],
            25 :[0.9396,"antineutron"],  
            26 :[1.115,"antilambda"],
            27 :[1.197,"antisigmaminus"],
            29 :[1.189,"antisigmaplus"],
            201:[2.014,"deuterium"],
            302:[3.016,"helium-3"],
            402:[4.003,"helium-4"],
}

class particle:
    def __init__(self,energy=0.0,px=0.0,py=0.0,pz=0.0,mass=0.0,t=0.0,x=0.0,y=0.0,pid=0.0,obs=0.0,name="",weight=1.0):
        self.energy=energy
        self.px=px
        self.py=py
        self.pz=pz
        self.pid=pid
        self.name=name
        self.t=t
        self.x=x
        self.y=y
        self.obs=obs
        self.mass=mass
        self.weight=weight
        pass
    def __str__(self):
        return "%5i %9.2e %9.2e %9.2e %9.2e %9.2e %9.2e %9.2e %9.2e %9.2e %5i %10s" % (
            self.pid,self.weight,
            self.energy,self.px,self.py,self.pz,self.mass,
            self.t,self.x,self.y,
            self.obs,self.name)      
    def radius(self):
        return np.sqrt( self.x**2 + self.y**2 )
    pass

class event:
    def __init__(self):
        self.particles=[]
        self.energy=0.0
        self.xmax=0.0
        self.theta=0.0
        pass
    def add_particle(self,p):
        self.particles.append(p)
        pass
    def find(self,tag,layer):
        items=[]
        for item in self.particles:
            if item.name==tag and item.obs==layer:
                items.append(item)
                pass
            pass
        return items
    def particles_from_file(self,path):
        with open(path,'r') as fin:
            is_particledata=False
            for line in fin.readlines():
                if   "#--< begin_particle_data >--" in line:
                    is_particledata=True
                    continue
                elif "#--< end_particle_data >--" in line:
                    is_particledata=False
                    pass
                elif "#--<" in line:
                    is_particledata=False
                    pass
                if is_particledata:
                    words=line.strip().split()
                    pid=int(float(words[0]))/1000
                    obs=int(float(words[0]))%10
                    if pid==75 or pid==76 or pid==0:
                        continue
                    px=float(words[1])
                    py=float(words[2])
                    pz=float(words[3])
                    x=float(words[4])
                    y=float(words[5])
                    t=float(words[6])
                    weight=float(words[7])
                    if not pid in mass_dict.keys():
                        continue
                    mass,name=mass_dict[pid]
                    energy=np.sqrt( px**2 + py**2 + pz**2 + mass**2  )
                    self.particles.append( particle(energy,px,py,pz,mass,t,x,y,pid,obs,name,weight) )
                    pass
                pass #for
            fin.close()
            pass
        pass
    def xmax_from_file(self,path):
        self.xmax=-1.0
        ymax=0.0
        with open(path,'r') as fin:
            for line in fin.readlines():
                if   "LONGITUDINAL ENERGY DEPOSIT IN" in line:
                    break
                elif "LONGITUDINAL DISTRIBUTION IN" in line or "DEPTH" in line:
                    continue
                words=line.strip().split()
                yval = float(words[1]) + float(words[2]) + float(words[3])
                if yval>ymax:
                    ymax=yval
                    self.xmax=float(words[0])
                    pass
                pass #for
            fin.close()
            pass #fin
        pass
    pass
