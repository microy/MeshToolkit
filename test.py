# -*- coding:utf-8 -*- 

#
# Test playground
#


#
# External dependencies
#
import timeit
from numpy import *
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
	print( "Test 1 : {}".format( timeit.timeit("Test1()", setup="from test import Test1", number=1) ) )
	print( "Test 2 : {}".format( timeit.timeit("Test2()", setup="from test import Test2", number=1) ) )
#	print( r1[0] )
#	print( r2[0] )

	
def Test1() :

	# Initialization
	neighbor_vertices = [ [] for i in range(len( testmesh.vertices )) ]

	# Loop through the faces
	for i, (a, b ,c) in enumerate( testmesh.faces ) :

		# Add vertices link by a face
		neighbor_vertices[ a ].append( b )
		neighbor_vertices[ a ].append( c )
		neighbor_vertices[ b ].append( a )
		neighbor_vertices[ b ].append( c )
		neighbor_vertices[ c ].append( a )
		neighbor_vertices[ c ].append( b )

	# Return the list of neighbors without duplicates
	return [ set( i ) for i in neighbor_vertices ] 


def Test2() :

	# Initialization
	neighbor_vertices = [ set() for i in range(len( testmesh.vertices )) ]

	# Loop through the faces
	for i, (a, b ,c) in enumerate( testmesh.faces ) :

		# Add vertices link by a face
		neighbor_vertices[ a ].add( b )
		neighbor_vertices[ a ].add( c )
		neighbor_vertices[ b ].add( a )
		neighbor_vertices[ b ].add( c )
		neighbor_vertices[ c ].add( a )
		neighbor_vertices[ c ].add( b )

	# Return the list of neighbors without duplicates
	return neighbor_vertices

