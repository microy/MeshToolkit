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
	# Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle             
	mesh.face_normals = numpy.cross( mesh.vertices[ mesh.faces[:,1] ] - mesh.vertices[ mesh.faces[:,0] ],
					mesh.vertices[ mesh.faces[:,2] ] - mesh.vertices[ mesh.faces[:,0] ] )
	# Initialize the vertex normal array
	mesh.vertex_normals = numpy.zeros( (len(mesh.vertices), 3) )
	# Add face normals to the normal of their respective vertices
	for ( i, face ) in enumerate( mesh.faces ) :
		mesh.vertex_normals[face] += mesh.face_normals[i]            
	# Normalize the normal vectors
	mesh.face_normals /= numpy.apply_along_axis( numpy.linalg.norm, 1, mesh.face_normals ).repeat( 3 ).reshape( mesh.face_normals.shape )
	mesh.vertex_normals /= numpy.apply_along_axis( numpy.linalg.norm, 1, mesh.vertex_normals ).repeat( 3 ).reshape( mesh.vertex_normals.shape )
	return mesh

#--
#
# UpdateNeighbors
#
#--
def UpdateNeighbors( mesh ) :
	# Initialization
	mesh.neighbor_vertices = [ [] for i in xrange(mesh.VertexNumber()) ]
	mesh.neighbor_faces = [ [] for i in xrange(mesh.VertexNumber()) ]
	# Create a list of faces and vertices in the neighborhood
	# for every vertex of the mesh
	for i in range( mesh.FaceNumber() ) :
		mesh.neighbor_faces[ mesh.faces[i,0] ].append( i )
		mesh.neighbor_faces[ mesh.faces[i,1] ].append( i )
		mesh.neighbor_faces[ mesh.faces[i,2] ].append( i )
		mesh.neighbor_vertices[ mesh.faces[i,0] ].append( mesh.faces[i,1] )
		mesh.neighbor_vertices[ mesh.faces[i,0] ].append( mesh.faces[i,2] )
		mesh.neighbor_vertices[ mesh.faces[i,1] ].append( mesh.faces[i,0] )
		mesh.neighbor_vertices[ mesh.faces[i,1] ].append( mesh.faces[i,2] )
		mesh.neighbor_vertices[ mesh.faces[i,2] ].append( mesh.faces[i,0] )
		mesh.neighbor_vertices[ mesh.faces[i,2] ].append( mesh.faces[i,1] )
	# Remove duplicates
	mesh.neighbor_vertices = [ list( set( i ) ) for i in mesh.neighbor_vertices ]
	mesh.neighbor_faces = [ list( set( i ) ) for i in mesh.neighbor_faces ]
	return mesh


