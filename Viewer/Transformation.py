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
def TranslateMatrix( matrix, direction ) :

	# Translate the matrix
	translation = identity( 4, dtype=float32 )
	translation[:3, 3] = direction[:3]
	return dot( matrix, translation )




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


