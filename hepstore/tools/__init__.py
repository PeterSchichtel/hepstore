#!/usr/bin/env python

# generic tools/helper/etc to be used through out the hepstore

import os
import errno
import numpy as np
import glob

# create new dir mkdir -p
def mkdir(path): 
    try:
        os.makedirs(path)
        pass
    except OSError as exc:  # Python >2.5                                                                                              
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
        pass
    pass #mkdir

# colorful output
class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    END       = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    pass #bcolors

# compute centre of mass for two given energies (assume mass less particles)
def centre_of_mass(ea,eb):
    return np.sqrt( 0.5 * ea * eb )

# generic data type, with save/load function
class data:
    def __init__(self,name):
        self.datalist = []
        self.name     = name
        pass
    def save(self,filename,allow_pickle=False,fix_imports=True):
        np.save(filename,self.data(),allow_pickle=allow_pickle,fix_imports=fix_imports)
        pass
    def load(self,filename, mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII'):
        self.datalist = np.ndarray.tolist( np.load(filename, mmap_mode=mmap_mode, allow_pickle=allow_pickle, fix_imports=fix_imports, encoding=encoding) )
        pass
    def data(self):
        return np.array(self.datalist)
    def append(self,d):
        self.datalist.append(d)
        pass
    def remove(self,d):
        self.datalist.remove(d)
        pass
    def clear(self):
        self.datalist = []
        pass
    pass #data

# create folder tree including constraints
# unresolved constraints will result in entries without
# corrresponding path
def listoffolders(pathes=["./"],all_constrains=[]):
    fullList = []
    try:
        constrains = all_constrains[0]
        pass
    except IndexError:
        constrains = []
        pass
    try:
        remained_constrains = all_constrains[1:]
        pass
    except IndexError:
        remained_constrains = []
        pass
    # recursive step
    for path in pathes:
        folders=glob.glob(os.path.join(path,"*/"))
        # filter
        i=0
        while len(folders)>i:
            folder = folders[i]
            if (folder.strip('/').split('/')[-1] in ['events','showers','analysis']) or (constrains!=[] and folder.strip('/').split('/')[-1] not in constrains):
                folders.remove(folder)
                pass
            else:
                i+=1
                pass
            pass
        # add non existant constrains as would be folders
        for constrain in constrains:
            if not any(constrain in folder for folder in folders):
                folders.append(os.path.join(path,constrain))
                pass
            pass
        # check for end of recursion
        if folders==[]:
            fullList.append(path)
            pass
        else:
            fullList=(fullList+listoffolders(folders,remained_constrains))
            pass
        pass
    return fullList


def options_to_list(options):
    full_list = []
    for option in options:
        try:
            num  = int(option.split('*')[0])
            kind = option.split('*')[1]
            for i in range(0,num):
                full_list.append(kind)
                pass
            pass
        except Exception:
            full_list.append(option)
            pass
        pass
    return full_list

def shake(data):
    for item in np.nditer(data,op_flags=['readwrite']):
        item[...] = (1.0 + 0.1 * (np.random.random()-0.5)) * item
        pass
    return data
