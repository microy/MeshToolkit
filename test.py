#! /usr/bin/env python
# -*- coding:utf-8 -*- 


import sys
import timeit
import numpy

from Core.Mesh import Mesh, CheckMesh, CheckNeighborhood
from Core.Curvature import GetNormalCurvature
from Core.Color import Array2Color
from Core.Vrml import ReadVrml, WriteVrml

normal_curvature = []

def test( mesh ) :
	for v in range(len(mesh.vertices)) :
		if mesh.IsBorderVertex( v ) : pass
#	normal_curvature = GetNormalCurvature( mesh )
		
		

if __name__ == "__main__" :

	print(sys.version)

	filename = ''

	if len(sys.argv) < 2 : filename = 'cube.wrl'
	else : filename = sys.argv[1]

	print( '~~~ Read file ~~~' )
	mesh = ReadVrml( filename )
	print( '  Done.' )

	print( '~~~ Compute normals ~~~' )
	mesh.UpdateNormals()
	print( '  Done.' )

	print( '~~~ Register neighbors ~~~' )
	mesh.UpdateNeighbors()
	print( '  Done.' )

	print( mesh )

	print( '~~~ Check mesh ~~~' )
	CheckMesh( mesh )
	print( '  Done.' )

	print( '~~~ Check neighborhood ~~~' )
	CheckNeighborhood( mesh )
	print( '  Done.' )

	print( '~~~ Neighbor ~~~' )
	print(timeit.timeit("test(mesh)", setup="from __main__ import mesh, test", number=100))
	print( '  Done.' )

#	print '~~~ Compute normal curvature ~~~'
#	normal_curvature = GetNormalCurvature( mesh )
#	mesh.colors = Array2Color( normal_curvature )
#	print '  Done.'

#	print '~~~ Color vertices ~~~'
#	b = numpy.zeros( (len(mesh.vertices),3) )
#	for v in range(len(mesh.vertices)) :
#		if mesh.IsBorderVertex( v ) : b[v] = [1,0,0]
#	mesh.colors = Array2Color( b )
#	print '  Done.'

#	print( mesh )

	if len(sys.argv) == 3 :

		print( '~~~ Write file ' + sys.argv[2] + ' ~~~' )
		WriteVrml( mesh, sys.argv[2] )
		print( '  Done.' )

