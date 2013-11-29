# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                Curvature.py
#                             -------------------
#    update               : 2013-11-29
#    copyright            : (C) 2013 by Michaël Roy
#    email                : microygh@gmail.com
# ***************************************************************************

# ***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************


#--
#
# Based on :
#
# Discrete Differential-Geometry Operators for Triangulated 2-Manifolds
# Mark Meyer, Mathieu Desbrun, Peter Schröder, Alan H. Barr
# VisMath '02, Berlin (Germany)
#
#--


#-
#
# External dependencies
#
#-
#
from numpy import dot, zeros
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
	normal_curvature = zeros( mesh.vertices.shape, dtype=mesh.vertices.dtype )

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
				
				# Compute the cotangent opposite to the edge
				# and add it to the ponderation coefficient
				u = mesh.vertices[v1] - mesh.vertices[v3]
				v = mesh.vertices[v2] - mesh.vertices[v3]
				coef += Cotangent( u, v )

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
	gaussian_curvature = zeros( mesh.vertices.shape, dtype=mesh.vertices.dtype )

	# Loop through the vertices
	for i in range(len( mesh.vertices ) ) :

		# Check border
		if mesh.IsBorderVertex( i ) : continue

		area = 0.0
		angle_sum = 0.0

		# Get the 1-ring neighborhood
		for f in mesh.neighbor_faces[i] :

			if mesh.faces[f, 0] == i :
				
#				area += VoronoiRegionArea( Vertex(i), Vertex(*it1, 1), Vertex(*it1, 2) )
#				angle_sum += AngleFromCotan( Vertex(i), Vertex(*it1, 1), Vertex(*it1, 2) )
				
			elif mesh.faces[f, 1] == i  :
				
#				area += VoronoiRegionArea( Vertex(i), Vertex(*it1, 2), Vertex(*it1, 0) )
#				angle_sum += AngleFromCotan( Vertex(i), Vertex(*it1, 2), Vertex(*it1, 0) )

			else :
				
#				area += VoronoiRegionArea( Vertex(i), Vertex(*it1, 0), Vertex(*it1, 1) )
#				angle_sum += AngleFromCotan( Vertex(i), Vertex(*it1, 0), Vertex(*it1, 1) )

		gaussian_curvature[i] = ( 2.0 * pi - angle_sum ) / area


#--
#
# Cotangent
#
#--
#
# Cotangent between two vector in nD
#
def Cotangent( u, v ) :

	lu = dot( u, u )
	lv = dot( v, v )
	dot_uv = dot( u, v )
	return dot_uv / sqrt( lu * lv - dot_uv * dot_uv )


def CotangentT( vo, va, vb ) :

	return Cotangent( va-vo, vb-vo )


# Obtuse angle
def ObtuseAngle( u, v ) :

	return dot( u, v ) < 0.0


def ObtuseAngleT( vo, va, vb ) :

	return ObtuseAngle( va-vo, vb-vo )


# Angle From Cotan
def AngleFromCotan( u, v ) :
	
	udotv = dot( u , v )
	denom = (u**2).sum()*(v**2).sum() - udotv*udotv;
	return abs( atan2( sqrt(denom), udotv ) )
	

def AngleFromCotanT( vo, va, vb ) :

	return AngleFromCotan( va-vo, vb-vo )


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
	face_area = sqrt((cross((va-vo),(vb-vo))**2).sum(axis=1)) * 0.5;

	# Degenerated triangle
	if face_area == 0.0 : return 0.0

	# Obtuse triangle case (Voronoi inappropriate)
	if ObtuseAngleT(vo, va, vb) : return face_area * 0.5
	if ObtuseAngleT(va, vb, vo) or ObtuseAngleT(vb, vo, va) : return face_area * 0.25

	# Non-obtuse triangle case (Voronoi area)
	return (CotangentT(va, vo, vb)*((vo-vb)**2).sum(axis=1) + CotangentT(vb, vo, va)*((vo-va)**2).sum(axis=1)) * 0.125

