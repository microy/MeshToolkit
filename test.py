#! /usr/bin/env python

from Core.Mesh import *
from Core.Vrml import *
from Viewer.Viewer import *
from numpy import *


if __name__ == "__main__":

#	m = ReadVrmlFile("cube1.wrl")
	m = Mesh( vertices = array([[0.75,0.75,0], [0.75,-0.75,0], [-0.75,-0.75,0]], dtype=float32),
		faces = array([[0, 1, 2]], dtype=uint32),
		colors = array([[0.5,0.2,0],[0.1,0.8,0],[0.3,0.1,0.9]],dtype=float32) )

#	UpdateNormals( m )
#	UpdateNeighbors( m )
	print m
#	CheckMesh( m )
	v = Viewer( mesh=m, title="Test" )
	v.PrintInfo()
	v.Run()
