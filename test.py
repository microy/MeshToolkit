# -*- coding:utf-8 -*- 

#
# Test playground
#


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


# Global variables
global testmesh



#
# Normal computation test
#

def TestNormals( mesh ) :
	
	global testmesh
	testmesh = mesh
	vn1 = GetNormals1(  )
	vn2 = GetNormals2(  )
	vn3 = GetNormals3(  )
	print( "GetNormals 1 : {}".format( timeit.timeit("GetNormals1()", setup="from test import GetNormals1", number=10) ) )
	print( "GetNormals 2 : {} {}".format( timeit.timeit("GetNormals2()", setup="from test import GetNormals2", number=10), allclose( vn1, vn2 ) ) )
	print( "GetNormals 3 : {} {}".format( timeit.timeit("GetNormals3()", setup="from test import GetNormals3", number=10), allclose( vn1, vn3 ) ) )
	
def GetNormals1(  ) :
	tris = testmesh.vertices[ testmesh.faces ]
	face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	face_normals /= sqrt( (face_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )
	vertex_normals = zeros( testmesh.vertices.shape )
	for i, f in enumerate( testmesh.faces ) : vertex_normals[ f ] += face_normals[ i ]
	return vertex_normals / sqrt( (vertex_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )

def GetNormals2(  ) :
	tris = testmesh.vertices[ testmesh.faces ]
	face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	face_normals /= sqrt( (face_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )
	vertex_normals = zeros( testmesh.vertices.shape )
	for i in range(vertex_normals.shape[-1]) :
		vertex_normals[:, i] += bincount( testmesh.faces[:, 0], face_normals[:, i], minlength=len(vertex_normals) )
		vertex_normals[:, i] += bincount( testmesh.faces[:, 1], face_normals[:, i], minlength=len(vertex_normals) )
		vertex_normals[:, i] += bincount( testmesh.faces[:, 2], face_normals[:, i], minlength=len(vertex_normals) )
	return vertex_normals / sqrt( (vertex_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )

def GetNormals3(  ) :
	tris = testmesh.vertices[ testmesh.faces ]
	face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	face_normals /= sqrt( (face_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )
	vertex_normals = zeros( testmesh.vertices.shape )
	vertex_normals[ testmesh.faces[:,0] ] += face_normals
	vertex_normals[ testmesh.faces[:,1] ] += face_normals
	vertex_normals[ testmesh.faces[:,2] ] += face_normals
	return vertex_normals / sqrt( (vertex_normals ** 2).sum( axis=1 ) ).reshape( -1, 1 )
		
	
	
