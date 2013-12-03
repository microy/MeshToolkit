# -*- coding:utf-8 -*- 

# ***************************************************************************
#                               OpenGLWidget.py
#                             -------------------
#    update               : 2013-12-03
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
import PySide
from PySide import QtGui, QtCore, QtOpenGL
from PySide.QtOpenGL import QGLWidget, QGLFormat, QGL
from numpy import identity, float32

from .ColorBar import ColorBar
from .MeshViewer import MeshViewer


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

		
		# Initialise QGLWidget with multisampling enabled and OpenGL 3 core only
		QGLWidget.__init__( self, QGLFormat( QGL.SampleBuffers | QGL.NoDeprecatedFunctions ), parent )

		# Track mouse events
		self.setMouseTracking( True )

		# Initialise mouse position
		self.previous_mouse_position = [ 0, 0 ]

		# Initialise OpenGL viewers
		self.mesh_viewer = None
		self.colorbar = None

		# Initialise viewing parameters
		self.colorbar_enabled = False
		self.wireframe_enabled = False


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

		# Color bar viewer initialisation
		self.colorbar = ColorBar()


	#-
	#
	# LoadMesh
	#
	#-
	#
	def LoadMesh( self, mesh ) :

		# Send the mesh to the OpenGL viewer
		self.mesh_viewer.LoadMesh( mesh )

		# Update the display
		self.update()


	#-
	#
	# Close
	#
	#-
	#
	def Close( self ) :

		# Close the current mesh
		self.mesh_viewer.Close()

		# Update the display
		self.update()

	#-
	#
	# Reset
	#
	#-
	#
	def Reset( self ) :

		# Reset the trackball
		self.mesh_viewer.trackball.Reset()

		# Update the display
		self.update()


	#-
	#
	# SetShader
	#
	#-
	#
	def SetShader( self, shader ) :

		# Load a shader for the model
		self.mesh_viewer.SetShader( shader )

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
	# SetWireframe
	#
	#-
	#
	def SetWireframe( self, enabled ) :

		# Enable / Disable color bar
		self.wireframe_enabled = enabled

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

		# Display the mesh with wireframe rendering
		if self.wireframe_enabled :

			# 1st pass : wireframe model
			glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
			self.mesh_viewer.Display()

			# 2nd pass : hidden line removal
			glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
			glEnable( GL_POLYGON_OFFSET_FILL )
			glPolygonOffset( 1.0, 1.0 )
			self.mesh_viewer.Display( True )
			glDisable( GL_POLYGON_OFFSET_FILL )

		# Display the mesh
		else : self.mesh_viewer.Display()

		# Display the color bar
		self.DrawColorBar()

		# Swap buffers
		self.swapBuffers()


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

		# Display the color bar
		self.colorbar.Display()

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

		# Recompute the perspective matrix of the mesh viewer
		self.mesh_viewer.Resize( width, height )


	#-
	#
	# mousePressEvent
	#
	#-
	#
	def mousePressEvent( self, mouseEvent ) :

		# Left button
		if int(mouseEvent.buttons()) & QtCore.Qt.LeftButton : button = 1

		# Right button
		elif int(mouseEvent.buttons()) & QtCore.Qt.RightButton : button = 2

		# Unmanaged
		else : return

		# Update the trackball
		self.mesh_viewer.trackball.MousePress( [ mouseEvent.x(), mouseEvent.y() ], button )


	#-
	#
	# mouseReleaseEvent
	#
	#-
	#
	def mouseReleaseEvent( self, mouseEvent ) :

		# Update the trackball
		self.mesh_viewer.trackball.MouseRelease()


	#-
	#
	# mouseMoveEvent
	#
	#-
	#
	def mouseMoveEvent( self, mouseEvent ) :

		# Update the trackball
		if self.mesh_viewer.trackball.Motion( [ mouseEvent.x(), mouseEvent.y() ] ) :

			# Refresh display
			self.update()


	#-
	#
	# wheelEvent
	#
	#-
	#
	def wheelEvent( self, event ) :

		# Get the mouse wheel delta for normalisation
		delta = event.delta()

		# Update the trackball
		self.mesh_viewer.trackball.WheelEvent( delta and delta // abs(delta) )

		# Refresh display
		self.update()


	#-
	#
	# OpenGLInfo
	#
	#-
	#
	def OpenGLInfo( self ) :

		# Return OpenGL driver informations
		gl_vendor = glGetString( GL_VENDOR ).decode('latin-1')
		gl_renderer = glGetString( GL_RENDERER ).decode('latin-1')
		gl_version = glGetString( GL_VERSION ).decode('latin-1')
		gl_shader = glGetString( GL_SHADING_LANGUAGE_VERSION ).decode('latin-1')
		return ( gl_vendor, gl_renderer, gl_version, gl_shader )

