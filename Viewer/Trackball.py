# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                Trackball.py
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


#--
#
# External dependencies
#
#--
#
# NumPy
#
from math import *
from numpy import *
from numpy.linalg import *



#--
#
# Trackball
#
#--
#
# Create a trackball
#
class Trackball :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self, width=1024, height=768 ) :

		self.width = width
		self.height = height
		self.previous_trackball_position = array( [0.0, 0.0, 0.0] )


	#-
	#
	# Resize
	#
	#-
	#
	def Resize( self, width, height ) :

		self.width = width
		self.height = height


	#-
	#
	# Update
	#
	#-
	#
	def Update( self, x, y ) :

		self.previous_trackball_position = self.TrackballMapping( x, y )


	#-
	#
	# GetRotation
	#
	#-
	#
	def GetRotation( self, x, y ) :

                current_position = self.TrackballMapping( x, y )

                rotation_axis = cross( self.previous_trackball_position, current_position )
                rotation_angle = 90.0 * norm( current_position - self.previous_trackball_position ) * 1.5

                self.previous_trackball_position = current_position

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
	def TrackballMapping( self, x, y ) :

		v = zeros( 3 )
		v[0] = ( 2.0 * x - self.width ) / self.width
		v[1] = ( self.height - 2.0 * y ) / self.height
		d = norm( v )
		if d > 1.0 : d = 1.0
		v[2] = cos( pi / 2.0 * d )

		return v / norm(v)



