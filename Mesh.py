# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Mesh.py
#                             -------------------
#    update               : 2013-06-04
#    copyright            : (C) 2013 by Michaël Roy
#    email                : microygt@gmail.com
# ***************************************************************************

# ***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************


#
# External dependencies
#
import math
import numpy


#--
#
# Mesh
#
#--
class Mesh :

	#
	# Initialisation
	#
	def __init__( self, name="", vertices=[], faces=[], colors=[], textures=[], face_normals=[], vertex_normals=[], texture_name="" ) :
		self.name = name
		self.vertices = vertices
		self.faces = faces
		self.colors = colors
		self.textures = textures
		self.face_normals = face_normals
		self.vertex_normals = vertex_normals
		self.texture_name = texture_name
		self.neighbor_faces = []
		self.neighbor_vertices = []

	#
	# Display
	#
	def __repr__( self ) :
		string = "Mesh " + self.name + "\n"\
			"  Vertices  : " + `self.VertexNumber()` + "\n"\
			"  Faces     : " + `self.FaceNumber()` + "\n"\
			"  Colors    : " + `len(self.colors)` + "\n"\
			"  FNormals  : " + `len(self.face_normals)` + "\n"\
			"  VNormals  : " + `len(self.vertex_normals)` + "\n"\
			"  Textures  : " + `len(self.textures)` + "\n"\
			"  TextFile  : " + self.texture_name + "\n"\
			"  Neighbors : " + `len( self.neighbor_vertices )`
	        return string

	#
	# VertexNumber
	#
	def VertexNumber( self ) :
		return len( self.vertices )

	#
	# FaceNumber
	#
	def FaceNumber( self ) :
		return len( self.faces )




#--
#
# UpdateNormals
#
#--
def UpdateNormals( mesh ) :
	# Get data
	vertices = m.vertices
	faces = m.faces
	# Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle             
	mesh.face_normals = numpy.cross( vertices[ faces[:,1] ] - vertices[ faces[:,0] ],
					vertices[ faces[:,2] ] - vertices[ faces[:,0] ] )
	# Normalize the normal vectors
	for i in range( len ( faces ) ) :
		norm = numpy.linalg.norm( mesh.face_normals[i] )
		if norm != 0 : mesh.face_normals[i] *= 1 / norm
# TODO:
#	lengths = numpy.apply_along_axis( numpy.linalg.norm, self.face_normals.ndim - 1, self.face_normals )
#	lengths = lengths.repeat( self.face_normals.shape[-1] ).reshape( self.face_normals.shape )
#	face_normals /= lengths
	# Create a zeroed array
	mesh.vertex_normals = numpy.zeros( (len( vertices ), 3), dtype=float )
	# Add face normals
	for i in range( len( faces ) ) :
		mesh.vertex_normals[ faces[i,0] ] += mesh.face_normals[ i ]
		mesh.vertex_normals[ faces[i,1] ] += mesh.face_normals[ i ]
		mesh.vertex_normals[ faces[i,2] ] += mesh.face_normals[ i ]
	# Normalize the normal vectors
	for i in range( len( vertices ) ) :
		norm = numpy.linalg.norm( mesh.vertex_normals[i] )
		if norm != 0 : mesh.vertex_normals[i] *= 1/norm
# TODO:
#	for (i,face) in enumerate(faces):
#		vertex_normals[face]+=face_normals[i]            
#	div=np.sqrt(np.sum(normals**2,axis=1))     
#	div=div.reshape(len(div),1)
#	normals=(normals/div)
	return mesh

#--
#
# UpdateNeighbors
#
#--
def UpdateNeighbors( mesh ) :
	# Get data
	faces = m.faces
	neighbor_vertices = [ [] for i in xrange(mesh.VertexNumber()) ]
	neighbor_faces = [ [] for i in xrange(mesh.VertexNumber()) ]
	# Create a list of faces and vertices in the neighborhood
	# for every vertex of the mesh
	for i in range( self.FaceNumber() ) :
		neighbor_faces[ faces[i,0] ].append( i )
		neighbor_faces[ faces[i,1] ].append( i )
		neighbor_faces[ faces[i,2] ].append( i )
		neighbor_vertices[ faces[i,0] ].append( faces[i,1] )
		neighbor_vertices[ faces[i,0] ].append( faces[i,2] )
		neighbor_vertices[ faces[i,1] ].append( faces[i,0] )
		neighbor_vertices[ faces[i,1] ].append( faces[i,2] )
		neighbor_vertices[ faces[i,2] ].append( faces[i,0] )
		neighbor_vertices[ faces[i,2] ].append( faces[i,1] )
	# Remove duplicates
	mesh.neighbor_vertices = [ list( set( i ) ) for i in neighbor_vertices ]
	mesh.neighbor_faces = [ list( set( i ) ) for i in neighbor_faces ]
	return mesh


