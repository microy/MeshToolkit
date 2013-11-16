# -*- coding:utf-8 -*- 

# ***************************************************************************
#                             BoundingContainer.py
#                             --------------------
#    update               : 2013-11-16
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



#
# External dependencies
#
from numpy import *
from numpy.linalg import *
from Mesh import *





#--
#
# GetAxisAlignedBoundingBox
#
#--
#
# Compute the axis-aligned bounding box of a given mesh
#
def GetAxisAlignedBoundingBox( mesh ) :

	# Initialisation
	min_point = array( [+inf, +inf, +inf] )
	max_point = array( [-inf, -inf, -inf] )

	# Loop through mesh vertices
	for v in mesh.vertices :
		for i in range( 3 ) :
			if v[i] < min_point[i] : min_point[i] = v[i]
			if v[i] > max_point[i] : max_point[i] = v[i]

	# Return result
	return (min_point, max_point)





#--
#
# GetBoundingSphere
#
#--
#
# Compute the bounding sphere of a given mesh
#
def GetBoundingSphere( mesh ) :

	# Compute axis-aligned bounding box
	(pmin, pmax) = GetAxisAlignedBoundingBox( mesh )

	# Compute center
	center = 0.5 * (pmin + pmax)

	# Compute radius
	radius = 0.0
	for v in mesh.vertices :
		radius = max( radius, norm( center - v ) )

	# Return result
	return (center, radius)












