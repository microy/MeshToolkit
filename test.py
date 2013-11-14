#! /usr/bin/env python

from Core.Mesh import *
from Core.Vrml import *
from Viewer.Viewer import *


if __name__ == "__main__":

	m = ReadVrmlFile("cube1.wrl")
	UpdateNormals( m )
#	UpdateNeighbors( m )
	print m
#	CheckMesh( m )
	v = Viewer( mesh=m, title="Test" )
	v.PrintInfo()
	v.Run()
