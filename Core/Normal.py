# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                  Normal.py
#                             -------------------
#    update               : 2013-11-23
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
from numpy import cross, zeros, sqrt






#--
#
# UpdateNormals
#
#--
#
# Compute vertex normal vectors of a given mesh
#
def UpdateNormals( mesh ) :

	# Create an indexed view of the triangles
	tris = mesh.vertices[ mesh.faces ]

	# Calculate the normal for all the triangles
	mesh.face_normals = cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )

	# Normalise the face normals
	lengths = sqrt( (mesh.face_normals ** 2).sum( axis=1 ) )
	mesh.face_normals /= lengths.reshape( len(mesh.face_normals), 1 )

	# Intialise the vertex normals
	mesh.vertex_normals = zeros( mesh.vertices.shape, dtype=mesh.vertices.dtype )

	# Add the face normals to the vertex normals
	mesh.vertex_normals[ mesh.faces[:,0] ] += mesh.face_normals
	mesh.vertex_normals[ mesh.faces[:,1] ] += mesh.face_normals
	mesh.vertex_normals[ mesh.faces[:,2] ] += mesh.face_normals

	# Normalise the vertex normals
	lengths = sqrt( (mesh.vertex_normals ** 2).sum( axis=1 ) )
	mesh.vertex_normals /= lengths.reshape( len(mesh.vertex_normals), 1 )

	# Return the mesh with the new normals
	return mesh



