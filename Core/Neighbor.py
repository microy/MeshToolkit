# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 Neighbor.py
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
#
from numpy import array




#--
#
# UpdateNeighbors
#
#--
#
# Collect vertex neighborhoods of a given mesh
#
def UpdateNeighbors( mesh ) :

	# Initialization
	mesh.neighbor_vertices = [ [] for i in xrange(len(mesh.vertices)) ]
	mesh.neighbor_faces = [ [] for i in xrange(len(mesh.vertices)) ]

	# Create a list of neighbor vertices and faces for every vertex of the mesh
	for i in range( len(mesh.faces) ) :
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
	mesh.neighbor_vertices = [ array( list( set( i ) ) ) for i in mesh.neighbor_vertices ]
	mesh.neighbor_faces = [ array( list( set( i ) ) ) for i in mesh.neighbor_faces ]

	# Return the mesh with the neighborhood informations
	return mesh






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


