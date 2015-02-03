# -*- coding:utf-8 -*- 


#
# Compute the normal and the gaussian curvature of a mesh
#


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
import math
import numpy as np



#
# Compute the normal curvature vectors of a given mesh
#
def GetNormalCurvatureReference( mesh ) :

	# Initialisation
	normal_curvature = zeros( mesh.vertices.shape )
#	mixed_area = GetMixedArea( mesh )

	# Loop through the faces
	for a, b, c in mesh.faces :

		# Get the vertices
		va, vb, vc = mesh.vertices[[a, b, c]]

		# Compute cotangent of each angle
		cota = Cotangent( vb-va, vc-va )
		cotb = Cotangent( va-vb, vc-vb )
		cotc = Cotangent( va-vc, vb-vc )

		# Add vectors to vertex normal curvature
		normal_curvature[a] += (va-vc) * cotb + (va-vb) * cotc
		normal_curvature[b] += (vb-vc) * cota + (vb-va) * cotc
		normal_curvature[c] += (vc-va) * cotb + (vc-vb) * cota

	# Weight the normal curvature vectors by the mixed area
#	normal_curvature /= 2.0 * mixed_area.reshape( (len(mesh.vertices),1) )
	
	# Remove border vertices
	for i in range(len( mesh.vertices ) ) :
		if mesh.IsBorderVertex( i ) : normal_curvature[i] = 0.0
		
	# Return the normal curvature vector array
	return normal_curvature


#
# Compute the mixed area of every vertex of a given mesh
#
def GetMixedArea( mesh ) :

	# Initialisation
	mixed_area = zeros( len(mesh.vertices) )

	# Create an indexed view of the triangles
	tris = self.vertices[ self.faces ]

	# Compute triangle area
	face_area = sqrt( (cross( tris[::,1] - tris[::,0], tris[::,2] - tris[::,0] ) ** 2).sum(axis=1) ) / 2.0
	
	# Loop through the faces
	for a, b, c in mesh.faces :

		# Get the vertices
		va, vb, vc = mesh.vertices[[a, b, c]]

		# Compute cotangent of each angle
		cota = Cotangent( vb-va, vc-va )
		cotb = Cotangent( va-vb, vc-vb )
		cotc = Cotangent( va-vc, vb-vc )

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
	
	# Return the mixed area of every vertex
	return mixed_area




#
# Compute the normal curvature vectors of a given mesh
#
def GetNormalCurvature( mesh ) :

	# Create an indexed view of the triangles
	tris = mesh.vertices[ mesh.faces ]

	# Compute the edge vectors of the triangles
	u = tris[::,1] - tris[::,0]
	v = tris[::,2] - tris[::,1]
	w = tris[::,0] - tris[::,2]

	# Compute the cotangent of the triangle angles
	cotangent = np.array( [ Cotangent( u, -w ), Cotangent( v, -u ), Cotangent( w, -v ) ] ).T

	# Compute triangle area
	face_area = np.sqrt( (np.cross( u, -w ) ** 2).sum(axis=1) ) / 2.0
	
	# Tell if there is an obtuse angle in the triangles
	obtuse_angle = ( np.array( [  (-u*w).sum(axis=1), (-u*v).sum(axis=1), (-w*v).sum(axis=1) ] ) < 0 ).T
	
	# Compute the voronoi area of the vertices in each face
	voronoi_area = np.array( [ cotangent[::,2] * (u**2).sum(axis=1) + cotangent[::,1] * (w**2).sum(axis=1),
					cotangent[::,0] * (v**2).sum(axis=1) + cotangent[::,2] * (u**2).sum(axis=1),
					cotangent[::,0] * (v**2).sum(axis=1) + cotangent[::,1] * (w**2).sum(axis=1)	] ).T / 8.0
			
	# Compute the mixed area of each vertex
	mixed_area = np.zeros( mesh.vertex_number )
	for i, (a, b, c) in enumerate( mesh.faces ) :

		# Mixed area - Non-obtuse triangle case (Voronoi area)
		if (obtuse_angle[i] == False).all() :
			
			mixed_area[a] += voronoi_area[i,0]
			mixed_area[b] += voronoi_area[i,1]
			mixed_area[c] += voronoi_area[i,2]
	
		# Mixed area - Obtuse triangle cases (Voronoi inappropriate)
		elif obtuse_angle[i,0] :
			
			mixed_area[a] += face_area[i] / 2.0
			mixed_area[b] += face_area[i] / 4.0
			mixed_area[c] += face_area[i] / 4.0
			
		elif obtuse_angle[i,1] :
			
			mixed_area[a] += face_area[i] / 4.0
			mixed_area[b] += face_area[i] / 2.0
			mixed_area[c] += face_area[i] / 4.0
			
		else :
			
			mixed_area[a] += face_area[i] / 4.0
			mixed_area[b] += face_area[i] / 4.0
			mixed_area[c] += face_area[i] / 2.0
	
	# Compute the curvature part of the vertices in each face
	vertex_curvature = np.array( [ w * cotangent[::,1].reshape(-1,1) - u * cotangent[::,2].reshape(-1,1),
					u * cotangent[::,2].reshape(-1,1) - v * cotangent[::,0].reshape(-1,1),
					v * cotangent[::,0].reshape(-1,1) - w * cotangent[::,1].reshape(-1,1) ] )
					
	# Compute the normal curvature vector of each vertex
	normal_curvature = np.zeros( mesh.vertices.shape )
	for i, (a, b, c) in enumerate( mesh.faces ) :

		normal_curvature[a] += vertex_curvature[0,i]
		normal_curvature[b] += vertex_curvature[1,i]
		normal_curvature[c] += vertex_curvature[2,i]

	# Weight the normal curvature vectors by the mixed area
	normal_curvature /= 2.0 * mixed_area.reshape( -1, 1 )

	# Remove border vertices
	normal_curvature[ mesh.GetBorderVertices() ] = 0.0

	# Return the normal curvature vector array
	return normal_curvature


#
# Compute vertex gaussian curvature
#
def GetGaussianCurvature( mesh ) :

	# Resize gaussian curvature array
	gaussian_curvature = np.zeros( mesh.vertex_number )

	# Loop through the vertices
	for i in range( mesh.vertex_number ) :

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

		gaussian_curvature[i] = ( 2.0 * math.pi - angle_sum ) / area
		
	return gaussian_curvature


#
# Cotangent between two arrays of vectors
#
def Cotangent( u, v ) :

	return ( u * v ).sum(axis=1) / np.sqrt( ( u**2 ).sum(axis=1) * ( v**2 ).sum(axis=1) - ( u * v ).sum(axis=1) ** 2 )


#
# AngleFromCotan
#
def AngleFromCotan( u, v ) :

	udotv = np.dot( u, v )
	denom = (u**2).sum()*(v**2).sum() - udotv*udotv;
	return abs( math.atan2( math.sqrt(denom), udotv ) )

