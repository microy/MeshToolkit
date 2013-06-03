#! /usr/bin/env python

from Mesh import *
from SmfFile import *
from Visualizer import *

if __name__ == "__main__":

	m = ReadSmfFile("swirl.smf")
	m.UpdateNormals()
	m.UpdateNeighbors()
	print m
	Visualizer().Run()
