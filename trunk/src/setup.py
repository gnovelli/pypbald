'''
    Module for the creation of an executable version of pypbald.
    
    This module is based on py2exe.

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"


import os
from distutils.core import setup
from shutil import rmtree

setup(console=['main.py'],
      options = {"py2exe": {"dist_dir": os.path.join("..", "dist")}})
      
rmtree('build')
