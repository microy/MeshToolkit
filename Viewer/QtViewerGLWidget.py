# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 QtViewer.py
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
import OpenGL
OpenGL.FORWARD_COMPATIBLE_ONLY = True
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtOpenGL import *
from numpy import identity, float32
from .AxesViewer import AxesViewer
from .MeshViewer import MeshViewer
from .Trackball import GetTrackballRotation
from .Transformation import RotateMatrix





#--
#
# QtViewerGLWidget
#
#--
#
# Create an OpenGL frame with Qt
#
class QtViewerGLWidget( QGLWidget ) :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self, parent=None ) :

		# Initialise QtGLWidget
		QGLWidget.__init__( self, parent )

		# Track mouse events
		self.setMouseTracking( True )

		# Initialise member variables
		self.mesh_viewer = None
		self.axes_viewer = None
		self.previous_mouse_position = [0, 0]
		self.motion_state = 0


	#-
	#
	# initializeGL
	#
	#-
	#
	def initializeGL( self ) :

		# OpenGL configuration
		glClearColor( 1, 1, 1, 1 )
		glHint( GL_LINE_SMOOTH_HINT, GL_NICEST )
		glHint( GL_POLYGON_SMOOTH_HINT, GL_NICEST )
		glEnable( GL_DEPTH_TEST )
		glEnable( GL_CULL_FACE )
		glEnable( GL_BLEND )
#		glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

		# Mesh viewer initialisation
		self.mesh_viewer = MeshViewer( self.width(), self.height() )

		# XYZ axes viewer initialisation
		self.axes_viewer = AxesViewer()


	#-
	#
	# LoadMesh
	#
	#-
	#
	def LoadMesh( self, mesh ) :

		# Send the mesh to the OpenGL viewer
		self.mesh_viewer.LoadMesh( mesh )

		# Initialise the XYZ axes viewer
		self.axes_viewer.trackball_transform = identity( 4, dtype=float32 )

		# Update the display
		self.update()


	#-
	#
	# Close
	#
	#-
	#
	def Close( self ) :

		# Initialise the mesh viewer
		self.mesh_viewer.Close()

		# Initialise the XYZ axes viewer
		self.axes_viewer.trackball_transform = identity( 4, dtype=float32 )

		# Update the display
		self.update()


	#-
	#
	# SetShader
	#
	#-
	#
	def SetShader( self, shader ) :

		# Load a shader for the model
		self.mesh_viewer.shader_program_id = LoadShader( shader )

		# Update the display
		self.update()



	#-
	#
	# Reset
	#
	#-
	#
	def Reset( self ) :

		# Reset model/axes rotation
		self.mesh_viewer.trackball_transform = identity( 4, dtype=float32 )
		self.axes_viewer.trackball_transform = identity( 4, dtype=float32 )

		# Update the display
		self.update()



	#-
	#
	# paintGL
	#
	#-
	#
	def paintGL( self ) :

		# Clear all pixels and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

		# Display the mesh
		self.mesh_viewer.Display()

		# Resize the viewport
		glViewport( 0, 0, 100, 100 )

		# Display the XYZ axes
		self.axes_viewer.Display()

		# Restore the viewport
		glViewport( 0, 0, self.width(), self.height() )

		# Swap buffers
		self.swapBuffers()


	#-
	#
	# resizeGL
	#
	#-
	#
	def resizeGL( self, width, height ) :

		# Resize the viewport
		glViewport( 0, 0, width, height )

		# Recompute the perspective matrix
		self.mesh_viewer.SetPerspectiveMatrix( width, height )




	#-
	#
	# mousePressEvent
	#
	#-
	#
	def mousePressEvent( self, mouseEvent ) :

		# Save mouse position		
		self.previous_mouse_position = [ mouseEvent.x(), mouseEvent.y() ]

		# Left button
		if int(mouseEvent.buttons()) & QtCore.Qt.LeftButton :

			# Trackball rotation
			self.motion_state = 1

		# Middle button
		elif int(mouseEvent.buttons()) & QtCore.Qt.MidButton :

			# XY translation
			self.motion_state = 2

		# Right button
		elif int(mouseEvent.buttons()) & QtCore.Qt.RightButton :

			# Z translation
			self.motion_state = 3



	#-
	#
	# mouseReleaseEvent
	#
	#-
	#
	def mouseReleaseEvent( self, mouseEvent ) :

		# Stop motion
		self.motion_state = 0



	#-
	#
	# mouseMoveEvent
	#
	#-
	#
	def mouseMoveEvent( self, mouseEvent ) :

		# Trackball rotation
                if self.motion_state == 1 :

                        (rotation_angle, rotation_axis) = GetTrackballRotation( [self.width(), self.height()],
				self.previous_mouse_position, [mouseEvent.x(), mouseEvent.y()] )
			self.mesh_viewer.trackball_transform = RotateMatrix( self.mesh_viewer.trackball_transform,
				rotation_angle, rotation_axis )
			self.axes_viewer.trackball_transform = self.mesh_viewer.trackball_transform
			self.previous_mouse_position = [ mouseEvent.x(), mouseEvent.y() ]
			self.update()

		# XY translation
                elif self.motion_state ==  2 :

                        self.mesh_viewer.model_translation[0] -= float(self.previous_mouse_position[0]-mouseEvent.x())*0.005
                        self.mesh_viewer.model_translation[1] += float(self.previous_mouse_position[1]-mouseEvent.y())*0.005
                        self.previous_mouse_position = [ mouseEvent.x(), mouseEvent.y() ]
			self.update()

		# Z translation
                elif self.motion_state ==  3 :

                        self.mesh_viewer.model_translation[2] -= float(self.previous_mouse_position[1]-mouseEvent.y()) * 0.005
                        self.previous_mouse_position = [ mouseEvent.x(), mouseEvent.y() ]
			self.update()



	#-
	#
	# PrintInfo
	#
	#-
	#
	def PrintInfo( self ) :

		# Display OpenGL driver informations
		print '~~~ OpenGL Informations ~~~'
		print '  Vendor :   ' + glGetString( GL_VENDOR )
		print '  Renderer : ' + glGetString( GL_RENDERER )
		print '  Version :  ' + glGetString( GL_VERSION )
		print '  Shader :   ' + glGetString( GL_SHADING_LANGUAGE_VERSION )

