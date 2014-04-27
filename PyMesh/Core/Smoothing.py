# -*- coding:utf-8 -*- 


#
# Provide functions to smooth mesh
#


#
# External dependencies
#
from numpy import array, zeros
from PyMesh.Core.Mesh import GetBorderVertices
from PyMesh.Core.Curvature import Cotangent


#
# Uniform laplacian
#
# Based on :
#
#   ...
#
def UniformLaplacianSmoothing( mesh, iteration, diffusion ) :
	
	# Convert neighbor list to numpy array for fancy indexing
	neighbors =  [ array(list(v)) for v in mesh.neighbor_vertices ]
	
	# Get neighbor vertex number
	neighbor_number = array( [ len(i) for i in neighbors ] ).reshape(-1,1)
	
	# Get border vertices
	border = GetBorderVertices( mesh )

	# Iteration steps
	for i in range( iteration ) :
		
		# Average neighbor vertices
		smoothed = [ (mesh.vertices[neighbors[v]]).sum(axis=0) for v in range( len(mesh.vertices) ) ]
		smoothed /= neighbor_number
		
		# Get new vertex position
		smoothed = mesh.vertices + diffusion * ( smoothed - mesh.vertices )
		
		# Don't change border vertices
		smoothed[ border ] = mesh.vertices[ border ]
		
		# Update original vertices
		mesh.vertices = smoothed


#
# Curvature flow smoothing
#
# Based on :
#
#   Implicit Fairing of Irregular Meshes using Diffusion and Curvature Flow
#     M. Desbrun, M. Meyer, P. Schröder, A. Barr
#     Proceedings of SIGGRAPH '99
#
def CurvatureFlowSmoothing( mesh, iteration, diffusion ) :
	
	# Get border vertices
	border = GetBorderVertices( mesh )

	# Iteration steps
	for i in range( iteration ) :
		
		# Create an indexed view of the triangles
		tris = mesh.vertices[ mesh.faces ]

		# Compute the edge vectors of the triangles
		u = tris[::,1] - tris[::,0]
		v = tris[::,2] - tris[::,1]
		w = tris[::,0] - tris[::,2]

		# Compute the cotangent of the triangle angles
		cotangent = array( [ Cotangent( u, -w ), Cotangent( v, -u ), Cotangent( w, -v ) ] ).T

		# Compute the voronoi area of the vertices in each face
		vertex_weight = array( [ cotangent[::,2] + cotangent[::,1], cotangent[::,0] + cotangent[::,2],	cotangent[::,0] + cotangent[::,1]	] )

		# Compute the curvature part of the vertices in each face
		vertex_curvature = array( [ w * cotangent[::,1].reshape(-1,1) - u * cotangent[::,2].reshape(-1,1),
						u * cotangent[::,2].reshape(-1,1) - v * cotangent[::,0].reshape(-1,1),
						v * cotangent[::,0].reshape(-1,1) - w * cotangent[::,1].reshape(-1,1) ] )
						
		# Compute the normal curvature vector of each vertex
		smoothed = zeros( mesh.vertices.shape )
		weight = zeros( len(mesh.vertices) )
		for i, (a, b, c) in enumerate( mesh.faces ) :

			smoothed[a] += vertex_curvature[0,i]
			smoothed[b] += vertex_curvature[1,i]
			smoothed[c] += vertex_curvature[2,i]
			weight[a] += vertex_weight[0,i]
			weight[b] += vertex_weight[1,i]
			weight[c] += vertex_weight[2,i]

		# Get new vertex position
		smoothed = mesh.vertices - diffusion * smoothed / weight.reshape(-1,1)
		
		# Don't change border vertices
		smoothed[ border ] = mesh.vertices[ border ]
		
		# Update original vertices
		mesh.vertices = smoothed
