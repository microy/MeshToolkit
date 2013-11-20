# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                Trackball.py
#                             -------------------
#    update               : 2013-11-20
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
# External dependencies
#
#--
#
from math import cos, pi
from numpy import zeros, cross
from numpy.linalg import norm




#-
#
# GetTrackballRotation
#
#-
#
# Compute a trackball rotation
#
def GetTrackballRotation( window_size, previous_mouse_position, current_mouse_position ) :

	# Map the mouse positions
	previous_position = TrackballMapping( window_size, previous_mouse_position )
        current_position = TrackballMapping( window_size, current_mouse_position )

	# Compute the rotation parameters
        rotation_axis = cross( previous_position, current_position )
        rotation_angle = 90.0 * norm( current_position - previous_position ) * 1.5

	# Return result
	return ( rotation_angle, rotation_axis )





#-
#
# TrackballMapping
#
#-
#
# Map the mouse coordinates to a ball
# Adapted from Nate Robins' programs
# http://www.xmission.com/~nate
#
def TrackballMapping( window_size, mouse_position ) :

	v = zeros( 3 )
	v[0] = ( 2.0 * mouse_position[0] - window_size[0] ) / window_size[0]
	v[1] = ( window_size[1] - 2.0 * mouse_position[1] ) / window_size[1]
	d = norm( v )
	if d > 1.0 : d = 1.0
	v[2] = cos( pi / 2.0 * d )

	return v / norm(v)





