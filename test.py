#! /usr/bin/env python

from Core.Mesh import *
from Core.Vrml import *
from Viewer.Viewer import *

if __name__ == "__main__":

	m = ReadVrmlFile("Data/swirl.wrl")
	UpdateNormals( m )
	UpdateNeighbors( m )
	print m
#	CheckMesh( m )
	Viewer( mesh=m, title="Test" ).Run()
