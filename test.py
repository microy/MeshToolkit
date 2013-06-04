#! /usr/bin/env python

from Mesh import *
from SmfFile import *
from Visualizer import *

if __name__ == "__main__":

	m = ReadSmfFile("swirl.smf")
	UpdateNormals( m )
	UpdateNeighbors( m )
	print m
	Visualizer( mesh=m, title="Test" ).Run()
