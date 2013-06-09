#! /usr/bin/env python

from Mesh import *
from Vrml import *
from Visualizer import *
from Normal import *
from Neighbor import *

if __name__ == "__main__":

	m = ReadVrmlFile("bunny.wrl")
	UpdateNormals( m )
	UpdateNeighbors( m )
	print m
	CheckMesh( m )
#	Visualizer( mesh=m, title="Test" ).Run()
