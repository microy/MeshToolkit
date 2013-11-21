# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                  Normal.py
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
from numpy import cross, zeros
from numpy.linalg import norm






#--
#
# UpdateNormals
#
#--
#
# Compute vertex normal vectors of a given mesh
#
def UpdateNormals( mesh ) :

	# Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle             
	mesh.face_normals = cross( mesh.vertices[ mesh.faces[:,1] ] - mesh.vertices[ mesh.faces[:,0] ],
					mesh.vertices[ mesh.faces[:,2] ] - mesh.vertices[ mesh.faces[:,0] ] )

	# Initialize the vertex normal array
	mesh.vertex_normals = zeros( (len(mesh.vertices), 3) )

	# Add face normals to the normal of their respective vertices
	for ( i, face ) in enumerate( mesh.faces ) :
		mesh.vertex_normals[ face ] += mesh.face_normals[ i ]

	# Normalize the normal vectors
	for i in range( len(mesh.face_normals) ) :
		mesh.face_normals[i] /= norm( mesh.face_normals[i] )
	for i in range( len(mesh.vertex_normals) ) :
		mesh.vertex_normals[i] /= norm( mesh.vertex_normals[i] )

#	mesh.face_normals /= numpy.apply_along_axis( numpy.linalg.norm, 1, mesh.face_normals ).repeat( 3 ).reshape( mesh.face_normals.shape )
#	mesh.vertex_normals /= numpy.apply_along_axis( numpy.linalg.norm, 1, mesh.vertex_normals ).repeat( 3 ).reshape( mesh.vertex_normals.shape )
#	mesh.face_normals /= numpy.apply_along_axis( numpy.linalg.norm, 1, mesh.face_normals )[:,numpy.newaxis]
#	mesh.vertex_normals /= numpy.apply_along_axis( numpy.linalg.norm, 1, mesh.vertex_normals )[:,numpy.newaxis]

	return mesh


