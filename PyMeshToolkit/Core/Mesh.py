# -*- coding:utf-8 -*-


#
# Provide a class to contain 3D triangular mesh data.
# Give some basic processing functions (normals, neighbors, bounding box...)
#


#
# External dependencies
#
from numpy import amin, amax, array, bincount, cross, sort, sqrt, zeros


#
# Define a class representing a triangular mesh
# The data are encapsulated into numpy arrays
#
class Mesh( object ) :

	#
	# Initialisation
	#
	def __init__( self, name='', vertices=[], faces=[], colors=[], texture_name='', textures=[], face_normals=[], vertex_normals=[] ) :

		# Mesh name
		self.name = name
		
		# Vertex array
		self.vertices = array( vertices )
		
		# Face index array
		self.faces = array( faces )
		
		# Per-vertex color array
		self.colors = array( colors )
		
		# Texture filename
		self.texture_name = texture_name
		
		# Per-vertex texture coordinate array
		self.textures = array( textures )
		
		# Per-face normal array
		self.face_normals = array( face_normals )
		
		# Per-vertex normal array
		self.vertex_normals = array( vertex_normals )

	#
	# Return mesh informations
	#
	def __str__( self ) :
		
		info   = '  Name :               {}\n'.format( self.name )
		info  += '  Vertices :           {}\n'.format( self.vertex_number )
		info  += '  Faces :              {}'.format( self.face_number )
		if len(self.colors) :
			info  += '\n  Colors :             {}'.format( self.color_number )
		if len(self.face_normals) :
			info  += '\n  Faces normals :      {}'.format( self.face_normal_number )
		if len(self.vertex_normals) :
			info  += '\n  Vertex normals :     {}'.format( self.vertex_normal_number )
		if len(self.textures) :
			info  += '\n  Textures :           {}'.format( self.texture_number )
		if self.texture_name :
			info  += '\n  Texture filename :   {}'.format( self.texture_name )
		return info

	#
	# Vertex number
	#
	@property
	def vertex_number( self ) :
		return len( self.vertices )

	#
	# Face number
	#
	@property
	def face_number( self ) :
		return len( self.faces )

	#
	# Color number
	#
	@property
	def color_number( self ) :
		return len( self.colors )

	#
	# Texture number
	#
	@property
	def texture_number( self ) :
		return len( self.textures )

	#
	# face normal number
	#
	@property
	def face_normal_number( self ) :
		return len( self.face_normals )

	#
	# Vertex normal number
	#
	@property
	def vertex_normal_number( self ) :
		return len( self.vertex_normals )

	#
	# Compute normal vectors of the faces and vertices
	#
	def UpdateNormals( self ) :

		# Create an indexed view of the triangles
		tris = self.vertices[ self.faces ]

		# Calculate the normal for all the triangles
		self.face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )

		# Normalise the face normals
		self.face_normals /= sqrt( ( self.face_normals ** 2 ).sum( axis=1 ) ).reshape( -1, 1 )

		# Initialise the vertex normals
		self.vertex_normals = zeros( self.vertices.shape )

		# Add the face normals to the vertex normals
		# Standard implementation :
		#	for i, f in enumerate( self.faces ) : self.vertex_normals[ f ] += self.face_normals[ i ]
		# Optimized implementation :
		for i in range( 3 ) :
			self.vertex_normals[:, i] += bincount( self.faces[:, 0], self.face_normals[:, i], minlength=self.vertex_number )
			self.vertex_normals[:, i] += bincount( self.faces[:, 1], self.face_normals[:, i], minlength=self.vertex_number )
			self.vertex_normals[:, i] += bincount( self.faces[:, 2], self.face_normals[:, i], minlength=self.vertex_number )
		
		# Normalise the vertex normals
		self.vertex_normals /= sqrt( ( self.vertex_normals ** 2 ).sum( axis=1 ) ).reshape( -1, 1 )


	#
	# Register neighborhood informations
	#
	def UpdateNeighbors( self ) :

		# Initialization
		self.neighbor_faces = [ set() for i in range(self.vertex_number) ]
		self.neighbor_vertices = [ set() for i in range(self.vertex_number) ]

		# Loop through the faces
		for i, (a, b ,c) in enumerate( self.faces ) :

			# Add faces bound to each vertex
			self.neighbor_faces[ a ].add( i )
			self.neighbor_faces[ b ].add( i )
			self.neighbor_faces[ c ].add( i )

			# Add vertices link by a face
			self.neighbor_vertices[ a ].add( b )
			self.neighbor_vertices[ a ].add( c )
			self.neighbor_vertices[ b ].add( a )
			self.neighbor_vertices[ b ].add( c )
			self.neighbor_vertices[ c ].add( a )
			self.neighbor_vertices[ c ].add( b )


	#
	# Collect the mesh edges
	#
	def GetEdges( self ) :

		# Edge dictionary
	#	edges = { e : {} for a, b in sort( self.faces )[:,[[0,0,1],[1,2,2]]] for e in zip(a,b) }

		# Edge set (unordered unique list)
	#	edges = set( e for a, b in sort( self.faces )[:,[[0,0,1],[1,2,2]]] for e in zip(a,b) )

		# Initialization
		edges = {}
		
		# Create an indexed view of the edges per face
		face_edges = [ zip(a,b) for a,b in sort( self.faces )[:,[[0,0,1],[1,2,2]]] ]

		# Create a dictionary of the mesh edges
		# and register associated faces
		for i, face_edge in enumerate( face_edges ) :
			for key in face_edge :
				if key not in edges :
					edges[key] = {}
					edges[key]['face'] = []
				edges[key]['face'].append( i )

		return edges


	#
	# Tell which vertex is on a border
	#
	def GetBorderVertices( self ) :
		
		border_vertices = zeros( self.vertex_number, dtype=bool )
		
		# Loop through the neighbor vertices
		for va, vn in enumerate( self.neighbor_vertices ) :
			for vb in vn :
				
				# Check the number of faces in common between the initial vertex and the neighbor
				if len( self.neighbor_faces[va] & self.neighbor_faces[vb] ) < 2 :
					border_vertices[ va ] = True
					break

		return border_vertices

	#
	# Compute the axis-aligned bounding box
	#
	def GetAxisAlignedBoundingBox( self ) :

		# Return the minimum point and the maximum point for each axis
		return ( amin( self.vertices, axis = 0 ), amax( self.vertices, axis = 0 ) )


	#
	# Compute (an approximation of) the bounding sphere
	#
	def GetBoundingSphere( self ) :

		# Compute axis-aligned bounding box
		( pmin, pmax ) = GetAxisAlignedBoundingBox( self )

		# Compute center
		center = 0.5 * (pmin + pmax)

		# Compute radius
		radius = sqrt(((center - self.vertices) ** 2).sum(axis = 1)).max()

		# Return result
		return ( center, radius )
