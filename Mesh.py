# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Mesh.py
#                             -------------------
#    update               : 2013-11-13
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


#
# External dependencies
#
import numpy




#--
#
# Mesh
#
#--
#
# Defines a class representing a triangular mesh
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

	#
	# Display
	#
	def __str__( self ) :
		string = 'Mesh ' + self.name + '\n'\
			'  Vertices            ' + `len(self.vertices)` + '\n'\
			'  Faces               ' + `len(self.faces)` + '\n'\
			'  Colors              ' + `len(self.colors)` + '\n'\
			'  Faces normals       ' + `len(self.face_normals)` + '\n'\
			'  Vertex normals      ' + `len(self.vertex_normals)` + '\n'\
			'  Textures            ' + `len(self.textures)` + '\n'\
			'  Texture filename    ' + self.texture_name
	        return string



#--
#
# CheckMesh
#
#--
#
# Defines a function that checks several parameters
# of a given mesh
#
def CheckMesh( mesh ) :
	# Initialisation
	vertex_number = len( mesh.vertices )
	face_number = len( mesh.faces )
	# Vertex number
	if vertex_number < 3 :
		raise RuntimeError( 'Error: Not enough vertices ({})'.format( vertex_number ) )
	# Face number
	if face_number < 1 :
		raise RuntimeError( 'Error: Not enough faces ({})'.format( face_number ) )
	# Face normal number
	if ( len(mesh.face_normals) > 0 ) and ( len(mesh.face_normals) != face_number ) :
		raise RuntimeError( 'Error: Face normal number doesn\'t match face number ({}/{})'.format( len(mesh.face_normals), face_number ) )
	# Vertex normal number
	if ( len(mesh.vertex_normals) > 0 ) and ( len(mesh.vertex_normals) != vertex_number ) :
		raise RuntimeError( 'Error: Vertex normal number doesn\'t match vertex number ({}/{})'.format( len(mesh.vertex_normals), vertex_number ) )
	# Color number
	if ( len(mesh.colors) > 0 ) and ( len(mesh.colors) != vertex_number ) :
		raise RuntimeError( 'Error: Color number doesn\'t match vertex number ({}/{})'.format( len(mesh.colors), vertex_number ) )
	# Texture coordinate number
	if ( len(mesh.textures) > 0 ) and ( len(mesh.textures) != vertex_number ) :
		raise RuntimeError( 'Error: Texture coordinate number doesn\'t match vertex number ({}/{})'.format( len(mesh.textures), vertex_number ) )
	# Texture filename
	if ( len(mesh.textures) > 0 ) and ( mesh.texture_name == '' ) :
		raise RuntimeError( 'Error: Empty texture filename' )
	# Face indices
	if ( mesh.faces < 0 ).any() or ( mesh.faces >= vertex_number ).any() :
		raise RuntimeError( 'Error: Wrong face indices' )
	# Degenerate face
	for (i, face) in enumerate( mesh.faces ) :
		# Calculate face normal vector           
		face_normal = numpy.cross( mesh.vertices[ face[1] ] - mesh.vertices[ face[0] ],
					mesh.vertices[ face[2] ] - mesh.vertices[ face[0] ] )
		# Normal vector length
		if numpy.linalg.norm( face_normal ) == 0 :
			raise RuntimeError( 'Error: Face {} is degenerate'.format(i) )
	# Degenerate vertex normals
	if len(mesh.vertex_normals) > 0 :
		for (i, normal) in enumerate( mesh.vertex_normals ) :
			# Normal vector length
			if numpy.linalg.norm( normal ) == 0 :
				raise RuntimeError( 'Error: Null vertex normal {}'.format(i) )

