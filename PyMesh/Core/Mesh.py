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
	def __init__( self, name='', vertices=[], faces=[], colors=[], texture_name='', textures=[], vertex_normals=[] ) :

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
		
		# Texture coordinate array
		self.textures = array( textures )
		
		# Per-face normal array
		self.face_normals = array( [] )
		
		# Per-vertex normal array
		self.vertex_normals = array( vertex_normals )


	#
	# Return mesh informations
	#
	def __str__( self ) :
		
		info   = '  Name :               {}\n'.format( self.name )
		info  += '  Vertices :           {}\n'.format( len(self.vertices) )
		info  += '  Faces :              {}'.format( len(self.faces) )
		if len(self.colors) :
			info  += '\n  Colors :             {}'.format( len(self.colors) )
		if len(self.face_normals) :
			info  += '\n  Faces normals :      {}'.format( len(self.face_normals) )
		if len(self.vertex_normals) :
			info  += '\n  Vertex normals :     {}'.format( len(self.vertex_normals) )
		if len(self.textures) :
			info  += '\n  Textures :           {}'.format( len(self.textures) )
		if self.texture_name :
			info  += '\n  Texture filename :   {}'.format( self.texture_name )
		return info


#
# Compute normal vectors of the faces and vertices
#
def UpdateNormals( mesh ) :

	# Create an indexed view of the triangles
	tris = mesh.vertices[ mesh.faces ]

	# Calculate the normal for all the triangles
	mesh.face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )

	# Normalise the face normals
	mesh.face_normals /= sqrt( ( mesh.face_normals ** 2 ).sum( axis=1 ) ).reshape( -1, 1 )

	# Initialise the vertex normals
	mesh.vertex_normals = zeros( mesh.vertices.shape )

	# Add the face normals to the vertex normals
	# Standard implementation :
	#	for i, f in enumerate( mesh.faces ) : mesh.vertex_normals[ f ] += mesh.face_normals[ i ]
	# Optimized implementation :
	for i in range( 3 ) :
		mesh.vertex_normals[:, i] += bincount( mesh.faces[:, 0], mesh.face_normals[:, i], minlength=len(mesh.vertices) )
		mesh.vertex_normals[:, i] += bincount( mesh.faces[:, 1], mesh.face_normals[:, i], minlength=len(mesh.vertices) )
		mesh.vertex_normals[:, i] += bincount( mesh.faces[:, 2], mesh.face_normals[:, i], minlength=len(mesh.vertices) )
	
	# Normalise the vertex normals
	mesh.vertex_normals /= sqrt( ( mesh.vertex_normals ** 2 ).sum( axis=1 ) ).reshape( -1, 1 )


#
# Collect the neighbor faces
#
def GetNeighborFaces( mesh ) :

	# Initialization
	neighbor_faces = [ set() for i in range(len( mesh.vertices )) ]

	# Loop through the faces
	for i, (a, b ,c) in enumerate( mesh.faces ) :

		# Add faces bound to each vertex
		neighbor_faces[ a ].add( i )
		neighbor_faces[ b ].add( i )
		neighbor_faces[ c ].add( i )

	# Return the list of neighbors without duplicates
	return  neighbor_faces


#
# Collect the neighborhoods vertices
#
def GetNeighborVertices( mesh ) :

	# Initialization
	neighbor_vertices = [ set() for i in range(len( mesh.vertices )) ]

	# Loop through the faces
	for i, (a, b ,c) in enumerate( mesh.faces ) :

		# Add vertices link by a face
		neighbor_vertices[ a ].add( b )
		neighbor_vertices[ a ].add( c )
		neighbor_vertices[ b ].add( a )
		neighbor_vertices[ b ].add( c )
		neighbor_vertices[ c ].add( a )
		neighbor_vertices[ c ].add( b )

	# Return the list of neighbors without duplicates
	return neighbor_vertices 


#
# Collect the mesh edges
#
def GetEdges( mesh ) :

	# Edge dictionary
#	edges = { e : {} for a, b in sort( mesh.faces )[:,[[0,0,1],[1,2,2]]] for e in zip(a,b) }

	# Edge set (unordered unique list)
#	edges = set( e for a, b in sort( mesh.faces )[:,[[0,0,1],[1,2,2]]] for e in zip(a,b) )

	# Initialization
	edges = {}
	
	# Create an indexed view of the edges per face
	face_edges = [ zip(a,b) for a,b in sort( mesh.faces )[:,[[0,0,1],[1,2,2]]] ]

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
