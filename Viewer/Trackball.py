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
from .Transformation import RotateMatrix
from math import cos, pi
from numpy import zeros, cross
from numpy.linalg import norm





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



	#-
	#
	# Resize
	#
	#-
	#
	def Resize( self, width=1024, height=768 ) :

		self.width = width
		self.height = height


	#-
	#
	# MousePress
	#
	#-
	#
	def MousePress( self, mouse_position, button ) :

		self.previous_mouse_position = mouse_position
		self.button = button


	#-
	#
	# MouseRelease
	#
	#-
	#
	def MouseRelease( self ) :

		self.motion_state = 0


	#-
	#
	# Motion
	#
	#-
	#
	def Motion( self, current_mouse_position ) :

		# Trackball rotation
		if self.button == 1 :

			(rotation_angle, rotation_axis) = GetTrackballRotation( current_mouse_position )
			self.trackball_transform = RotateMatrix( self.trackball_transform, rotation_angle, rotation_axis )
			self.previous_mouse_position = current_mouse_position

		# XY translation
		elif self.button ==  2 :

			self.model_translation[0] -= float(self.previous_mouse_position[0]-current_mouse_position[0])*0.005
			self.model_translation[1] += float(self.previous_mouse_position[1]-current_mouse_position[1])*0.005
			self.previous_mouse_position = current_mouse_position

		# Z translation
		elif self.button ==  3 :

			self.mesh_viewer.model_translation[2] -= float(self.previous_mouse_position[1]-current_mouse_position[1]) * 0.005
			self.previous_mouse_position = current_mouse_position


	
	#-
	#
	# GetTrackballRotation
	#
	#-
	#
	# Compute a trackball rotation
	#
	def GetTrackballRotation( current_mouse_position ) :

		# Map the mouse positions
		previous_position = TrackballMapping( self.previous_mouse_position )
		current_position = TrackballMapping( current_mouse_position )

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
	def TrackballMapping( mouse_position ) :

		v = zeros( 3 )
		v[0] = ( 2.0 * mouse_position[0] - self.width ) / self.width
		v[1] = ( self.height - 2.0 * mouse_position[1] ) / self.height
		d = norm( v )
		if d > 1.0 : d = 1.0
		v[2] = cos( pi / 2.0 * d )

		return v / norm(v)











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





