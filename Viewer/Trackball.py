# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                Trackball.py
#                             -------------------
#    update               : 2013-11-29
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
#       - NeHe Productions - ArcBall Rotation Tutorial
#         http://nehe.gamedev.net
#


#--
#
# External dependencies
#
#--
#
from math import cos, sin, pi, sqrt
from numpy import array, identity, zeros, float32, dot, cross, copy


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
	# WheelEvent
	#
	#-
	#
	def WheelEvent( self, delta ) :

		# Compute the Z-translation
		translation = zeros( 3 )
		translation[2] -= delta * 2.0

		# Compute the translation according to the camera view
		translation = self.Camera2Model( translation )

		# Update the transformation matrix
		self.transformation = self.TranslateMatrix( self.transformation, translation )


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

		# XY translation
		elif self.button ==  2 :

			# Compute the XY-translation
			translation = zeros( 3 )
			translation[0] -= (self.previous_mouse_position[0] - current_mouse_position[0])*0.02
			translation[1] += (self.previous_mouse_position[1] - current_mouse_position[1])*0.02

			# Compute the translation according to the camera view
			translation = self.Camera2Model( translation )

			# Update the transformation matrix
			self.transformation = self.TranslateMatrix( self.transformation, translation )

			# Save the mouse position
			self.previous_mouse_position = current_mouse_position

			# Require a display update
			return True

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
		rotation_axis = self.Camera2Model( cross( previous_position, current_position ) )

		# Rotation angle
		rotation_angle = 90.0 * sqrt( ((current_position - previous_position)**2).sum() ) * 1.5

		# Update transformation matrix
		self.transformation = self.RotateMatrix( self.transformation, rotation_angle, rotation_axis )


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


	#--
	#
	# Camera2Model
	#
	#--
	#
	def Camera2Model( self, vector ) :

		# Transform the vector from the camera space to the model space
		return dot( self.transformation[:3,:3], vector )


	#--
	#
	# TranslateMatrix
	#
	#--
	#
	def TranslateMatrix( self, matrix, direction ) :

		# Translate the matrix
		T = copy( matrix )
		T[3] = matrix[0] * direction[0] + matrix[1] * direction[1] + matrix[2] * direction[2] + matrix[3]
		return T


	#--
	#
	# RotateMatrix
	#
	#--
	#
	def RotateMatrix( self, matrix, angle, axis ) :

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
			    [          0,          0,          0, 1] ], dtype=float32 ).T
		return dot( R, matrix )


