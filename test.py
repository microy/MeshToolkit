#! /usr/bin/env python
# -*- coding:utf-8 -*- 


import sys
import timeit
import numpy

from Core.Mesh import Mesh
from Core.Repair import CheckMesh, CheckNeighborhood, RemoveIsolatedVertices
from Core.Curvature import GetNormalCurvature, GetGaussianCurvature
from Core.Color import Array2Colors, VectorArray2Colors
from Core.Vrml import ReadVrml, WriteVrml

normal_curvature = []

def test( mesh ) :
#	for v in range(len(mesh.vertices)) :
#		if mesh.IsBorderVertex( v ) : pass
	normal_curvature = GetNormalCurvature( mesh )
		
		

if __name__ == "__main__" :

	print(sys.version)

	filename = ''

	if len(sys.argv) < 2 : filename = 'cube.wrl'
	else : filename = sys.argv[1]

	print( '~~~ Read file ' + filename + ' ~~~' )
	mesh = ReadVrml( filename )
	print( '  Done.' )

	print( mesh )
	
	print( '~~~ Compute normals ~~~' )
	mesh.UpdateNormals()
	print( '  Done.' )

	print( '~~~ Register neighbors ~~~' )
	mesh.UpdateNeighbors()
	print( '  Done.' )

	print( '~~~ Check mesh ~~~' )
	print( CheckMesh( mesh ) )
	print( '  Done.' )

	print( '~~~ Check neighborhood ~~~' )
	print( CheckNeighborhood( mesh ) )
	print( '  Done.' )

	print( '~~~ Register edges ~~~' )
	mesh.UpdateEdges()
	print( '  Done.' )

#	print( '~~~ Neighbor ~~~' )
#	print(timeit.timeit("test(mesh)", setup="from __main__ import mesh, test", number=1))
#	print( '  Done.' )

#	print '~~~ Compute curvature ~~~'
#	curvature = GetGaussianCurvature( mesh )
#	mesh.colors = Array2Colors( curvature )
#	print '  Done.'

#	print '~~~ Color vertices ~~~'
#	b = numpy.zeros( (len(mesh.vertices),3) )
#	for v in range(len(mesh.vertices)) :
#		if mesh.IsBorderVertex( v ) : b[v] = [1,0,0]
#	mesh.colors = Array2Color( b )
#	print '  Done.'

	print( mesh )

	if len(sys.argv) == 3 :

		print( '~~~ Write file ' + sys.argv[2] + ' ~~~' )
		WriteVrml( mesh, sys.argv[2] )
		print( '  Done.' )

