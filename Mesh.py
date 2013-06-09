# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Mesh.py
#                             -------------------
#    update               : 2013-06-09
#    copyright            : (C) 2013 by Michaël Roy
#    email                : microygh@gmail.com
# ***************************************************************************

# ***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************





#--
#
# Mesh
#
#--
#
# Define a class representing a triangular mesh
# This class only contains member variables
# All processing functions are elsewhere
#
class Mesh :

	#
	# Initialisation
	#
	def __init__( self, name='', vertices=[], faces=[], colors=[], textures=[], face_normals=[], vertex_normals=[], texture_name='' ) :
		self.name = name
		self.vertices = vertices
		self.faces = faces
		self.colors = colors
		self.textures = textures
		self.texture_name = texture_name
		self.face_normals = face_normals
		self.vertex_normals = vertex_normals
		self.neighbor_faces = []
		self.neighbor_vertices = []

	#
	# Display
	#
	def __str__( self ) :
		string = 'Mesh ' + self.name + '\n'\
			'  Vertices :         ' + `len(self.vertices)` + '\n'\
			'  Faces :            ' + `len(self.faces)` + '\n'\
			'  Colors :           ' + `len(self.colors)` + '\n'\
			'  Faces normals :    ' + `len(self.face_normals)` + '\n'\
			'  Vertex normals :   ' + `len(self.vertex_normals)` + '\n'\
			'  Textures :         ' + `len(self.textures)` + '\n'\
			'  Texture filename : ' + self.texture_name + '\n'\
			'  Neighbors :        ' + `len( self.neighbor_vertices )`
	        return string


