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
from math import tan, pi
from numpy import identity, dot, float32





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


