#! /usr/bin/env python

from Core.Mesh import *
from Core.BoundingContainer import *
from Core.Vrml import *
from Viewer.GlutViewer import *
from numpy import *


if __name__ == "__main__":

	m = ReadVrmlFile("bunny.wrl")

	UpdateNormals( m )
#	UpdateNeighbors( m )
	print m
#	CheckMesh( m )
	v = GlutViewer( mesh=m, title="Test" )
	v.PrintInfo()
	v.Run()
