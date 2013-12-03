# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 Repair.py
#                             -------------------
#    update               : 2013-12-03
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
from numpy import array, isfinite, zeros


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
	log_message = ''

	# Vertex number
	if len(mesh.vertices) < 3 :
		log_message += 'Not enough vertices\n'

	# Face number
	if len(mesh.faces) < 1 :
		log_message += 'Not enough faces\n'

	# Face normal number
	if len(mesh.face_normals) and (len(mesh.face_normals) != len(mesh.faces)) :
		log_message += 'Face normal number doesn\'t match face number\n'

	# Vertex normal number
	if len(mesh.vertex_normals) and (len(mesh.vertex_normals) != len(mesh.vertices)) :
		log_message += 'Vertex normal number doesn\'t match vertex number\n'

	# Color number
	if len(mesh.colors) and (len(mesh.colors) != len(mesh.vertices)) :
		log_message += 'Color number doesn\'t match vertex number\n'

	# Texture coordinate number
	if len(mesh.textures) and (len(mesh.textures) != len(mesh.vertices)) :
		log_message += 'Texture coordinate number doesn\'t match vertex number\n'

	# Texture filename
	if len(mesh.textures) and not mesh.texture_name :
		log_message += 'Empty texture filename\n'

	# Face indices
	if (mesh.faces < 0).any() or (mesh.faces >= len(mesh.vertices)).any() :
		log_message += 'Bad face indices\n'

	# Vertex coordinates
	if not isfinite(mesh.vertices).all() :
		log_message += 'Bad vertex coordinates\n'
			
	# Face normals
	if not isfinite(mesh.face_normals).all() :
		log_message += 'Bad face normals\n'
			
	# Vertex normals
	if not isfinite(mesh.vertex_normals).all() :
		log_message += 'Bad vertex normals\n'
			
	# Colors
	if (mesh.colors < 0).any() or (mesh.colors > 1).any() :
		log_message += 'Bad color values\n'

	# Texture coordinates
	if (mesh.textures < 0).any() or (mesh.textures > 1).any() :
		log_message += 'Bad texture coordinates\n'

	# Return the log message
	return log_message


#--
#
# CheckNeighborhood
#
#--
#
# Check neighborhood parameters
#
def CheckNeighborhood( mesh ) :

	# Initialization
	log_message = ''

	# Check isolated vertices
	if (array([len(neighbor) for neighbor in mesh.neighbor_faces]) == 0).any() :
		log_message += 'Isolated vertices\n'

	# Return the log message
	return log_message


#--
#
# RemoveIsolatedVertices
#
#--
#
# Remove isolated vertices in the mesh
# TODO : process colors and texture coordinates
#
def RemoveIsolatedVertices( mesh ) :

	# Register isolated vertices
	isolated_vertices = (array([len(neighbor) for neighbor in mesh.neighbor_faces]) == 0)

	# Do nothing if there is no isolated vertex
	if not isolated_vertices.any() : return

	# Create the new vertex array and a lookup table
	new_vertices = []
	index = 0
	lut = zeros( len(mesh.vertices), dtype=int )
	for ( v, isolated ) in enumerate( isolated_vertices ) :
		if isolated : continue
		new_vertices.append( mesh.vertices[v] )
		lut[v] = index
		index += 1

	# Create a new face array
	new_faces = lut[mesh.faces].reshape( len(mesh.faces), 3 )
	
	# Update the mesh
	mesh.vertices = array( new_vertices )
	mesh.faces = new_faces
	mesh.UpdateNormals()
	mesh.UpdateNeighbors()


#--
#
# InvertFacesOrientation
#
#--
#
# Invert orientation of every face in a given mesh
#
def InvertFacesOrientation( mesh ) :

	# Swap two vertices in each face
	for face in mesh.faces : face[0], face[1] = face[1], face[0]

	# Recompute face and vertex normals
	mesh.UpdateNormals()
