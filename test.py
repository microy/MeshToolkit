#! /usr/bin/env python

from Core import *
from Core.Vrml import *
from Viewer import *
from Viewer.GlutViewer import *


if __name__ == "__main__":

	m = ReadVrmlFile("swirl.wrl")

	UpdateNormals( m )
#	UpdateNeighbors( m )
	print m
#	CheckMesh( m )
	v = GlutViewer( mesh=m, title="Test" )
	v.PrintInfo()
	v.Run()
