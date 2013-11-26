# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Mesh.py
#                             -------------------
#    update               : 2013-11-26
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
from numpy import array, cross, dot, sqrt, zeros, inf
from numpy.linalg import norm


#--
#
# Mesh
#
#--
#
# Defines a class representing a triangular mesh
#
class Mesh :


	#--
	#
	# Initialisation
	#
	#--
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
		self.neighbor_vertices = []
		self.neighbor_faces = []


	#--
	#
	# Display
	#
	#--
	#
	def __str__( self ) :
		
		# Return OpenGL driver informations
		log_message = '~~~ Mesh informations ~~~\n'
		log_message  += '  Name :             {}\n'.format( self.name )
		log_message  += '  Vertices :         {}\n'.format( len(self.vertices) )
		log_message  += '  Faces :            {}\n'.format( len(self.faces) )
		log_message  += '  Colors :           {}\n'.format( len(self.colors) )
		log_message  += '  Faces normals :    {}\n'.format( len(self.face_normals) )
		log_message  += '  Vertex normals :   {}\n'.format( len(self.vertex_normals) )
		log_message  += '  Textures :         {}\n'.format( len(self.textures) )
		log_message  += '  Texture filename : {}'.format( self.texture_name )
		return log_message


	#--
	#
	# UpdateNormals
	#
	#--
	#
	# Compute vertex normal vectors of a given mesh
	#
	def UpdateNormals( self ) :

		# Create an indexed view of the triangles
		tris = self.vertices[ self.faces ]

		# Calculate the normal for all the triangles
		self.face_normals = cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )

		# Normalise the face normals
		self.face_normals /= sqrt( (self.face_normals ** 2).sum( axis=1 ) ).reshape( len(self.face_normals), 1 )

		# Intialise the vertex normals
		self.vertex_normals = zeros( self.vertices.shape, dtype=self.vertices.dtype )

		# Add the face normals to the vertex normals
		self.vertex_normals[ self.faces[:,0] ] += self.face_normals
		self.vertex_normals[ self.faces[:,1] ] += self.face_normals
		self.vertex_normals[ self.faces[:,2] ] += self.face_normals

		# Normalise the vertex normals
		self.vertex_normals /= sqrt( (self.vertex_normals ** 2).sum( axis=1 ) ).reshape( len(self.vertex_normals), 1 )


	#--
	#
	# UpdateNeighbors
	#
	#--
	#
	# Collect vertex neighborhoods of a given mesh
	#
	def UpdateNeighbors( self ) :

		# Initialization
		self.neighbor_vertices = [ [] for i in range(len(self.vertices)) ]
		self.neighbor_faces = [ [] for i in range(len(self.vertices)) ]

		# Create a list of neighbor vertices and faces for every vertex of the mesh
		for i in range( len(self.faces) ) :

			# Add faces bound to each vertex
			self.neighbor_faces[ self.faces[i,0] ].append( i )
			self.neighbor_faces[ self.faces[i,1] ].append( i )
			self.neighbor_faces[ self.faces[i,2] ].append( i )

			# Add vertices link by a face
			self.neighbor_vertices[ self.faces[i,0] ].append( self.faces[i,1] )
			self.neighbor_vertices[ self.faces[i,0] ].append( self.faces[i,2] )
			self.neighbor_vertices[ self.faces[i,1] ].append( self.faces[i,0] )
			self.neighbor_vertices[ self.faces[i,1] ].append( self.faces[i,2] )
			self.neighbor_vertices[ self.faces[i,2] ].append( self.faces[i,0] )
			self.neighbor_vertices[ self.faces[i,2] ].append( self.faces[i,1] )

		# Remove duplicates
		self.neighbor_vertices = [ array( list( set( i ) ) ) for i in self.neighbor_vertices ]
		self.neighbor_faces = [ array( list( set( i ) ) ) for i in self.neighbor_faces ]


	#--
	#
	# IsBorderVertex
	#
	#--
	#
	# Return true if the vertex is on a border edge
	#
	def IsBorderVertex( self, vertex ) :

		# Loop through the neighbor vertices
		for v in self.neighbor_vertices[ vertex ] :

			common_face = 0

			# Loop through the neighbor faces
			for f1 in self.neighbor_faces[ v ] :

				for f2 in self.neighbor_faces[ vertex ] :

					# Check if it has a face in common
					if f1 == f2 : common_face += 1

			# If there is only 1 common face with this neighbor,
			# it is a vertex on the border
			if common_face < 2 : return True

		# Otherwise, it is not on the border
		return False


	#--
	#
	# GetAxisAlignedBoundingBox
	#
	#--
	#
	# Compute the axis-aligned bounding box of a given mesh
	#
	def GetAxisAlignedBoundingBox( self ) :

		# Initialisation
		min_point = array( [+inf, +inf, +inf] )
		max_point = array( [-inf, -inf, -inf] )

		# Loop through mesh vertices
		for v in self.vertices :
			for i in range( 3 ) :
				if v[i] < min_point[i] : min_point[i] = v[i]
				if v[i] > max_point[i] : max_point[i] = v[i]

		# Return result
		return ( min_point, max_point )


	#--
	#
	# GetBoundingSphere
	#
	#--
	#
	# Compute the bounding sphere of a given mesh
	#
	def GetBoundingSphere( self ) :

		# Compute axis-aligned bounding box
		( pmin, pmax ) = self.GetAxisAlignedBoundingBox()

		# Compute center
		center = 0.5 * (pmin + pmax)

		# Compute radius
		radius = 0.0
		for v in self.vertices :
			radius = max( radius, norm( center - v ) )

		# Return result
		return ( center, radius )


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
		if sqrt( dot(face_normal, face_normal) ) <= 0 : dvn.append( i )
		if len(dvn) > 0 : log_message += '  Degenerated face normal : {}\n'.format(dvn)

	# Degenerate vertex normals
	if len(mesh.vertex_normals) > 0 :
		dvn = []
		for (i, normal) in enumerate( mesh.vertex_normals ) :
			length = sqrt( dot(normal, normal) )
			# Normal vector length
			if (length <= 0) or (length > 1.0001) : dvn.append( i )
		if len(dvn) > 0 : log_message += '  Degenerated vertex normal :{}\n'.format(dvn)

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



