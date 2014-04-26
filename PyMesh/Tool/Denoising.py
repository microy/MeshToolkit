# -*- coding:utf-8 -*- 


#
# Provide functions to denoise a mesh
#


#
# External dependencies
#
from numpy import array, zeros
from PyMesh.Core.Mesh import GetBorderVertices, GetNeighborVertices, GetNeighborFaces


#
# Uniform laplacian
#
#
# Based on :
#
#   ...
#
def UniformLaplacianSmoothing( mesh, iteration, diffusion ) :
	
	# Get neighbors
	neighbors =  [ array(list(v)) for v in GetNeighborVertices( mesh ) ]
	neighbor_number = array( [ len(i) for i in neighbors ] ).reshape(-1,1)
	border = GetBorderVertices( mesh )

	# Smooth
	vertices = mesh.vertices.copy()
	for i in range( iteration ) :
		
		smoothed = [ (vertices[neighbors[v]]).sum(axis=0) for v in range( len(vertices) ) ]
		smoothed /= neighbor_number
		smoothed -= vertices
		smoothed *= diffusion
		smoothed += vertices
		# Don't change border vertices
		for v in range( len(vertices) ) :
			if border[v] : smoothed[v] = vertices[v]
		vertices = smoothed

	return vertices
