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
from numpy import dot, cross, zeros
from math import pi, sqrt, atan2


#
# Compute the normal curvature vectors of a given mesh
#
def GetNormalCurvature( mesh ) :

	# Initialisation
	normal_curvature = zeros( mesh.vertices.shape )
	mixed_area = zeros( (len(mesh.vertices),1) )
	
	# Loop through the faces
	for a, b, c in mesh.faces :

		# Get the vertices
		va, vb, vc = mesh.vertices[[a, b, c]]

		# Compute cotangent of each angle
		cota = Cotangent( vb-va, vc-va )
		cotb = Cotangent( va-vb, vc-vb )
		cotc = Cotangent( va-vc, vb-vc )

		# Add vectors to vertex normal curvature
		normal_curvature[a] += (va-vc) * cotb + (va-vb) * cotc
		normal_curvature[b] += (vb-vc) * cota + (vb-va) * cotc
		normal_curvature[c] += (vc-va) * cotb + (vc-vb) * cota
		
		#
		# Compute "mixed" area
		#

		# Compute triangle area
		face_area = sqrt((cross((vb-va),(vc-va))**2).sum()) / 2.0

		# Obtuse triangle cases (Voronoi inappropriate)
		if dot( vb-va, vc-va ) <  0 :
			
			mixed_area[a] += face_area / 2.0
			mixed_area[b] += face_area / 4.0
			mixed_area[c] += face_area / 4.0
			
		elif dot( va-vb, vc-vb ) <  0 :
			
			mixed_area[a] += face_area / 4.0
			mixed_area[b] += face_area / 2.0
			mixed_area[c] += face_area / 4.0
			
		elif dot( va-vc, vb-vc ) <  0 :
			
			mixed_area[a] += face_area / 4.0
			mixed_area[b] += face_area / 4.0
			mixed_area[c] += face_area / 2.0
			
		# Non-obtuse triangle case (Voronoi area)
		else :
		
			u = ( (va - vb) ** 2 ).sum()
			v = ( (va - vc) ** 2 ).sum()
			w = ( (vb - vc) ** 2 ).sum()
			mixed_area[a] += ( u * cotc + v * cotb ) / 8.0
			mixed_area[b] += ( u * cotc + w * cota ) / 8.0
			mixed_area[c] += ( v * cotb + w * cota ) / 8.0

	# Weight the normal curvature vectors by the mixed area
	normal_curvature /= 2.0 * mixed_area
	
	# Remove border vertices
	for i in range(len( mesh.vertices ) ) :
		if mesh.IsBorderVertex( i ) : normal_curvature[i] = 0.0
		
	# Return the normal curvature vector array
	return normal_curvature



#
# Cotangent between two vectors
#
def Cotangent( u, v ) :

	return dot( u, v ) / sqrt( dot(u, u) * dot(v, v) - dot(u, v) ** 2 )


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
# 
#
def AngleFromCotan( u, v ) :

	udotv = dot( u, v )
	denom = (u**2).sum()*(v**2).sum() - udotv*udotv;
	return abs( atan2( sqrt(denom), udotv ) )

