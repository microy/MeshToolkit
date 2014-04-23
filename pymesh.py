#! /usr/bin/env python
# -*- coding:utf-8 -*- 


#
# External dependencies
#
import sys
import timeit
from numpy import bincount, cross, sqrt, zeros, allclose
from PyMesh.Mesh import Mesh, UpdateNormals, GetNeighborFaces, GetNeighborVertices, GetBorderVertices
from PyMesh.Tools.Repair import CheckMesh, CheckNeighborhood, RemoveIsolatedVertices, InvertFacesOrientation
from PyMesh.Tools.Curvature import GetNormalCurvature, GetGaussianCurvature
from PyMesh.Tools.Color import Array2Colors, VectorArray2Colors
from PyMesh.File.Vrml import ReadVrml, WriteVrml



#
# Normal computation test
#

def TestNormals( mesh ) :
	
	vn1 = GetNormals1( mesh )
	vn2 = GetNormals2( mesh )
	vn3 = GetNormals3( mesh )
	print( "GetNormals 1 : {}".format( timeit.timeit("GetNormals1(mesh)", setup="from __main__ import mesh, GetNormals1", number=1) ) )
	print( "GetNormals 2 : {} {}".format( timeit.timeit("GetNormals2(mesh)", setup="from __main__ import mesh, GetNormals2", number=1), allclose( vn1, vn2 ) ) )
	print( "GetNormals 3 : {} {}".format( timeit.timeit("GetNormals3(mesh)", setup="from __main__ import mesh, GetNormals3", number=1), allclose( vn1, vn3 ) ) )
	
def GetNormals1( mesh ) :
	tris = mesh.vertices[ mesh.faces ]
	face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	face_normals /= sqrt( (face_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )
	vertex_normals = zeros( mesh.vertices.shape )
	for i, f in enumerate( mesh.faces ) : vertex_normals[ f ] += face_normals[ i ]
	return vertex_normals / sqrt( (vertex_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )

def GetNormals2( mesh ) :
	tris = mesh.vertices[ mesh.faces ]
	face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	face_normals /= sqrt( (face_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )
	vertex_normals = zeros( mesh.vertices.shape )
	for i in range(vertex_normals.shape[-1]) :
		vertex_normals[:, i] += bincount( mesh.faces[:, 0], face_normals[:, i], minlength=len(vertex_normals) )
		vertex_normals[:, i] += bincount( mesh.faces[:, 1], face_normals[:, i], minlength=len(vertex_normals) )
		vertex_normals[:, i] += bincount( mesh.faces[:, 2], face_normals[:, i], minlength=len(vertex_normals) )
	return vertex_normals / sqrt( (vertex_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )

def GetNormals3( mesh ) :
	tris = mesh.vertices[ mesh.faces ]
	face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	face_normals /= sqrt( (face_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )
	vertex_normals = zeros( mesh.vertices.shape )
	vertex_normals[ mesh.faces[:,0] ] += face_normals
	vertex_normals[ mesh.faces[:,1] ] += face_normals
	vertex_normals[ mesh.faces[:,2] ] += face_normals
	return vertex_normals / sqrt( (vertex_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )
		
	
	
#
# Main
#
if __name__ == "__main__" :

	filename = ''

	if len(sys.argv) < 2 : filename = 'Models/cube.wrl'
	else : filename = sys.argv[1]

	print( '~~ Read file ' + filename + ' ~~' )
	mesh = ReadVrml( filename )
	print( '  Done.' )

	print( mesh )
	
	print( '~~ Compute normals ~~' )
	UpdateNormals( mesh )
	print( '  Done.' )

	print( '~~ Check mesh ~~' )
	log_message = CheckMesh( mesh )
	if log_message : print( log_message )
	print( '  Done.' )

#	print( '~~ Check neighborhood ~~' )
#	print( CheckNeighborhood( mesh ) )
#	print( '  Done.' )

#	print( '~~ Register edges ~~' )
#	mesh.UpdateEdges()
#	print( '  Done.' )
#	print len( mesh.edges.keys() )
#	print mesh.edges

	print( '~~ Compute curvature ~~' )
	curvature = GetNormalCurvature( mesh )
#	curvature = GetGaussianCurvature( mesh )
	mesh.colors = VectorArray2Colors( curvature )
	print( '  Done.' )

#	print( '~~ Color border vertices ~~' )
#	border = GetBorderVertices( mesh )
#	mesh.colors = Array2Colors( border )
#	print( '  Done.' )

#	print( '~~ Test curvature ~~' )
#	TestCurvature( mesh )
#	print( '  Done.' )

#	print( '~~ Test normals ~~' )
#	TestNormals( mesh )
#	print( '  Done.' )

	print( mesh )

	if len(sys.argv) == 3 :

		print( '~~ Write file ' + sys.argv[2] + ' ~~' )
		WriteVrml( mesh, sys.argv[2] )
		print( '  Done.' )
		
