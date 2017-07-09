#!/usr/bin/env python

# python imports
import argparse

# our own label error
class LabelError(IndexError):
    pass

# our own argument parsing error
class ParserError(argparse.ArgumentTypeError):
    pass


