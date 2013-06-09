#! /usr/bin/env python

from Mesh import *
from Smf import *
from Vrml import *
from Visualizer import *
from Normal import *
from Neighbor import *

if __name__ == "__main__":

	m = ReadSmfFile("swirl.smf")
	UpdateNormals( m )
	UpdateNeighbors( m )
	print m
	WriteVrmlFile( m, "swirl.wrl" )
#	m = ReadVrmlFile("cube.wrl")
	UpdateNormals( m )
	UpdateNeighbors( m )
	print m
	WriteVrmlFile( m, "test2.wrl" )
#	Visualizer( mesh=m, title="Test" ).Run()
