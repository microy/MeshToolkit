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
from Mesh import Mesh




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
	mesh.neighbor_vertices = [ list( set( i ) ) for i in mesh.neighbor_vertices ]
	mesh.neighbor_faces = [ list( set( i ) ) for i in mesh.neighbor_faces ]

	return mesh



