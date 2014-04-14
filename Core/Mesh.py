# -*- coding:utf-8 -*- 


# ***************************************************************************
#                                   Mesh.py
#                             -------------------
#    update               : 2014-04-14
#    copyright            : (C) 2013-2014 by Michaël Roy
#    email                : microygh@gmail.com
# ***************************************************************************


#-
#
# External dependencies
#
#-
#
from numpy import array, cross, sqrt, zeros, amin, amax


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
		
		# Return mesh informations
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
		self.neighbor_vertices = [ [] for i in range(len( self.vertices )) ]
		self.neighbor_faces = [ [] for i in range(len( self.vertices )) ]

		# Create a list of neighbor vertices and faces for every vertex of the mesh
		for i in range(len( self.faces )) :

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
		self.neighbor_vertices =  [ set( i ) for i in self.neighbor_vertices ] 
		self.neighbor_faces =  [ set( i ) for i in self.neighbor_faces ] 


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

			# Check the number of faces in common between the initial vertex and the neighbor
			if len(self.neighbor_faces[v] & self.neighbor_faces[vertex]) < 2 : return True

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

		# Return the minimum point and the maximum point for each axis
		return ( amin( self.vertices, axis = 0 ), amax( self.vertices, axis = 0 ) )


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
		radius = sqrt(((center - self.vertices) ** 2).sum(axis = 1)).max()

		# Return result
		return ( center, radius )
