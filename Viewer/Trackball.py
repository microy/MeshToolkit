# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                Trackball.py
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
#       - Nate Robins' Programs
#         http://www.xmission.com/~nate
#
#	- NeHe Productions - ArcBall Rotation Tutorial
#         http://nehe.gamedev.net
#


#--
#
# External dependencies
#
#--
#
from .Transformation import RotateMatrix
from math import cos, pi
from numpy import identity, zeros, float32, dot, cross, sqrt


#--
#
# Trackball
#
#--
#
# Create a trackball for smooth visualization
#
class Trackball :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self, width=1024, height=768 ) :

		# Window size
		self.width = width
		self.height = height

		# Button pressed
		self.button = 0

		# Mouse position
		self.previous_mouse_position = [ 0, 0 ]

		# Tranformation matrix
		self.transformation = identity( 4, dtype=float32 )


	#-
	#
	# Resize
	#
	#-
	#
	def Resize( self, width=1024, height=768 ) :

		# Change window size
		self.width = width
		self.height = height


	#-
	#
	# Reset
	#
	#-
	#
	def Reset( self ) :

		# Reset the transformation matrix
		self.transformation = identity( 4, dtype=float32 )


	#-
	#
	# MousePress
	#
	#-
	#
	def MousePress( self, mouse_position, button ) :

		# Record mouse position
		self.previous_mouse_position = mouse_position

		# Record button pressed
		self.button = button


	#-
	#
	# MouseRelease
	#
	#-
	#
	def MouseRelease( self ) :

		# Mouse button release
		self.button = 0


	#-
	#
	# Motion
	#
	#-
	#
	def Motion( self, current_mouse_position ) :

		# Trackball rotation
		if self.button == 1 :

			# Update the rotation of the trackball
                        self.TrackballRotation( current_mouse_position )

			# Save the mouse position
			self.previous_mouse_position = current_mouse_position

			# Require a display update
			return True

		# XY translation
		elif self.button ==  2 :

			return False

		# Z translation
		elif self.button ==  3 :

			return False

		# No update
		return False

	
	#-
	#
	# TrackballRotation
	#
	#-
	#
	# Update the rotation of the trackball
	#
	def TrackballRotation( self, current_mouse_position ) :

		# Map the mouse positions
		previous_position = self.TrackballMapping( self.previous_mouse_position )
		current_position = self.TrackballMapping( current_mouse_position )

		# Compute the rotation axis according to the camera view
		rotation_axis = dot( self.transformation[:3,:3].T, cross( previous_position, current_position ) )

		# Rotation angle
	        rotation_angle = 90.0 * sqrt( ((current_position - previous_position)**2).sum() ) * 1.5

		# Update transformation matrix
		self.transformation = RotateMatrix( self.transformation, rotation_angle, rotation_axis )


	#-
	#
	# TrackballMapping
	#
	#-
	#
	def TrackballMapping( self, mouse_position ) :

		# Map the mouse position onto a unit sphere
		v = zeros( 3 )
		v[0] = ( 2.0 * mouse_position[0] - self.width ) / self.width
		v[1] = ( self.height - 2.0 * mouse_position[1] ) / self.height
		d = sqrt(( v**2 ).sum())
		if d > 1.0 : d = 1.0
		v[2] = cos( pi / 2.0 * d )
		return v / sqrt(( v**2 ).sum())



