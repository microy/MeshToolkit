#! /usr/bin/env python
# -*- coding:utf-8 -*- 


import sys
import timeit
import numpy

from numpy import bincount, cross, sqrt, zeros


from Core.Mesh import Mesh
from Core.Repair import CheckMesh, CheckNeighborhood, RemoveIsolatedVertices, InvertFacesOrientation
from Core.Curvature import GetNormalCurvature, GetGaussianCurvature
from Core.Color import Array2Colors, VectorArray2Colors
from Core.Vrml import ReadVrml, WriteVrml

normal_curvature = []

def test( mesh ) :
#	for v in range(len(mesh.vertices)) :
#		if mesh.IsBorderVertex( v ) : pass
	normal_curvature = GetNormalCurvature( mesh )
#	InvertFacesOrientation( mesh )
#	mesh.UpdateNormals()
	

if __name__ == "__main__" :

	filename = ''

	if len(sys.argv) < 2 : filename = 'Models/cube.wrl'
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

#	print( '~~~ Check neighborhood ~~~' )
#	print( CheckNeighborhood( mesh ) )
#	print( '  Done.' )

#	print( '~~~ Register edges ~~~' )
#	mesh.UpdateEdges()
#	print( '  Done.' )
#	print len( mesh.edges.keys() )
#	print mesh.edges

#	print( '~~~ Time ~~~' )
#	print(timeit.timeit("test(mesh)", setup="from __main__ import mesh, test", number=10))
#	print( '  Done.' )

	print '~~~ Compute curvature ~~~'
	curvature = GetNormalCurvature( mesh )
#	curvature = GetGaussianCurvature( mesh )
	mesh.colors = VectorArray2Colors( curvature )
	print '  Done.'

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
		
	
	
#
# Normal computation test
#
	
def GetNormals1( mesh ) :
	tris = mesh.vertices[ mesh.faces ]
	face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	print (sqrt((face_normals**2).sum(axis=1))>0).all()
	face_normals /= sqrt( (face_normals ** 2).sum( axis=1 ) ).reshape( len(face_normals), 1 )
	vertex_normals = zeros( mesh.vertices.shape )
	for i, f in enumerate( mesh.faces ) :
		vertex_normals[ f ] += face_normals[ i ]
	return vertex_normals / sqrt( (vertex_normals ** 2).sum( axis=1 ) ).reshape( len(vertex_normals), 1 )

def GetNormals2( mesh ) :
	tris = mesh.vertices[ mesh.faces ]
	face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	face_normals /= sqrt( (face_normals ** 2).sum( axis=1 ) ).reshape( len(face_normals), 1 )
	vertex_normals = zeros( mesh.vertices.shape )
	for i in range(vertex_normals.shape[-1]) :
		vertex_normals[:, i] += bincount( mesh.faces[:, 0], face_normals[:, i], minlength=len(vertex_normals) )
		vertex_normals[:, i] += bincount( mesh.faces[:, 1], face_normals[:, i], minlength=len(vertex_normals) )
		vertex_normals[:, i] += bincount( mesh.faces[:, 2], face_normals[:, i], minlength=len(vertex_normals) )
	return vertex_normals / sqrt( (vertex_normals ** 2).sum( axis=1 ) ).reshape( len(vertex_normals), 1 )

def GetNormals3( mesh ) :
	tris = mesh.vertices[ mesh.faces ]
	face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	face_normals /= sqrt( (face_normals ** 2).sum( axis=1 ) ).reshape( len(face_normals), 1 )
	vertex_normals = zeros( mesh.vertices.shape )
	vertex_normals[ mesh.faces[:,0] ] += face_normals
	vertex_normals[ mesh.faces[:,1] ] += face_normals
	vertex_normals[ mesh.faces[:,2] ] += face_normals
	return vertex_normals / sqrt( (vertex_normals ** 2).sum( axis=1 ) ).reshape( len(vertex_normals), 1 )
		


