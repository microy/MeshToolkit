# -*- coding:utf-8 -*-

#
# Test playground
#


#
# External dependencies
#
import timeit
import numpy as np
from numpy import allclose, invert, copy
import MeshToolkit as mtk


# Global variables
testmesh = None


#
# Test function
#

def Test( mesh = None ) :

	mesh = mtk.GenerateSaddleSurface()

	print( mesh )

	# Return the newly constructed triangular mesh
	mtk.WritePly( mesh, 'saddle.ply' )

	#~ global testmesh
	#~ testmesh = mesh
	#~
	#~ r1 = Test1()
	#~ r2 = Test2()
	#~ print( "Test 1 : {}".format( timeit.timeit("Test1()", setup="from MeshToolkit.Core.Test import Test1", number=1) ) )
	#~ print( "Test 2 : {}".format( timeit.timeit("Test2()", setup="from MeshToolkit.Core.Test import Test2", number=1) ) )
	#~ print( allclose( r1, r2 ) )


def Test1() :

	return mtk.GetNormalCurvature( testmesh )



def Test2() :

	return mtk.GetNormalCurvatureReference( testmesh )


def TestGenerateSaddleSurface( xsize = 200, ysize = 200 ) :

	# Compute vertex coordinates
	X, Y = np.meshgrid( np.linspace( -2, 2, xsize ), np.linspace( -2, 2, ysize ) )
	Z = ( X ** 2 - Y ** 2 ) * 0.5

	# Create the vertex array
	vertices = np.array( (X.flatten(), Y.flatten(), Z.flatten()) ).T

	# Find the diagonal that minimizes the Z difference
	right_diagonal = np.absolute( Z[1:,1:] - Z[:-1,:-1] ) < np.absolute( Z[1:,:-1] - Z[:-1,1:] )

	# Create the faces
	faces = []
	for j in range( ysize - 1 ) :
		for i in range( xsize - 1 ) :
			if right_diagonal[j,i] :
				face1 = np.array( [j*xsize+i, j*xsize+i+1, (j+1)*xsize+i+1] )
				face2 = np.array( [j*xsize+i, (j+1)*xsize+i+1, (j+1)*xsize+i] )
			else :
				face1 = np.array( [j*xsize+i, j*xsize+i+1, (j+1)*xsize+i] )
				face2 = np.array( [j*xsize+i+1, (j+1)*xsize+i+1, (j+1)*xsize+i] )
			faces.append( face1 )
			faces.append( face2 )

	mesh = mtk.Mesh( 'Saddle', vertices, faces )

	# Return the newly constructed triangular mesh
	mtk.WritePly( mesh, 'saddle.ply' )
