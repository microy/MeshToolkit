#! /usr/bin/env python
# -*- coding:utf-8 -*- 


from Core.Mesh import CheckMesh
from Core.Normal import UpdateNormals
from Core.Neighbor import UpdateNeighborhood, CheckNeighborhood
from Core.Curvature import GetNormalCurvature
from Core.Color import Array2Color
from Core.Vrml import ReadVrml, WriteVrml
from numpy import array, dot, sqrt
#from numpy.linalg import norm
import sys
import timeit





if __name__ == "__main__" :

	filename = ''

	if len(sys.argv) < 2 : filename = 'cube.wrl'
	else : filename = sys.argv[1]

	print '~~~ Read file ~~~'
	mesh = ReadVrml( filename )
	print '  Done.'

	print mesh

#	print '~~~ Check mesh ~~~'
#	CheckMesh( mesh )
#	print '  Done.'

#	print '~~~ Compute normals ~~~'
#	UpdateNormals( mesh )
#	print '  Done.'

	print '~~~ Register neighborhood ~~~'
	UpdateNeighborhood( mesh )
	print '  Done.'

#	print '~~~ Check neighborhood ~~~'
#	CheckNeighborhood( mesh )
#	print '  Done.'
#

	print '~~~ Compute normal curvature ~~~'
	normal_curvature = GetNormalCurvature( mesh )
	print '  Done.'

	print '~~~ Color vertices ~~~'
	mesh.colors = Array2Color( normal_curvature )
	print '  Done.'

#	print mesh

#	print '~~~ Check mesh ~~~'
#	CheckMesh( mesh )
#	print '  Done.'

	if len(sys.argv) == 3 :

		print '~~~ Write file ' + sys.argv[2] + ' ~~~'
		WriteVrml( mesh, sys.argv[2] )
		print '  Done.'

