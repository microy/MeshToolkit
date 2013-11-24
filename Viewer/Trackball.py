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
#	- NeHe Productions - ArcBall Rotation Tutorial
#         http://nehe.gamedev.net
#
#       - Nate Robins' Programs
#         http://www.xmission.com/~nate
#



#--
#
# External dependencies
#
#--
#
from math import cos, pi
from numpy import identity, zeros, float32, dot, cross, sqrt, copy




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

		# Tranformation matrices
		self.transform = identity( 4, dtype=float32 )
		self.last_rot = identity( 3, dtype=float32 )
		self.this_rot = identity( 3, dtype=float32 )


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

		# Reset the transformation matrices
		self.transform = identity( 4, dtype=float32 )
		self.last_rot = identity( 3, dtype=float32 )
		self.this_rot = identity( 3, dtype=float32 )


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

		# Initialise the rotation matrix
		self.last_rot = copy( self.this_rot )


	#-
	#
	# MouseRelease
	#
	#-
	#
	def MouseRelease( self ) :

		self.last_rot = copy( self.this_rot )
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

                        quaternion = self.GetTrackballRotation( current_mouse_position )
			self.this_rot = self.Matrix3fSetRotationFromQuat4f( quaternion )
			self.this_rot = dot( self.last_rot, self.this_rot )
			self.last_rot = copy( self.this_rot )
			self.transform = self.Matrix4fSetRotationFromMatrix3f( self.transform, self.this_rot )
			self.previous_mouse_position = current_mouse_position
			return True

		# XY translation
		elif self.button ==  2 :

			pass

		# Z translation
		elif self.button ==  3 :

			pass

		return False


	
	#-
	#
	# GetTrackballRotation
	#
	#-
	#
	# Compute a trackball rotation
	#
	def GetTrackballRotation( self, current_mouse_position ) :

		# Initialise the quaternion representing the rotation
		quaternion = zeros( 4 )

		# Map the mouse positions
		previous_position = self.TrackballMapping( self.previous_mouse_position )
		current_position = self.TrackballMapping( current_mouse_position )

		# Transform the rotation axis according to the camera view
		quaternion[:3] = dot( self.last_rot.T, cross( previous_position, current_position ) )

		# Rotation angle
		quaternion[3] = dot( current_position, previous_position )

		# Return result
		return quaternion





	#-
	#
	# TrackballMapping
	#
	#-
	#
	def TrackballMapping( self, mouse_position ) :

		v = zeros( 3 )
		v[0] = ( 2.0 * mouse_position[0] - self.width ) / self.width
		v[1] = ( self.height - 2.0 * mouse_position[1] ) / self.height
		d = sqrt(( v**2 ).sum())
		if d > 1.0 : d = 1.0
		v[2] = cos( pi / 2.0 * d )

		return v / sqrt(( v**2 ).sum())




	#-
	#
	# Matrix3fSetRotationFromQuat4f
	#
	#-
	#
	def Matrix3fSetRotationFromQuat4f( self, q1 ) :

		# Converts the H quaternion q1 into a new equivalent 3x3 rotation matrix. 
		X = 0
		Y = 1
		Z = 2
		W = 3

		NewObj = identity( 3, dtype=float32 )
		n = (q1**2).sum()
		s = 0.0
		if (n > 0.0):
			s = 2.0 / n
		xs = q1 [X] * s;  ys = q1 [Y] * s;  zs = q1 [Z] * s
		wx = q1 [W] * xs; wy = q1 [W] * ys; wz = q1 [W] * zs
		xx = q1 [X] * xs; xy = q1 [X] * ys; xz = q1 [X] * zs
		yy = q1 [Y] * ys; yz = q1 [Y] * zs; zz = q1 [Z] * zs
		# This math all comes about by way of algebra, complex math, and trig identities.
		# See Lengyel pages 88-92
		NewObj [X][X] = 1.0 - (yy + zz);	NewObj [Y][X] = xy - wz; 		NewObj [Z][X] = xz + wy;
		NewObj [X][Y] =       xy + wz; 		NewObj [Y][Y] = 1.0 - (xx + zz);	NewObj [Z][Y] = yz - wx;
		NewObj [X][Z] =       xz - wy; 		NewObj [Y][Z] = yz + wx;          	NewObj [Z][Z] = 1.0 - (xx + yy)

		return NewObj



	#-
	#
	# Matrix4fSetRotationFromMatrix3f
	#
	#-
	#
	def Matrix4fSetRotationFromMatrix3f( self, NewObj, three_by_three_matrix ) :

		scale = self.SVD( NewObj )
		NewObj = self.Matrix4fSetRotationScaleFromMatrix3f( NewObj, three_by_three_matrix )
		scaled_NewObj = NewObj * scale
		return scaled_NewObj



	#-
	#
	# Matrix4fSetRotationScaleFromMatrix3f
	#
	#-
	#
	def Matrix4fSetRotationScaleFromMatrix3f( self, NewObj, three_by_three_matrix ) :

		NewObj [0:3,0:3] = three_by_three_matrix
		return NewObj




	#-
	#
	# SVD
	#
	#-
	#
	def SVD( self, NewObj ) :

		X = 0
		Y = 1
		Z = 2
		s = sqrt ( 
			( (NewObj [X][X] * NewObj [X][X]) + (NewObj [X][Y] * NewObj [X][Y]) + (NewObj [X][Z] * NewObj [X][Z]) +
			(NewObj [Y][X] * NewObj [Y][X]) + (NewObj [Y][Y] * NewObj [Y][Y]) + (NewObj [Y][Z] * NewObj [Y][Z]) +
			(NewObj [Z][X] * NewObj [Z][X]) + (NewObj [Z][Y] * NewObj [Z][Y]) + (NewObj [Z][Z] * NewObj [Z][Z]) ) / 3.0 )
		return s




