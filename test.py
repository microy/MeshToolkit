# -*- coding:utf-8 -*- 


#
# External dependencies
#
import timeit
from numpy import bincount, cross, sqrt, zeros, allclose
from PyMesh.Core.Mesh import *
from PyMesh.File.Vrml import *
from PyMesh.Tool.Color import *
from PyMesh.Tool.Curvature import *
from PyMesh.Tool.Repair import *


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
		
	
	
