# -*- coding:utf-8 -*- 


#
# Provide functions to denoise a mesh
#


#
# External dependencies
#
from PyMesh.Core.Mesh import GetBorderVertices
from numpy import array, zeros


#
# Uniform laplacian
#
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
