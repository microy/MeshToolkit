# -*- coding:utf-8 -*- 

# ***************************************************************************
#                               Neighborhood.py
#                             -------------------
#    update               : 2013-06-07
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
import Mesh



#--
#
# UpdateNeighbors
#
#--
def UpdateNeighbors( mesh ) :
	# Initialization
	mesh.neighbor_vertices = [ [] for i in xrange(mesh.VertexNumber()) ]
	mesh.neighbor_faces = [ [] for i in xrange(mesh.VertexNumber()) ]
	# Create a list of neighbor vertices and faces for every vertex of the mesh
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
#	mesh.neighbor_faces = [ list( set( i ) ) for i in mesh.neighbor_faces ] # Useless ?!
	return mesh


