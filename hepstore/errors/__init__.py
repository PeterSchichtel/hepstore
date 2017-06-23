#!/usr/bin/env python

import os

import numpy as np
import sys
import argparse

class LabelError(IndexError):
    pass

class ParserError(argparse.ArgumentTypeError):
    pass


