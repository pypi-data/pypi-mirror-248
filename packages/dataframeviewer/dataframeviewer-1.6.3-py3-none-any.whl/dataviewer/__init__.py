import os
import sys
import glob
from   os.path import dirname, basename, isfile, join

# Update PYTHONPATH
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Import main function
from .dataviewer import main

# Import all .py files in this directory
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]