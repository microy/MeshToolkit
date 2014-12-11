# -*- coding:utf-8 -*- 

#
# Test playground
#


#
# External dependencies
#
import timeit
from numpy import allclose, invert, copy
from PyMeshToolkit import *


# Global variables
testmesh = None


#
# Test function
#

def Test( mesh ) :
	
	global testmesh
	testmesh = mesh
	
	#~ m = ReadX3d( 'Models/buddha_clean.x3d' )
	#~ UpdateNormals( m )
	#~ UpdateNeighbors( m )
	#~ print( m )
	#~ print( Check( m ) )
	#~ v = GlutViewer( m )
	#~ v.Run()
	
	
	
	r1 = Test1()
	r2 = Test2()
	r3 = Test3()
	print( "Test 1 : {}".format( timeit.timeit("Test1()", setup="from test import Test1", number=1) ) )
	print( "Test 2 : {}".format( timeit.timeit("Test2()", setup="from test import Test2", number=1) ) )
	print( "Test 3 : {}".format( timeit.timeit("Test3()", setup="from test import Test3", number=1) ) )

	
def Test1() :

	return ReadVrml( 'Models/buddha_clean.wrl' )
	
	

def Test2() :

	return ReadObj( 'Models/buddha_clean.obj' )
	

def Test3() :

	return ReadX3d( 'Models/buddha_clean.x3d' )

