# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Mesh.py
#                             -------------------
#    update               : 2013-06-03
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
			"  Vertices : " + `self.VertexNumber()` + "\n"\
			"  Faces    : " + `self.FaceNumber()` + "\n"\
			"  Colors   : " + `len(self.colors)` + "\n"\
			"  FNormals : " + `len(self.face_normals)` + "\n"\
			"  VNormals : " + `len(self.vertex_normals)` + "\n"\
			"  Textures : " + `len(self.textures)` + "\n"\
			"  TextFile : " + self.texture_name
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

	#
	# ComputeFaceNormals
	#
	def ComputeFaceNormals( self ) :
		# Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle             
		self.face_normals = numpy.cross( self.vertices[self.faces[:,1]] - self.vertices[self.faces[:,0]],
						self.vertices[self.faces[:,2]] - self.vertices[self.faces[:,0]] )
		# Normalize the normal vectors
		for i in range( self.FaceNumber() ) :
			norm = numpy.linalg.norm( self.face_normals[i] )
			if norm != 0 : self.face_normals[i] *= 1 / norm
#		lengths = numpy.apply_along_axis( numpy.linalg.norm, self.face_normals.ndim - 1, self.face_normals )
#		lengths = lengths.repeat( self.face_normals.shape[-1] ).reshape( self.face_normals.shape )
#		face_normals /= lengths
		return self

	#
	# ComputeVertexNormals
	#
	def ComputeVertexNormals( self ) :
		# Compute face normals if necessary
		if len(self.face_normals) != len(self.faces) : self.ComputeFaceNormals()
		# Create a zeroed array
		self.vertex_normals = numpy.zeros( (self.VertexNumber(), 3), dtype=float )
		# Add face normals
		for i in range( self.FaceNumber() ) :
			self.vertex_normals[self.faces[i,0]] += self.face_normals[i]
			self.vertex_normals[self.faces[i,1]] += self.face_normals[i]
			self.vertex_normals[self.faces[i,2]] += self.face_normals[i]
		# Normalize the normal vectors
		for i in range( self.VertexNumber() ) :
			norm = numpy.linalg.norm( self.vertex_normals[i] )
			if norm != 0 : self.vertex_normals[i] *= 1/norm

		return self

	#
	# ComputeSmoothVertexNormals
	#
	def ComputeSmoothVertexNormals( self, smoothing_angle=90.0 ) :
		# 
		# Taken from "Smooth Normal Generation with Preservation of Edges" by Nate Robins
		# http://user.xmission.com/~nate/smooth.html
		# 
		# Compute face normals
		self.ComputeFaceNormals()
		# Collect vertex neighborhood informations
		self.CollectNeighbors()
		# Create a zeroed array
		self.vertex_normals = numpy.zeros( (self.VertexNumber(), 3), dtype=float )
		# Crease angle
		cos_angle = math.cos(smoothing_angle * math.pi / 180.0)
		return self

	#
	# CollectNeighbors
	#
	def CollectNeighbors( self ) :
		faces = getattr( self, 'faces' )
		neighbor_vertices = [ [] for i in xrange(self.VertexNumber()) ]
		neighbor_faces = [ [] for i in xrange(self.VertexNumber()) ]
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
		self.neighbor_vertices = [ list( set( i ) ) for i in neighbor_vertices ]
		self.neighbor_faces = [ list( set( i ) ) for i in neighbor_faces ]
		return self


