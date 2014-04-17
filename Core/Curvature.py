# -*- coding:utf-8 -*- 


#--
#
# Copyright (C) 2013-2014 Michaël Roy
#
#--


#
# Based on :
#
#   Discrete Differential-Geometry Operators for Triangulated 2-Manifolds
#     Mark Meyer, Mathieu Desbrun, Peter Schröder, Alan H. Barr
#     VisMath '02, Berlin (Germany)
#


#--
#
# External dependencies
#
#--
#
from numpy import dot, cross, zeros
from math import pi, sqrt, atan2


#--
#
# GetNormalCurvature
#
#--
#
# Compute the normal curvature vectors of the mesh
# for every vertex
#
def GetNormalCurvature( mesh ) :

	# Initialise normal curvature array
	normal_curvature = zeros( mesh.vertices.shape )

	# Loop through the vertices
	for v1 in range(len( mesh.vertices ) ) :

		# Check border
		if mesh.IsBorderVertex( v1 ) : continue

		# Get the 1-ring neighborhood
		for v2 in mesh.neighbor_vertices[v1] :

			# Initialise the ponderation coefficient
			coef = 0.0
			
			# Find third vertices along the edge
			for v3 in mesh.neighbor_vertices[v1] & mesh.neighbor_vertices[v2] :
				
				# Compute the cotangent of the angle opposite to the edge
				# and add it to the ponderation coefficient
				coef += Cotangent( mesh.vertices[v3], mesh.vertices[v1], mesh.vertices[v2] )

			# Add the edge value to the normal curvature of this vertex
			normal_curvature[v1] += (coef * (mesh.vertices[v1] - mesh.vertices[v2]))

	# Return the normal curvature vector array
	return normal_curvature


#--
#
# ComputeGaussianNormal
#
#--
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


#--
#
# Cotangent
#
#--
#
# Cotangent between two vectors formed by three points
#
def Cotangent( vo, va, vb ) :

	u = va - vo
	v = vb - vo
	lu = dot( u, u )
	lv = dot( v, v )
	dot_uv = dot( u, v )
	return dot_uv / sqrt( lu * lv - dot_uv * dot_uv )


#--
#
# ObtuseAngle
#
#--
#
# Tell if an angle formed by three points is obtuse
#
def ObtuseAngle( vo, va, vb ) :

	u = va - vo
	v = vb - vo
	return dot( u, v ) < 0.0


#--
#
# AngleFromCotan
#
#--
#
# 
#
def AngleFromCotan( vo, va, vb ) :

	u = va - vo
	v = vb - vo
	udotv = dot( u, v )
	denom = (u**2).sum()*(v**2).sum() - udotv*udotv;
	return abs( atan2( sqrt(denom), udotv ) )


#--
#
# VoronoiRegionArea
#
#--
#
# Compute the Voronoi region area of a triangle
#
def VoronoiRegionArea( vo, va, vb ) :

	# Compute triangle area
	face_area = sqrt((cross((va-vo),(vb-vo))**2).sum()) * 0.5;

	# Degenerated triangle
	if face_area == 0.0 : return 0.0

	# Obtuse triangle cases (Voronoi inappropriate)
	if ObtuseAngle(vo, va, vb) : return face_area * 0.5
	if ObtuseAngle(va, vb, vo) or ObtuseAngle(vb, vo, va) : return face_area * 0.25

	# Non-obtuse triangle case (Voronoi area)
	return (Cotangent(va, vo, vb) * ((vo - vb)**2).sum() + Cotangent(vb, vo, va) * ((vo - va)**2).sum()) * 0.125

