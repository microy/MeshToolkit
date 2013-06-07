#! /usr/bin/env python

from Mesh import *
from SmfFile import *
from Visualizer import *
from Normal import *
from Neighborhood import *

if __name__ == "__main__":

	m = ReadSmfFile("swirl.smf")
	UpdateNormals( m )
	UpdateNeighbors( m )
	print m
	Visualizer( mesh=m, title="Test" ).Run()
