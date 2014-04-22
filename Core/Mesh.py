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
	# Return mesh informations
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
		self.face_normals /= sqrt( ( self.face_normals ** 2 ).sum( axis=1 ) ).reshape( -1, 1 )

		# Initialise the vertex normals
		self.vertex_normals = zeros( self.vertices.shape )

		# Add the face normals to the vertex normals
		for i, f in enumerate( self.faces ) : self.vertex_normals[ f ] += self.face_normals[ i ]
		
		#~ for i in range(self.vertex_normals.shape[-1]) :
			#~ self.vertex_normals[:, i] += bincount( self.faces[:, 0], self.face_normals[:, i], minlength=len(self.vertex_normals) )
			#~ self.vertex_normals[:, i] += bincount( self.faces[:, 1], self.face_normals[:, i], minlength=len(self.vertex_normals) )
			#~ self.vertex_normals[:, i] += bincount( self.faces[:, 2], self.face_normals[:, i], minlength=len(self.vertex_normals) )
		
		# Bug :(
#		self.vertex_normals[ self.faces[:,0] ] += self.face_normals
#		self.vertex_normals[ self.faces[:,1] ] += self.face_normals
#		self.vertex_normals[ self.faces[:,2] ] += self.face_normals
		
		# Normalise the vertex normals
		self.vertex_normals /= sqrt( ( self.vertex_normals ** 2 ).sum( axis=1 ) ).reshape( -1, 1 )


#
# Collect the neighbor faces
#
def GetNeighborFaces( mesh ) :

	# Initialization
	neighbor_faces = [ [] for i in range(len( mesh.vertices )) ]

	# Loop through the faces
	for i, (a, b ,c) in enumerate( mesh.faces ) :

		# Add faces bound to each vertex
		neighbor_faces[ a ].append( i )
		neighbor_faces[ b ].append( i )
		neighbor_faces[ c ].append( i )

	# Return the list of neighbors without duplicates
	return  [ set( i ) for i in neighbor_faces ] 


#
# Collect the neighborhoods vertices
#
def GetNeighborVertices( mesh ) :

	# Initialization
	neighbor_vertices = [ [] for i in range(len( mesh.vertices )) ]

	# Loop through the faces
	for i, (a, b ,c) in enumerate( mesh.faces ) :

		# Add vertices link by a face
		neighbor_vertices[ a ].append( b )
		neighbor_vertices[ a ].append( c )
		neighbor_vertices[ b ].append( a )
		neighbor_vertices[ b ].append( c )
		neighbor_vertices[ c ].append( a )
		neighbor_vertices[ c ].append( b )

	# Return the list of neighbors without duplicates
	return [ set( i ) for i in neighbor_vertices ] 


#
# Collect the mesh edges
#
def GetEdges( mesh ) :

	# Initialization
	edges = {}
	
	# Create an indexed view of the edges per face
	face_edges = sort( self.faces )[:,[[0,1],[0,2],[1,2]]]

	# Create a dictionary of the mesh edges
	for i, ef in enumerate( face_edges ) :
		for e in ef :
			edge = tuple( e )
			if edge not in self.edges :
				edges[edge] = {};
				edges[edge]['face'] = []
			edges[edge]['face'].append( i )

	return edges


#
# Tell which vertex is on a border
#
def GetBorderVertices( mesh ) :
	
	neighbor_vertices =  GetNeighborVertices( mesh ) 
	neighbor_faces =  GetNeighborFaces( mesh )
	border_vertices = zeros( len(mesh.vertices), dtype=bool )
	
	# Loop through the neighbor vertices
	for va, vn in enumerate( neighbor_vertices ) :
		for vb in vn :
			
			# Check the number of faces in common between the initial vertex and the neighbor
			if len( neighbor_faces[va] & neighbor_faces[vb] ) < 2 :
				border_vertices[ va ] = True
				break

	return border_vertices

#
# Compute the axis-aligned bounding box
#
def GetAxisAlignedBoundingBox( mesh ) :

	# Return the minimum point and the maximum point for each axis
	return ( amin( mesh.vertices, axis = 0 ), amax( mesh.vertices, axis = 0 ) )


#
# Compute the bounding sphere
#
def GetBoundingSphere( mesh ) :

	# Compute axis-aligned bounding box
	( pmin, pmax ) = GetAxisAlignedBoundingBox( mesh )

	# Compute center
	center = 0.5 * (pmin + pmax)

	# Compute radius
	radius = sqrt(((center - mesh.vertices) ** 2).sum(axis = 1)).max()

	# Return result
	return ( center, radius )
