# -*- coding:utf-8 -*-


#
# External dependencies
#
import numpy as np


#
# Define a class to store neighborhood informations
# of a given mesh
#
class Neighborhood( object ) :

	#
	# Initialisation
	#
	def __init__( self, mesh ) :

		# Register the mesh
		self.mesh = mesh
		
		# Collect neighborhood informations
		self.UpdateNeighbors()

	#
	# Register neighborhood informations
	#
	def UpdateNeighbors( self ) :

		# Initialization
		self.neighbor_faces = [ set() for i in range(self.mesh.vertex_number) ]
		self.neighbor_vertices = [ set() for i in range(self.mesh.vertex_number) ]

		# Loop through the faces
		for i, (a, b ,c) in enumerate( self.mesh.faces ) :

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
		
		# Initialize border vertex list
		border_vertices = np.zeros( self.mesh.vertex_number, dtype=np.bool )
		
		# Loop through the neighbor vertices
		for va, vn in enumerate( self.neighbor_vertices ) :
			for vb in vn :
				
				# Check the number of faces in common between the initial vertex and the neighbor
				if len( self.neighbor_faces[va] & self.neighbor_faces[vb] ) < 2 :
					border_vertices[ va ] = True
					break
		
		# Return the border vertex list
		return border_vertices

