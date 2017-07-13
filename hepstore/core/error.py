#!/usr/bin/env python

# python imports
import argparse

# our own label error
class LabelError(IndexError):
    pass

# our own argument parsing error
class ParserError(argparse.ArgumentTypeError):
    pass

# fit error
class FitError(Exception):
    pass

# unknown collider
class ColliderError(KeyError):
    pass

# unknown model
class ModelError(KeyError):
    pass

# unknown provider
class ProviderError(KeyError):
    pass

# unknown scale
class ScaleError(KeyError):
    pass

class ShowerError(KeyError):
    pass

class Flavorerror(KeyError):
    pass

class PdfError(KeyError):
    pass

