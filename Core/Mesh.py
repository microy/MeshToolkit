# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Mesh.py
#                             -------------------
#    update               : 2013-11-19
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


#-
#
# External dependencies
#
#-
from numpy import cross
from numpy.linalg import norm




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
	def __init__( self, name='', vertices=[], faces=[], colors=[], texture_name='', textures=[], face_normals=[], vertex_normals=[] ) :
		self.name = name
		self.vertices = vertices
		self.faces = faces
		self.colors = colors
		self.texture_name = texture_name
		self.textures = textures
		self.face_normals = face_normals
		self.vertex_normals = vertex_normals

	#
	# Display
	#
	def __str__( self ) :
		string = '~~~ Mesh informations ~~~\n' +\
			'  Filename :         ' + self.name + '\n'\
			'  Vertices :         ' + `len(self.vertices)` + '\n'\
			'  Faces :            ' + `len(self.faces)` + '\n'\
			'  Colors :           ' + `len(self.colors)` + '\n'\
			'  Faces normals :    ' + `len(self.face_normals)` + '\n'\
			'  Vertex normals :   ' + `len(self.vertex_normals)` + '\n'\
			'  Textures :         ' + `len(self.textures)` + '\n'\
			'  Texture filename : ' + self.texture_name
	        return string





#--
#
# CheckMesh
#
#--
#
# Check several parameters of a given mesh
#
def CheckMesh( mesh ) :

	# Initialisation
	vertex_number = len( mesh.vertices )
	face_number = len( mesh.faces )
	log_message = ''

	# Vertex number
	if vertex_number < 3 :
		log_message += '  Not enough vertices ({})\n'.format( vertex_number )

	# Face number
	if face_number < 1 :
		log_message += '  Not enough faces ({})\n'.format( face_number )

	# Face normal number
	if ( len(mesh.face_normals) > 0 ) and ( len(mesh.face_normals) != face_number ) :
		log_message += '  Face normal number doesn\'t match face number ({}/{})\n'.format( len(mesh.face_normals), face_number )

	# Vertex normal number
	if ( len(mesh.vertex_normals) > 0 ) and ( len(mesh.vertex_normals) != vertex_number ) :
		log_message += '  Vertex normal number doesn\'t match vertex number ({}/{})\n'.format( len(mesh.vertex_normals), vertex_number )

	# Color number
	if ( len(mesh.colors) > 0 ) and ( len(mesh.colors) != vertex_number ) :
		log_message += '  Color number doesn\'t match vertex number ({}/{})\n'.format( len(mesh.colors), vertex_number )

	# Texture coordinate number
	if ( len(mesh.textures) > 0 ) and ( len(mesh.textures) != vertex_number ) :
		log_message += '  Texture coordinate number doesn\'t match vertex number ({}/{})\n'.format( len(mesh.textures), vertex_number )

	# Texture filename
	if ( len(mesh.textures) > 0 ) and ( mesh.texture_name == '' ) :
		log_message += '  Empty texture filename\n'

	# Face indices
	if ( mesh.faces < 0 ).any() or ( mesh.faces >= vertex_number ).any() :
		log_message += '  Wrong face indices\n'

	# Degenerate face
	for (i, face) in enumerate( mesh.faces ) :
		dvn = []
		# Calculate face normal vector           
		face_normal = cross( mesh.vertices[ face[1] ] - mesh.vertices[ face[0] ],
					mesh.vertices[ face[2] ] - mesh.vertices[ face[0] ] )
		# Normal vector length
		if norm( face_normal ) <= 0 : dvn.append( i )
		if len(dvn) > 0 : log_message += '  Degenerated face normal : {}\n'.format(dvn)

	# Degenerate vertex normals
	if len(mesh.vertex_normals) > 0 :
		dvn = []
		for (i, normal) in enumerate( mesh.vertex_normals ) :
			length = norm( normal )
			# Normal vector length
			if (length <= 0) or (length > 1) : dvn.append( i )
		if len(dvn) > 0 : log_message += '  Degenerated vertex normal :{}\n'.format(dvn)

	# Return silently if there is no error
	if not log_message : return True

	# Print log message in case of errors
	print '~~~ Mesh checking informations ~~~\n'
	print log_message

