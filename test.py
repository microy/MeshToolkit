# -*- coding:utf-8 -*- 

#
# Test playground
#


#
# External dependencies
#
import timeit
from numpy import unique
from PyMesh.Core.Mesh import *
from PyMesh.File.Vrml import *
from PyMesh.Tool.Color import *
from PyMesh.Tool.Curvature import *
from PyMesh.Tool.Repair import *


# Global variables
testmesh = None



#
# Test function
#

def Test( mesh ) :
	
	global testmesh
	testmesh = mesh
	r1 = Test1()
	r2 = Test2()
	print( "Test 1 : {}".format( timeit.timeit("Test1()", setup="from test import Test1", number=10) ) )
	print( "Test 2 : {}".format( timeit.timeit("Test2()", setup="from test import Test2", number=10) ) )
	print( (r1 == r2).all() )

	
def Test1() :

	neighbor_vertices =  GetNeighborVertices( testmesh ) 
	neighbor_faces =  GetNeighborFaces( testmesh )
	border_vertices = zeros( len(testmesh.vertices), dtype=bool )
	
	# Loop through the neighbor vertices
	for va, vn in enumerate( neighbor_vertices ) :
		for vb in vn :
			
			# Check the number of faces in common between the initial vertex and the neighbor
			if len( neighbor_faces[va] & neighbor_faces[vb] ) < 2 :
				border_vertices[ va ] = True
				break

	return border_vertices


def Test2() :

	edges =  GetEdges( testmesh ) 
	border_vertices = zeros( len(testmesh.vertices), dtype=bool )
	
	# Loop through the neighbor vertices
	for key in edges.keys() :
		if len( edges[key]['face'] ) < 2 :
			border_vertices[ key[0] ] = True
			border_vertices[ key[1] ] = True

	return border_vertices
