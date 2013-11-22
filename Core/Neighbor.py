# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 Neighbor.py
#                             -------------------
#    update               : 2013-11-22
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
from numpy import array, empty, zeros




#--
#
# UpdateNeighborhood
#
#--
#
# Collect vertex neighborhoods of a given mesh
#
def UpdateNeighborhood( mesh ) :

	# Initialization
	mesh.neighbor_vertices = [ [] for i in xrange(len(mesh.vertices)) ]
	mesh.neighbor_faces = [ [] for i in xrange(len(mesh.vertices)) ]

	# Create a list of neighbor vertices and faces for every vertex of the mesh
	for i in range( len(mesh.faces) ) :

		# Add faces bound to each vertex
		mesh.neighbor_faces[ mesh.faces[i,0] ].append( i )
		mesh.neighbor_faces[ mesh.faces[i,1] ].append( i )
		mesh.neighbor_faces[ mesh.faces[i,2] ].append( i )

		# Add vertices link by a face
		mesh.neighbor_vertices[ mesh.faces[i,0] ].append( mesh.faces[i,1] )
		mesh.neighbor_vertices[ mesh.faces[i,0] ].append( mesh.faces[i,2] )
		mesh.neighbor_vertices[ mesh.faces[i,1] ].append( mesh.faces[i,0] )
		mesh.neighbor_vertices[ mesh.faces[i,1] ].append( mesh.faces[i,2] )
		mesh.neighbor_vertices[ mesh.faces[i,2] ].append( mesh.faces[i,0] )
		mesh.neighbor_vertices[ mesh.faces[i,2] ].append( mesh.faces[i,1] )

	# Remove duplicates
	mesh.neighbor_vertices = [ array( list( set( i ) ) ) for i in mesh.neighbor_vertices ]
	mesh.neighbor_faces = [ array( list( set( i ) ) ) for i in mesh.neighbor_faces ]

	# Return the mesh with the neighborhood informations
	return mesh


#--
#
# RemoveIsolatedVertices
#
#--
#
# Remove isolated vertices in the mesh
#
def RemoveIsolatedVertices( mesh ) :

	# Register isolated vertices
	isolated_vertices = zeros( (len(mesh.vertices),1), dtype=bool )
	for i, n in enumerate( mesh.neighbor_faces ) :
		if len(n) == 0 : isolated_vertices[i] = True

	# Do nothing if there is no isolated vertex
	if not isolated_vertices.any() : return

	# Create the new vertex array
	new_vertices = []
	for (v, isolated) in enumerate(isolated_vertices) :
		if not isolated : new_vertices.append(mesh.vertices[v])

	# Create a lookup table for the vertex indices
	lut = empty( (len(mesh.vertices),1), dtype=int )
	index = 0
	for (v, isolated) in enumerate(isolated_vertices) :
		if isolated : lut[v] = -1
		else :
			lut[v] = index
			index += 1
	
	# Create a new face array
	new_faces = lut[mesh.faces].reshape( len(mesh.faces), 3 )
	
	# Update the mesh
	mesh.vertices = array( new_vertices )
	mesh.faces = new_faces

	# Remove previous normals
	mesh.vertex_normals = []
	mesh.face_normals = []




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
	print '~~~ Neighborhood checking informations ~~~\n'
	print log_message





#--
#
# IsBorderVertex
#
#--
#
# Return true if the vertex is on a border edge
#
def IsBorderVertex( mesh, vertex ) :

	# Loop through the neighbor vertices
	for v in mesh.neighbor_vertices[ vertex ] :

		common_face = 0

		# Loop through the neighbor faces
		for f1 in mesh.neighbor_faces[ v ] :

			for f2 in mesh.neighbor_faces[ vertex ] :

				# Check if it has a face in common
				if f1 == f2 : common_face += 1

		# If there is only 1 common face with this neighbor,
		# it is a vertex on the border
		if common_face < 2 : return True

	# Otherwise, it is not on the border
	return False


