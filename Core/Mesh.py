# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Mesh.py
#                             -------------------
#    update               : 2013-11-18
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
	mesh.face_normals = numpy.cross( mesh.vertices[ mesh.faces[:,1] ] - mesh.vertices[ mesh.faces[:,0] ],
					mesh.vertices[ mesh.faces[:,2] ] - mesh.vertices[ mesh.faces[:,0] ] )
	# Initialize the vertex normal array
	mesh.vertex_normals = numpy.zeros( (len(mesh.vertices), 3) )
	# Add face normals to the normal of their respective vertices
	for ( i, face ) in enumerate( mesh.faces ) :
		mesh.vertex_normals[ face ] += mesh.face_normals[ i ]
	# Normalize the normal vectors
	for i in range( len(mesh.face_normals) ) :
		mesh.face_normals[i] /= numpy.linalg.norm( mesh.face_normals[i] )
	for i in range( len(mesh.vertex_normals) ) :
		mesh.vertex_normals[i] /= numpy.linalg.norm( mesh.vertex_normals[i] )
#	mesh.face_normals /= numpy.apply_along_axis( numpy.linalg.norm, 1, mesh.face_normals ).repeat( 3 ).reshape( mesh.face_normals.shape )
#	mesh.vertex_normals /= numpy.apply_along_axis( numpy.linalg.norm, 1, mesh.vertex_normals ).repeat( 3 ).reshape( mesh.vertex_normals.shape )
#	mesh.face_normals /= numpy.apply_along_axis( numpy.linalg.norm, 1, mesh.face_normals )[:,numpy.newaxis]
#	mesh.vertex_normals /= numpy.apply_along_axis( numpy.linalg.norm, 1, mesh.vertex_normals )[:,numpy.newaxis]
	return mesh




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
	log_message = '~~~ Mesh checking informations ~~~\n'

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
		face_normal = numpy.cross( mesh.vertices[ face[1] ] - mesh.vertices[ face[0] ],
					mesh.vertices[ face[2] ] - mesh.vertices[ face[0] ] )
		# Normal vector length
		if numpy.linalg.norm( face_normal ) <= 0 : dvn.append( i )
		if len(dvn) > 0 : log_message += '  Degenerated face normal : {}\n'.format(dvn)
	# Degenerate vertex normals
	if len(mesh.vertex_normals) > 0 :
		dvn = []
		for (i, normal) in enumerate( mesh.vertex_normals ) :
			# Normal vector length
			if numpy.linalg.norm( normal ) <= 0 : dvn.append( i )
		if len(dvn) > 0 : log_message += '  Degenerated vertex normal :{}\n'.format(dvn)

	print log_message

