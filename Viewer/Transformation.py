# -*- coding:utf-8 -*- 

# ***************************************************************************
#                              Transformation.py
#                             -------------------
#    update               : 2013-11-18
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
#	  glTranslate, glRotate, glScale, glOrtho, glFrustrum
#	  gluPerspective, gluLookAT
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
from math import *
from numpy import *
from numpy.linalg import *




#--
#
# TranslateMatrix
#
#--
#
def TranslateMatrix( M, direction ) :

	T = identity( 4, dtype=float32 )
	T[:3, 3] = direction[:3]

	return dot( M, T )



#--
#
# ScaleMatrix
#
#--
#
def ScaleMatrix( M, x, y=None, z=None ) :

	if y is None : y = x
	if z is None : z = x

	S = zeros( (4, 4), dtype=float32 )
	S[0] = dot( M[0], x )
	S[1] = dot( M[1], y )
	S[2] = dot( M[2], z )
	S[3] = M[3]
# Slower ?
#	S = identity( 4, dtype=float32 )
#	S[0,0] = x
#	S[1,1] = y
#	S[2,2] = z
#	return dot( M, S )

	return S


#--
#
# RotateMatrix
#
#--
#
def RotateMatrix( M, angle, axis ) :

	x, y, z = axis[0], axis[1], axis[2]
	angle = pi * float(angle) / 180.0
	c, s = cos( angle ), sin( angle )
	n = sqrt( x*x + y*y + z*z )
	if n == 0 : n = 1.0
	x /= n
	y /= n
	z /= n
	cx, cy, cz = (1 - c) * x, (1 - c) * y, (1 - c) * z

	R = array([[  cx*x + c , cy*x - z*s, cz*x + y*s, 0],
		   [ cx*y + z*s,   cy*y + c, cz*y - x*s, 0],
		   [ cx*z - y*s, cy*z + x*s,   cz*z + c, 0],
		   [          0,          0,          0, 1] ])

	return array( dot( M, R ), dtype=float32 )


#--
#
# OrthographicMatrix
#
#--
#
def OrthographicMatrix( left, right, bottom, top, znear, zfar ) :

	# Initialise matrix
	M = identity( 4, dtype=float32 )

	# Compute orthographic matrix
	M[0,0] = 2.0 / float(right - left)
	M[1,1] = 2.0 / float(top - bottom)
	M[2,2] = - 2.0 / float(zfar - znear)
	M[0,3] = - float(right + left) / float(right - left)
	M[1,3] = - float(top + bottom) / float(top - bottom)
	M[2,3] = - float(zfar + znear) / float(zfar - znear)

	# Return result
	return M

        
#--
#
# FrustrumMatrix
#
#--
#
def FrustrumMatrix( left, right, bottom, top, znear, zfar ) :

	# Initialise matrix
	M = zeros( (4,4), dtype=float32 )

	# Compute frustrum matrix
	M[0,0] = 2.0 * float(znear) / float(right - left)
	M[1,1] = 2.0 * float(znear) / float(top - bottom)
	M[0,2] = float(right + left) / float(right - left)
	M[1,2] = float(top + bottom) / float(top - bottom)
	M[2,2] = - float(zfar + znear) / float(zfar - znear)
	M[3,2] = - 1.0
	M[2,3] = - 2.0 * float(znear) * float(zfar) / float(zfar - znear)

	# Return result
	return M


#--
#
# PerspectiveMatrix
#
#--
#
def PerspectiveMatrix( fovy, aspect, znear, zfar ) :

	# Initialise matrix
	M = identity( 4, dtype=float32 )

	# Compute perspective matrix
	f = tan( pi * float(fovy) / 360.0 )
	M[0,0] = 1.0 / ( f * float(aspect) )
	M[1,1] = 1.0 / f
	M[2,2] = - float(zfar + znear) / float(zfar - znear)
	M[2,3] = - 2.0 * float(znear) * float(zfar) / float(zfar - znear)
	M[3,2] = - 1.0

	# Return result
	return M


#--
#
# LookAtMatrix
#
#--
#
def LookAtMatrix( eye, center, up ) :

	# Cast input variables
	eye = array ( eye, dtype=float32 )
	center = array ( center, dtype=float32 )
	up = array ( up, dtype=float32 )

	# The "look-at" vector
	f = center - eye
	f /= norm( f )

	# The "right" vector
	s = cross(f, up)
	s /= norm( s )

	# The "up" vector
	u = cross(s, f)

	# Compute the "look-at" matrix
	M = identity( 4, dtype=float32 )
	M[0,0] =  s[0]
	M[0,1] =  s[1]
	M[0,2] =  s[2]
	M[1,0] =  u[0]
	M[1,1] =  u[1]
	M[1,2] =  u[2]
	M[2,0] = -f[0]
	M[2,1] = -f[1]
	M[2,2] = -f[2]

	# Return result
	return TranslateMatrix( M, -eye )



