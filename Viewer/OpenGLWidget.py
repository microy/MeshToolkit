# -*- coding:utf-8 -*- 

# ***************************************************************************
#                               OpenGLWidget.py
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





#--
#
# External dependencies
#
#--
#
from .Axis import Axis
from .ColorBar import ColorBar
from .MeshViewer import MeshViewer
from .Shader import LoadShader
from .Trackball import Trackball
import OpenGL
OpenGL.FORWARD_COMPATIBLE_ONLY = True
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtOpenGL import *






#--
#
# OpenGLWidget
#
#--
#
# Create an OpenGL frame with Qt
#
class OpenGLWidget( QGLWidget ) :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self, parent=None ) :

		
		# Initialise QtGLWidget with multisampling enabled and OpenGL 3 core only
		QGLWidget.__init__( self, QGLFormat( QGL.SampleBuffers | QGL.NoDeprecatedFunctions ), parent )

		# Track mouse events
		self.setMouseTracking( True )

		# Initialise mouse position
		self.previous_mouse_position = [0, 0]

		# Initialise OpenGL viewers
		self.mesh_viewer = None
		self.axis_viewer = None
		self.colorbar_viewer = None

		# Initialise viewing parameters
		self.axis_enabled = True
		self.colorbar_enabled = False

		# Trackball initialisation
		self.trackball = Trackball( self.width(), self.height() )




	#-
	#
	# initializeGL
	#
	#-
	#
	def initializeGL( self ) :

		# Default background color
		glClearColor( 1, 1, 1, 1 )

		# Enable depth test
		glEnable( GL_DEPTH_TEST )

		# Enable face culling
		glEnable( GL_CULL_FACE )

		# Enable blending function
		glEnable( GL_BLEND )
		glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

		# Enable multisampling (antialiasing)
		glEnable( GL_MULTISAMPLE )

		# Mesh viewer initialisation
		self.mesh_viewer = MeshViewer( self.width(), self.height() )

		# XYZ axes viewer initialisation
		self.axis_viewer = Axis()

		# Color bar viewer initialisation
		self.colorbar_viewer = ColorBar()


	#-
	#
	# LoadMesh
	#
	#-
	#
	def LoadMesh( self, mesh ) :

		# Send the mesh to the OpenGL viewer
		self.mesh_viewer.LoadMesh( mesh )

		# Reset current transformations
		self.Reset()


	#-
	#
	# Close
	#
	#-
	#
	def Close( self ) :

		# Initialise the mesh viewer
		self.mesh_viewer.Close()

		# Reset current transformations
		self.Reset()


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
	# SetAntialiasing
	#
	#-
	#
	def SetAntialiasing( self, enabled ) :

		# Enable / Disable antialiasing
		if enabled : glEnable( GL_MULTISAMPLE )
		else : glDisable( GL_MULTISAMPLE )

		# Update the display
		self.update()


	#-
	#
	# SetAxis
	#
	#-
	#
	def SetAxis( self, enabled ) :

		# Enable / Disable XYZ-axes
		self.axis_enabled = enabled

		# Update the display
		self.update()


	#-
	#
	# SetColorBar
	#
	#-
	#
	def SetColorBar( self, enabled ) :

		# Enable / Disable color bar
		self.colorbar_enabled = enabled

		# Update the display
		self.update()


	#-
	#
	# Reset
	#
	#-
	#
	def Reset( self ) :

		# Reset trackball transformation matrix
		self.trackball.Reset()
		self.mesh_viewer.trackball_transform = self.trackball.transform
		self.axis_viewer.trackball_transform = self.trackball.transform

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
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT )

		# Display the mesh
		self.mesh_viewer.Display()

		# Display the XYZ-axes
		self.DrawAxis()

		# Display the color bar
		self.DrawColorBar()

		# Swap buffers
		self.swapBuffers()


	#-
	#
	# DrawAxis
	#
	#-
	#
	def DrawAxis( self ) :

		# Axis enabled ?
		if not self.axis_enabled : return

		# Resize the viewport
		glViewport( 0, 0, 100, 100 )

		# Display the XYZ axes
		self.axis_viewer.Display()

		# Restore the viewport
		glViewport( 0, 0, self.width(), self.height() )


	#-
	#
	# DrawColorBar
	#
	#-
	#
	def DrawColorBar( self ) :

		# Color bar enabled ?
		if not self.colorbar_enabled : return

		# Resize the viewport
		glViewport( self.width()-50, self.height()/2-300, 50, 600 )

		# Display the XYZ axes
		self.colorbar_viewer.Display()

		# Restore the viewport
		glViewport( 0, 0, self.width(), self.height() )


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
		self.mesh_viewer.Resize( width, height )
		self.trackball.Resize( width, height )


	#-
	#
	# mousePressEvent
	#
	#-
	#
	def mousePressEvent( self, mouseEvent ) :

		button = 0
		# Left button
		if int(mouseEvent.buttons()) & QtCore.Qt.LeftButton : button = 1
		# Middle button
		elif int(mouseEvent.buttons()) & QtCore.Qt.MidButton : button = 2
		# Right button
		elif int(mouseEvent.buttons()) & QtCore.Qt.RightButton : button = 3
		self.trackball.MousePress( [ self.width()-mouseEvent.x(), self.height()-mouseEvent.y() ], button )


	#-
	#
	# mouseReleaseEvent
	#
	#-
	#
	def mouseReleaseEvent( self, mouseEvent ) :

		self.trackball.MouseRelease()


	#-
	#
	# mouseMoveEvent
	#
	#-
	#
	def mouseMoveEvent( self, mouseEvent ) :

		if self.trackball.Motion( [ self.width()-mouseEvent.x(), self.height()-mouseEvent.y() ] ) :
			self.mesh_viewer.trackball_transform = self.trackball.transform
			self.axis_viewer.trackball_transform = self.trackball.transform
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
