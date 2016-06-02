#! /usr/bin/env python
# -*- coding:utf-8 -*-

#
# Setup for the MeshToolkit package
#

# External dependencies
from setuptools import setup

# Setup configuration
setup(
    name = "MeshToolkit",
    version = "0.2",
    packages = ['MeshToolkit'],
    scripts = ['meshtoolkit.py'],
    author = "Michaël Roy",
    author_email = "microygh@gmail.com",
    description = "Python 3D Mesh Toolkit",
    license = "MIT",
    url = "https://github.com/microy/MeshToolkit"
)
