#!/usr/bin/env python

# global imports
import os
import numpy as np
from itertools import cycle

# hepstore imports
from hepstore.core.utility import *
from hepstore.core.error import *

# local imports
from student import *
from data import *

# the teacher of our school
class Teacher(object):

    def __init__(self,options):
        self.options = options
        self.student = None
        # create cyclers for options
        self.label = cycle( options_to_list(options.label) )
        pass

    def teach(self):
        # load data
        for fin in self.options.file:
            raw_data = np.load(fin)
            data     = DataUnit(raw_data,np.array([next(self.label)]*len(raw_data)))
            if self.student == None:
                self.student = Student(self.options,data)
                pass
            else:
                self.student.add_data(data)
                pass
            pass
        if self.options.load == '':
            # prepare student
            self.student.prepare()
            # check that training is allowed
            if len(np.unique(self.student.label_train))<=1:
                raise LabelError("not enough labels for training")
            # explore classifier
            if self.options.explore or self.options.only_explore:
                self.student.explore()
                pass
            # train student
            if not self.options.only_explore:
                self.student.train()
                self.student.test()
                pass
            pass
        else:
            self.student.load()
            self.student.classify()
            pass
        pass

    def save(self):
        mkdir(self.options.path)
        # preparation results
        if self.options.explore or self.options.only_explore:
            pass
        if not self.options.only_explore and self.options.load == '':
            self.student.save()
            pass
        pass

    pass
