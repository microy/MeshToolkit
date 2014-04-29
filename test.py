# -*- coding:utf-8 -*- 

#
# Test playground
#


#
# External dependencies
#
import timeit
from numpy import allclose, invert, copy
from PyMesh import *


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
	
	
	r1 = Test1()
	r2 = Test2()
	print( "Test 1 : {}".format( timeit.timeit("Test1()", setup="from test import Test1", number=10) ) )
	print( "Test 2 : {}".format( timeit.timeit("Test2()", setup="from test import Test2", number=10) ) )
	print( allclose(r1, r2) )

	
def Test1() :

	# Convert neighbor list to numpy array for fancy indexing
	neighbors =  [ array(list(v)) for v in testmesh.neighbor_vertices ]

	# Get neighbor vertex number
	neighbor_number = array( [ len(i) for i in neighbors ] ).reshape(-1,1)

	# Get border vertices
	border = GetBorderVertices( testmesh )

	vertices = copy( testmesh.vertices )

	# Iteration steps
	for i in range( iteration ) :

		# Average neighbor vertices
		smoothed = [ (vertices[neighbors[v]]).sum(axis=0) for v in range( len(vertices) ) ]
		smoothed /= neighbor_number

		# Get new vertex position
		smoothed = vertices + diffusion * ( smoothed - vertices )

		# Don't change border vertices
		smoothed[ border ] = vertices[ border ]

		# Update original vertices
		vertices = smoothed

	return vertices
	
	

def Test2() :

	# Convert neighbor list to numpy array for fancy indexing
	neighbors =  [ array(list(v)) for v in testmesh.neighbor_vertices ]

	# Get neighbor vertex number
	neighbor_number = array( [ len(i) for i in neighbors ] ).reshape(-1,1)

	# Get border vertices
	border = GetBorderVertices( testmesh )

	vertices = copy( testmesh.vertices )

	# Iteration steps
	for i in range( iteration ) :

		# Compute displacement values
#		displacement = diffusion * ( [ (vertices[neighbors[v]]).sum(axis=0) for v in range( len(vertices) ) ] / neighbor_number - vertices )
		
		# Don't change border vertices
#		displacement[ border ] = 0
		
		# Get new vertex position
#		vertices += displacement

		# Compute average of neighbor vertices
		displacement  = [ (vertices[neighbors[v]]).sum(axis=0) for v in range( len(vertices) ) ] / neighbor_number
		displacement -= vertices
		
		# Don't change border vertices
		displacement[ border ] = 0
		
		# Get new vertex position
		vertices += diffusion *displacement
		
	return vertices

