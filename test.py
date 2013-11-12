#! /usr/bin/env python

from Mesh import *
from Vrml import *
from Visualizer import *
from Normal import *
from Neighbor import *
import time

if __name__ == "__main__":

	m = ReadVrmlFile("swirl.wrl")
	UpdateNormals( m )
	UpdateNeighbors( m )
	print m
#	CheckMesh( m )
	Visualizer( mesh=m, title="Test" ).Run()
