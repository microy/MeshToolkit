# -*- coding:utf-8 -*- 


#
# External dependencies
#
from numpy import amin, amax, array, bincount, cross, sort, sqrt, zeros


#
# Define a class representing a triangular mesh
#
class Mesh :


	#
	# Initialisation
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


	#
	# Print object informations
	#
	def __str__( self ) :
		
		log_message = '~~~ Mesh informations ~~~\n'
		log_message  += '  Name :               {}\n'.format( self.name )
		log_message  += '  Vertices :           {}\n'.format( len(self.vertices) )
		log_message  += '  Faces :              {}\n'.format( len(self.faces) )
		log_message  += '  Colors :             {}\n'.format( len(self.colors) )
		log_message  += '  Faces normals :      {}\n'.format( len(self.face_normals) )
		log_message  += '  Vertex normals :     {}\n'.format( len(self.vertex_normals) )
		log_message  += '  Textures :           {}\n'.format( len(self.textures) )
		log_message  += '  Texture filename :   {}'.format( self.texture_name )
		return log_message


	#
	# Compute normal vectors of the faces and vertices
	#
	def UpdateNormals( self ) :

		# Create an indexed view of the triangles
		tris = self.vertices[ self.faces ]

		# Calculate the normal for all the triangles
		self.face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )

		# Normalise the face normals
		self.face_normals /= sqrt( (self.face_normals ** 2).sum( axis=1 ) ).reshape( len(self.face_normals), 1 )

		# Initialise the vertex normals
		self.vertex_normals = zeros( self.vertices.shape )

		# Add the face normals to the vertex normals
		for i, (a, b, c) in enumerate( self.faces ) :
			self.vertex_normals[a] += self.face_normals[i]
			self.vertex_normals[b] += self.face_normals[i]
			self.vertex_normals[c] += self.face_normals[i]
		
		#~ for i in range(self.vertex_normals.shape[-1]) :
			#~ self.vertex_normals[:, i] += bincount( self.faces[:, 0], self.face_normals[:, i], minlength=len(self.vertex_normals) )
			#~ self.vertex_normals[:, i] += bincount( self.faces[:, 1], self.face_normals[:, i], minlength=len(self.vertex_normals) )
			#~ self.vertex_normals[:, i] += bincount( self.faces[:, 2], self.face_normals[:, i], minlength=len(self.vertex_normals) )
		
		# Bug :(
#		self.vertex_normals[ self.faces[:,0] ] += self.face_normals
#		self.vertex_normals[ self.faces[:,1] ] += self.face_normals
#		self.vertex_normals[ self.faces[:,2] ] += self.face_normals
		
		# Normalise the vertex normals
		self.vertex_normals /= sqrt( (self.vertex_normals ** 2).sum( axis=1 ) ).reshape( len(self.vertex_normals), 1 )


	#
	# Collect vertex neighborhoods of a given mesh
	#
	def UpdateNeighbors( self ) :

		# Initialization
		self.neighbor_vertices = [ [] for i in range(len( self.vertices )) ]
		self.neighbor_faces = [ [] for i in range(len( self.vertices )) ]

		# Loop through the faces
		for i, (a, b ,c) in enumerate( self.faces ) :

			# Add faces bound to each vertex
			self.neighbor_faces[ a ].append( i )
			self.neighbor_faces[ b ].append( i )
			self.neighbor_faces[ c ].append( i )

			# Add vertices link by a face
			self.neighbor_vertices[ a ].append( b )
			self.neighbor_vertices[ a ].append( c )
			self.neighbor_vertices[ b ].append( a )
			self.neighbor_vertices[ b ].append( c )
			self.neighbor_vertices[ c ].append( a )
			self.neighbor_vertices[ c ].append( b )

		# Remove duplicates
		self.neighbor_vertices =  [ set( i ) for i in self.neighbor_vertices ] 
		self.neighbor_faces =  [ set( i ) for i in self.neighbor_faces ] 


	#
	# Collect the mesh edges
	#
	def UpdateEdges( self ) :

		# Initialization
		self.edges = {}
		
		# Create an indexed view of the edges per face
		edges = sort( self.faces )[:,[[0,1],[0,2],[1,2]]]

		# Create a dictionary of the mesh edges
		for i, ef in enumerate( edges ) :
			for e in ef :
				edge = tuple( e )
				if edge not in self.edges :
					self.edges[edge] = {};
					self.edges[edge]['face'] = []
				self.edges[edge]['face'].append( i )


	#
	# Tell if a vertex is on a border
	#
	def IsBorderVertex( self, vertex ) :

		# Loop through the neighbor vertices
		for v in self.neighbor_vertices[ vertex ] :

			# Check the number of faces in common between the initial vertex and the neighbor
			if len(self.neighbor_faces[v] & self.neighbor_faces[vertex]) < 2 : return True

		# Otherwise, it is not on the border
		return False


	#
	# Compute the axis-aligned bounding box
	#
	def GetAxisAlignedBoundingBox( self ) :

		# Return the minimum point and the maximum point for each axis
		return ( amin( self.vertices, axis = 0 ), amax( self.vertices, axis = 0 ) )


	#
	# Compute the bounding sphere
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
