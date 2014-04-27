# -*- coding:utf-8 -*- 

#
# Test playground
#


#
# External dependencies
#
import timeit
from numpy import allclose, invert
from PyMesh.Core.Mesh import *
from PyMesh.File.Vrml import *
from PyMesh.Tool.Color import *
from PyMesh.Tool.Curvature import *
from PyMesh.Tool.Repair import *
from PyMesh.Tool.Smoothing import *


# Global variables
testmesh = None
iteration = 5
diffusion = 1


#
# Test function
#

def Test( mesh ) :
	
	global testmesh
	testmesh = mesh
	
	mesh.vertices = UniformLaplacianSmoothing( mesh, iteration, diffusion )
	
#	r1 = Test1()
#	r2 = Test2()
#	print( "Test 1 : {}".format( timeit.timeit("Test1()", setup="from test import Test1", number=1) ) )
#	print( "Test 2 : {}".format( timeit.timeit("Test2()", setup="from test import Test2", number=10) ) )
#	print( allclose(r1, r2) )

	
def Test1() :

	# Get neighbors
	neighbor_vertices =  GetNeighborVertices( testmesh ) 
	neighbor_faces =  GetNeighborFaces( testmesh )
	
	# Get border
	border = zeros( len(testmesh.vertices), dtype=bool )
	for va, vn in enumerate( neighbor_vertices ) :
		for vb in vn :
			if len( neighbor_faces[va] & neighbor_faces[vb] ) < 2 :
				border[ va ] = True
				break

	# Smooth
	vertices = testmesh.vertices.copy()
	for i in range( iteration ) :
		
		smoothed = zeros( vertices.shape )

		for v in range( len(vertices) ) :
			
			# Don't smooth border vertex
			if border[v] : smoothed[v] = vertices[v]
			else :
			
				for n in neighbor_vertices[v] :	smoothed[v] += vertices[n] - vertices[v]
				smoothed[v] = vertices[v] + diffusion * smoothed[v] / len( neighbor_vertices[v] )

		vertices = smoothed

	return vertices



def Test2() :

	# Get neighbors
	neighbors =  [ array(list(v)) for v in GetNeighborVertices( testmesh ) ]
	neighbor_number = array( [ len(i) for i in neighbors ] ).reshape(-1,1)
	not_on_border = invert( GetBorderVertices( testmesh ) )
#	border = GetBorderVertices( testmesh )

	# Smooth
	vertices = testmesh.vertices.copy()
	for i in range( iteration ) :
		
		smoothed = [ (vertices[neighbors[v]]).sum(axis=0) for v in range( len(vertices) ) ]
		smoothed /= neighbor_number
		smoothed -= vertices
		smoothed *= diffusion
		smoothed += vertices
		vertices[ not_on_border ] = smoothed[ not_on_border ]
#		smoothed[border] = vertices[border]
#		vertices = smoothed
#		for v in range( len(vertices) ) :
#			if border[v] : smoothed[v] = vertices[v]

	return vertices

