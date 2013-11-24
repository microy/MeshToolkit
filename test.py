#! /usr/bin/env python
# -*- coding:utf-8 -*- 


from Core.Mesh import Mesh, CheckMesh, CheckNeighborhood
from Core.Curvature import GetNormalCurvature
from Core.Color import Array2Color
from Core.Vrml import ReadVrml, WriteVrml
from numpy import array, dot, sqrt
#from numpy.linalg import norm
import sys
import timeit






#--
#
# RemoveIsolatedVertices
#
#--
#
# Remove isolated vertices in the mesh
#
def RemoveIsolatedVertices( mesh ) :

	# External dependencies
	from numpy import array, empty, zeros

	# Register isolated vertices
	isolated_vertices = zeros( len(mesh.vertices), dtype=bool )
	for i, n in enumerate( mesh.neighbor_faces ) :
		if len(n) == 0 : isolated_vertices[i] = True

	# Do nothing if there is no isolated vertex
	if not isolated_vertices.any() : return

	# Create the new vertex array
	new_vertices = []
	for ( v, isolated ) in enumerate( isolated_vertices ) :
		if not isolated : new_vertices.append( mesh.vertices[v] )

	# Create a lookup table for the vertex indices
	lut = empty( len(mesh.vertices), dtype=int )
	index = 0
	for ( v, isolated ) in enumerate( isolated_vertices ) :
		if isolated : lut[v] = -1
		else : lut[v] = index; index += 1
	
	# Create a new face array
	new_faces = lut[mesh.faces].reshape( len(mesh.faces), 3 )
	
	# Return the new mesh
	return Mesh( name='{} clean'.format(mesh.name), vertices=array( new_vertices ), faces=new_faces )








if __name__ == "__main__" :

	filename = ''

	if len(sys.argv) < 2 : filename = 'cube.wrl'
	else : filename = sys.argv[1]

	print '~~~ Read file ~~~'
	mesh = ReadVrml( filename )
	print '  Done.'

	print '~~~ Compute normals ~~~'
	mesh.UpdateNormals()
	print '  Done.'

	print '~~~ Register neighbors ~~~'
	mesh.UpdateNeighbors()
	print '  Done.'

	print mesh

	print '~~~ Check mesh ~~~'
	CheckMesh( mesh )
	print '  Done.'

	print '~~~ Check neighborhood ~~~'
	CheckNeighborhood( mesh )
	print '  Done.'


#	print '~~~ Compute normal curvature ~~~'
#	normal_curvature = GetNormalCurvature( mesh )
#	print '  Done.'

#	print '~~~ Color vertices ~~~'
#	mesh.colors = Array2Color( normal_curvature )
#	print '  Done.'

	print mesh

	if len(sys.argv) == 3 :

		print '~~~ Write file ' + sys.argv[2] + ' ~~~'
		WriteVrml( mesh, sys.argv[2] )
		print '  Done.'

