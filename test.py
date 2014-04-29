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

	return ReadVrml( 'Models/buddha_clean.wrl' )
	
	

def Test2() :

	return ReadObj( 'Models/buddha_clean.obj' )

