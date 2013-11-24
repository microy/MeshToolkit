# -*- coding:utf-8 -*- 

# ***************************************************************************
#                              Transformation.py
#                             -------------------
#    update               : 2013-11-24
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
# Inspired from :
#
#	- OpenGL and GLU documentation
#         http://www.opengl.org/sdk/docs/man2
#
#	- GLM
#	  https://github.com/g-truc/glm
#


#--
#
# External dependencies
#
#--
#
from math import cos, sin, tan, pi
from numpy import array, identity, dot, sqrt, float32


#--
#
# TranslateMatrix
#
#--
#
def TranslateMatrix( matrix, direction ) :

	# Translate the matrix
	T = identity( 4, dtype=float32 )
	T[:3, 3] = direction[:3]
	return dot( matrix, T )


#--
#
# RotateMatrix
#
#--
#
def RotateMatrix( matrix, angle, axis ) :

	# Rotate the matrix according to the given angle and axis
	angle = pi * angle / 180.0
	c, s = cos( angle ), sin( angle )
	n = sqrt( (axis**2).sum() )
	if n == 0 : n = 1.0
	axis /= n
	x, y, z = axis[0], axis[1], axis[2]
	cx, cy, cz = (1 - c) * x, (1 - c) * y, (1 - c) * z
	R = array([ [   cx*x + c, cy*x - z*s, cz*x + y*s, 0],
		    [ cx*y + z*s,   cy*y + c, cz*y - x*s, 0],
		    [ cx*z - y*s, cy*z + x*s,   cz*z + c, 0],
		    [          0,          0,          0, 1] ], dtype=float32 )
	return dot( matrix, R )


#--
#
# OrthographicMatrix
#
#--
#
def OrthographicMatrix( left, right, bottom, top, near, far ) :

	# Compute the orthographic matrix
	M = identity( 4, dtype=float32 )
	M[0,0] = 2.0 / (right - left)
	M[1,1] = 2.0 / (top - bottom)
	M[2,2] = - 2.0 / (far - near)
	M[0,3] = - (right + left) / (right - left)
	M[1,3] = - (top + bottom) / (top - bottom)
	M[2,3] = - (far + near) / (far - near)
	return M


#--
#
# PerspectiveMatrix
#
#--
#
def PerspectiveMatrix( fovy, aspect, near, far ) :

	# Compute the perspective matrix
	M = identity( 4, dtype=float32 )
	f = tan( pi * fovy / 360.0 )
	M[0,0] = 1.0 / (f * aspect)
	M[1,1] = 1.0 / f
	M[2,2] = - (far + near) / (far - near)
	M[2,3] = - 2.0 * near * far / (far - near)
	M[3,2] = - 1.0
	return M


