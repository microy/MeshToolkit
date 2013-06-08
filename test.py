#! /usr/bin/env python

from Mesh import *
from Smf import *
from Vrml import *
from Visualizer import *
from Normal import *
from Neighbor import *

if __name__ == "__main__":

	m = ReadSmfFile("swirl.smf")
	print m
	UpdateNormals( m )
	print m
	UpdateNeighbors( m )
	print m
	m = ReadVrmlFile("cube.wrl")
	print m
	UpdateNormals( m )
	print m
	UpdateNeighbors( m )
	print m
	print m.faces
#	Visualizer( mesh=m, title="Test" ).Run()
