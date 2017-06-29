
import numpy as np
import os

def enrich(fname_in,fname_out,energy=None,element=None,model=None):

    with open(fname_in,'r') as fin:
        with open(fname_out,'w') as fout:
            count=0
            for line in fin.readlines():
                if count==0:
                    num_particles = int(line.split()[0])
                    if   model == "nucl":
                        num_particles+=1
                        pass
                    elif model == "frac":
                        num_particles+=(element.nucleons-1)
                        pass
                    else:
                        raise NotImplemented("unknown model '%s'" % model )
                    fout.write("  %i %f \n" % ( num_particles, energy.value ) )
                    pass
                else:
                    fout.write(line)
                    pass
                count+=1
                pass
            if   model == "nucl":
                energy_nucl = energy.value - energy.value/element.nucleons
                mass        = element.mass - 1.0
                pid         = 100*(int(element.mass)-1) + (element.protons-1)
                px          = np.random.normal(0,1,1)[0]
                py          = np.random.normal(0,1,1)[0]
                pz          = np.sqrt( energy_nucl**2 - mass**2 - px**2 - py**2 )
                fout.write("%5i%5i%15.7e%15.7e%15.7e%15.7e \n" % (count+1,pid,energy_nucl,pz,px,py))
                pass
            elif model == "frac":
                energy_frac = energy.value/element.nucleons
                mass        = 1.0
                for i in range(0,element.neutrons):
                    pid = 15
                    px          = np.random.normal(0,1,1)[0]
                    py          = np.random.normal(0,1,1)[0]
                    pz          = np.sqrt( energy_frac**2 - mass**2 - px**2 - py**2 )
                    fout.write("%5i%5i%15.7e%15.7e%15.7e%15.7e \n" % (count+1,pid,energy_frac,pz,px,py))
                    count+=1
                    pass
                for i in range(0,element.protons-1):
                    pid = 14
                    px          = np.random.normal(0,1,1)[0]
                    py          = np.random.normal(0,1,1)[0]
                    pz          = np.sqrt( energy_frac**2 - mass**2 - px**2 - py**2 )
                    fout.write("%5i%5i%15.7e%15.7e%15.7e%15.7e \n" % (count+1,pid,energy_frac,pz,px,py))
                    count+=1
                    pass
                pass
            else:
                raise NotImplemented("unknown model '%s'" % model )
            pass
        pass
    
    pass
