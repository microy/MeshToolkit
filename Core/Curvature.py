# -*- coding:utf-8 -*- 


#
# Based on :
#
#   Discrete Differential-Geometry Operators for Triangulated 2-Manifolds
#     Mark Meyer, Mathieu Desbrun, Peter Schröder, Alan H. Barr
#     VisMath '02, Berlin (Germany)
#


#
# External dependencies
#
from numpy import array, cross, dot, sqrt, zeros
from math import pi, atan2
from .Mesh import GetBorderVertices


#
# Compute the normal curvature vectors of a given mesh
#
def GetNormalCurvature( mesh ) :

	# Initialisation
	normal_curvature = zeros( mesh.vertices.shape )
	mixed_area = zeros( len(mesh.vertices) )

	# Create an indexed view of the triangles
	tris = mesh.vertices[ mesh.faces ]

	# Compute the cotangent of the triangle angles
	cotangent = array( [ Cotangent( tris[::,1] - tris[::,0], tris[::,2] - tris[::,0] ),
				Cotangent( tris[::,0] - tris[::,1], tris[::,2] - tris[::,1] ),
				Cotangent( tris[::,0] - tris[::,2], tris[::,1] - tris[::,2] ) ] ).T

	# Compute triangle area
	face_area = sqrt( (cross( tris[::,1] - tris[::,0], tris[::,2] - tris[::,0] ) ** 2).sum(axis=1) ) / 2.0
	
	# Tell if there is an obtuse angle in the triangles
	obtuse_angle = ( array( [  ((tris[::,1]-tris[::,0])*(tris[::,2]-tris[::,0])).sum(axis=1),
			((tris[::,0]-tris[::,1])*(tris[::,2]-tris[::,1])).sum(axis=1),
			((tris[::,0]-tris[::,2])*(tris[::,1]-tris[::,2])).sum(axis=1) ] ) < 0 ).T
			
	# Compute the mixed area and the normal curvature vector of each vertex
	for i, f in enumerate( mesh.faces ) :

		# Get the vertices
		a, b, c = f
		va, vb, vc = mesh.vertices[ f ]
		
		# Mixed area - Obtuse triangle cases (Voronoi inappropriate)
		if obtuse_angle[i,0] :
			
			mixed_area[a] += face_area[i] / 2.0
			mixed_area[b] += face_area[i] / 4.0
			mixed_area[c] += face_area[i] / 4.0
			
		elif obtuse_angle[i,1] :
			
			mixed_area[a] += face_area[i] / 4.0
			mixed_area[b] += face_area[i] / 2.0
			mixed_area[c] += face_area[i] / 4.0
			
		elif obtuse_angle[i,2] :
			
			mixed_area[a] += face_area[i] / 4.0
			mixed_area[b] += face_area[i] / 4.0
			mixed_area[c] += face_area[i] / 2.0
			
		# Mixed area - Non-obtuse triangle case (Voronoi area)
		else :
		
			u = ( (va - vb) ** 2 ).sum()
			v = ( (va - vc) ** 2 ).sum()
			w = ( (vb - vc) ** 2 ).sum()
			mixed_area[a] += ( u * cotangent[i,2] + v * cotangent[i,1] ) / 8.0
			mixed_area[b] += ( u * cotangent[i,2] + w * cotangent[i,0] ) / 8.0
			mixed_area[c] += ( v * cotangent[i,1] + w * cotangent[i,0] ) / 8.0

		# Compute the normal curvature vector of each vertex
		normal_curvature[a] += (va-vc) * cotangent[i,1] + (va-vb) * cotangent[i,2]
		normal_curvature[b] += (vb-vc) * cotangent[i,0] + (vb-va) * cotangent[i,2]
		normal_curvature[c] += (vc-va) * cotangent[i,1] + (vc-vb) * cotangent[i,0]

	# Weight the normal curvature vectors by the mixed area
	normal_curvature /= 2.0 * mixed_area.reshape( -1, 1 )

	# Remove border vertices
	border = GetBorderVertices( mesh )
	for v, on_border in enumerate( border ) :
		if on_border : normal_curvature[ v ] = 0.0

	# Return the normal curvature vector array
	return normal_curvature


#
# Cotangent between two vector arrays
#
def Cotangent( u, v ) :

	return ( u * v ).sum(axis=1) / sqrt( ( u**2 ).sum(axis=1) * ( v**2 ).sum(axis=1) - ( u * v ).sum(axis=1) ** 2 )


#
# Compute vertex gaussian curvature
#
def GetGaussianCurvature( mesh ) :

	# Resize gaussian curvature array
	gaussian_curvature = zeros(len( mesh.vertices ))

	# Loop through the vertices
	for i in range(len( mesh.vertices ) ) :

		# Check border
		if mesh.IsBorderVertex( i ) : continue

		area = 0.0
		angle_sum = 0.0

		# Get the 1-ring neighborhood
		for f in mesh.neighbor_faces[i] :

			if mesh.faces[f, 0] == i :
				
				area += VoronoiRegionArea( mesh.vertices[i], mesh.vertices[mesh.faces[f,1]], mesh.vertices[mesh.faces[f,2]] )
				angle_sum += AngleFromCotan( mesh.vertices[i], mesh.vertices[mesh.faces[f,1]], mesh.vertices[mesh.faces[f,2]] )
				
			elif mesh.faces[f, 1] == i  :
				
				area += VoronoiRegionArea( mesh.vertices[i], mesh.vertices[mesh.faces[f,2]], mesh.vertices[mesh.faces[f,0]] )
				angle_sum += AngleFromCotan( mesh.vertices[i], mesh.vertices[mesh.faces[f,2]], mesh.vertices[mesh.faces[f,0]] )

			else :
				
				area += VoronoiRegionArea( mesh.vertices[i], mesh.vertices[mesh.faces[f,0]], mesh.vertices[mesh.faces[f,1]] )
				angle_sum += AngleFromCotan( mesh.vertices[i], mesh.vertices[mesh.faces[f,0]], mesh.vertices[mesh.faces[f,1]] )

		gaussian_curvature[i] = ( 2.0 * pi - angle_sum ) / area
		
	return gaussian_curvature


#
# AngleFromCotan
#
def AngleFromCotan( u, v ) :

	udotv = dot( u, v )
	denom = (u**2).sum()*(v**2).sum() - udotv*udotv;
	return abs( atan2( sqrt(denom), udotv ) )

