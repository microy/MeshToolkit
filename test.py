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
	print( len(r1) )
	print( len(r2) )
	print( (sort(list(r1.keys())) == sort(list(r2))).all() )

	
def Test1() :

	# Edge dictionary
	edges = { e : {} for a, b in sort( testmesh.faces )[:,[[0,0,1],[1,2,2]]] for e in zip(a,b) }

	return edges


def Test2() :

	# Edge set (unordered unique list)
	edges = set( e for a, b in sort( testmesh.faces )[:,[[0,0,1],[1,2,2]]] for e in zip(a,b) )

	return edges
