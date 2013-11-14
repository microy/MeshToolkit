# -*- coding:utf-8 -*- 

# ***************************************************************************
#                              Transformation.py
#                             -------------------
#    update               : 2013-11-14
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
# Taken from Vispy
# https://github.com/vispy
#

#
# External dependencies
#
from math import *
from numpy import *




#--
#
# TranslateMatrix
#
#--
#
def TranslateMatrix( M, x, y=None, z=None ) :
	if y is None : y = x
	if z is None : z = x
	T = [	[ 1, 0, 0, x],
		[ 0, 1, 0, y],
		[ 0, 0, 1, z],
		[ 0, 0, 0, 1]	]
	T = array( T, dtype=float32 ).T
	M[...] = dot( M, T )



#--
#
# ScaleMatrix
#
#--
#
def ScaleMatrix( M, x, y=None, z=None ) :
	if y is None : y = x
	if z is None : z = x
	S = [	[ x, 0, 0, 0],
		[ 0, y, 0, 0],
		[ 0, 0, z, 0],
		[ 0, 0, 0, 1]	]
	S = array( S, dtype=float32 ).T
	M[...] = dot( M, S )


#--
#
# RotateMatrixX
#
#--
#
def RotateMatrixX( M, theta ) :
	t = pi * theta / 180.0
	cosT = cos( t )
	sinT = sin( t )
	R = array( [
		[ 1.0,  0.0,  0.0, 0.0 ],
		[ 0.0, cosT,-sinT, 0.0 ],
		[ 0.0, sinT, cosT, 0.0 ],
		[ 0.0,  0.0,  0.0, 1.0 ] ], dtype=float32 )
	M[...] = dot( M, R )


#--
#
# RotateMatrixY
#
#--
#
def RotateMatrixY( M, theta ) :
	t = pi * theta / 180.0
	cosT = cos( t )
	sinT = sin( t )
	R = array( [
		[ cosT, 0.0, sinT, 0.0 ],
		[  0.0, 1.0,  0.0, 0.0 ],
		[-sinT, 0.0, cosT, 0.0 ],
		[  0.0, 0.0,  0.0, 1.0 ] ], dtype=float32 )
	M[...] = dot( M, R )


#--
#
# RotateMatrixZ
#
#--
#
def RotateMatrixZ( M, theta ) :
	t = pi * theta / 180.0
	cosT = cos( t )
	sinT = sin( t )
	R = array( [
		[ cosT,-sinT, 0.0, 0.0 ],
		[ sinT, cosT, 0.0, 0.0 ],
		[  0.0,  0.0, 1.0, 0.0 ],
		[  0.0,  0.0, 0.0, 1.0 ] ], dtype=float32 )
	M[...] = dot( M, R )


#--
#
# RotateMatrix
#
#--
#
def RotateMatrix( M, angle, x, y, z, point=None ) :
	angle = pi * angle / 180.0
	c,s = cos( angle ), sin( angle )
	n = sqrt( x*x + y*y + z*z )
	x /= n
	y /= n
	z /= n
	cx,cy,cz = (1-c)*x, (1-c)*y, (1-c)*z
	R = array([[  cx*x + c , cy*x - z*s, cz*x + y*s, 0],
		   [ cx*y + z*s,   cy*y + c, cz*y - x*s, 0],
		   [ cx*z - y*s, cy*z + x*s,   cz*z + c, 0],
		   [          0,          0,          0, 1] ]).T
	M[...] = dot( M, R )


#--
#
# OrthoMatrix
#
#--
#
def OrthoMatrix( left, right, bottom, top, znear, zfar ) :
	M = zeros( (4,4), dtype=float32 )
	M[0,0] = +2.0 / (right - left)
	M[3,0] = -(right + left) / float(right - left)
	M[1,1] = +2.0 / (top - bottom)
	M[3,1] = -(top + bottom) / float(top - bottom)
	M[2,2] = -2.0 / (zfar - znear)
	M[3,2] = -(zfar + znear) / float(zfar - znear)
	M[3,3] = 1.0
	return M

        
#--
#
# FrustrumMatrix
#
#--
#
def FrustrumMatrix( left, right, bottom, top, znear, zfar ) :
	M = zeros( (4,4), dtype=float32 )
	M[0,0] = +2.0 * znear / (right - left)
	M[2,0] = (right + left) / (right - left)
	M[1,1] = +2.0 * znear / (top - bottom)
	M[3,1] = (top + bottom) / (top - bottom)
	M[2,2] = -(zfar + znear) / (zfar - znear)
	M[3,2] = -2.0 * znear * zfar / (zfar - znear)
	M[2,3] = -1.0
	return M


#--
#
# PerspectiveMatrix
#
#--
#
def PerspectiveMatrix( fovy, aspect, znear, zfar ) :
	h = tan(fovy / 360.0 * pi) * znear
	w = h * aspect
	return FrustrumMatrix( -w, w, -h, h, znear, zfar )


#-
#
# TrackballMapping
#
#-
#
def TrackballMapping( x, y, width, height ) :
	# Adapted from Nate Robins' programs
	# http://www.xmission.com/~nate
	v = zeros( 3 )
	v[0] = ( 2.0 * float(x) - float(width) ) / float(width)
	v[1] = ( float(height) - 2.0 * float(y) ) / float(height)
	d = norm( v )
	if d > 1.0 : d = 1.0
	v[2] = cos( pi / 2.0 * d );
	return v / norm(v)

