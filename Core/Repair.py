# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 Repair.py
#                             -------------------
#    update               : 2013-12-01
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
#
from .Mesh import Mesh
#from numpy import array, cross, dot, sqrt, zeros




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
#		face_normal = cross( mesh.vertices[ face[1] ] - mesh.vertices[ face[0] ],
#					mesh.vertices[ face[2] ] - mesh.vertices[ face[0] ] )
		# Normal vector length
#		if sqrt( dot(face_normal, face_normal) ) <= 0 : dvn.append( i )
#		if len(dvn) > 0 : log_message += '  Degenerated face normal : {}\n'.format(dvn)

	# Degenerate vertex normals
	if len(mesh.vertex_normals) > 0 :
		dvn = []
#		for (i, normal) in enumerate( mesh.vertex_normals ) :
#			length = sqrt( dot(normal, normal) )
#			# Normal vector length
#			if (length <= 0) or (length > 1.0001) : dvn.append( i )
#		if len(dvn) > 0 : log_message += '  Degenerated vertex normal :{}\n'.format(dvn)

	# Return silently if there is no error
	if not log_message : return

	# Print log message in case of errors
	print( '~~~ Mesh checking informations ~~~' )
	print( log_message )


#--
#
# CheckNeighborhood
#
#--
#
# Check neighborhood parameters
#
def CheckNeighborhood( mesh ) :

	log_message = ''

	# Check isolated vertices
	dvn = []
	for i,n in enumerate(mesh.neighbor_faces) :
		if len(n) == 0 : dvn.append( i )
	if dvn : log_message += '  Isolated vertices : {}\n'.format(dvn)

	# Return silently if there is no error
	if not log_message : return

	# Print log message in case of errors
	print( '~~~ Neighborhood checking informations ~~~' )
	print( log_message )


#--
#
# RemoveIsolatedVertices
#
#--
#
# Remove isolated vertices in the mesh
# TODO : colors and texture coordinates
#
def RemoveIsolatedVertices( mesh ) :

	# Register isolated vertices
	isolated_vertices = zeros( len(mesh.vertices), dtype=bool )
	for (i, neighbor) in enumerate( mesh.neighbor_faces ) :
		if not len(neighbor) : isolated_vertices[i] = True

	# Do nothing if there is no isolated vertex
	if not isolated_vertices.any() : return mesh

	# Create the new vertex array and a lookup table
	new_vertices = []
	index = 0
	lut = empty( len(mesh.vertices), dtype=int )
	for ( v, isolated ) in enumerate( isolated_vertices ) :
		if isolated : continue
		new_vertices.append( mesh.vertices[v] )
		lut[v] = index;
		index += 1

	# Create a new face array
	new_faces = lut[mesh.faces].reshape( len(mesh.faces), 3 )
	
	# Update the mesh
	mesh.vertices = array( new_vertices )
	mesh.faces = new_faces


#--
#
# InvertFaceOrientation
#
#--
#
# Invert orientation of every face in a given mesh
#
def InvertFaceOrientation( mesh ) :

	# Swap two vertices in each face
	for face in mesh.faces :
		face[0], face[1] = face[1], face[0]

	# Recompute face and vertex normals
	mesh.UpdateNormals()
