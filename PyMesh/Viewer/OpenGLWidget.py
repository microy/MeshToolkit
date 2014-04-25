# -*- coding:utf-8 -*- 


#
# Create an OpenGL widget with Qt to diplay a 3D mesh
#


#
# External dependencies
#
import OpenGL
from OpenGL.GL import *
import PySide
from PySide import QtGui, QtCore, QtOpenGL
from PySide.QtOpenGL import QGLWidget, QGLFormat, QGL
from math import tan, pi
from numpy import array, identity, dot, float32, uint32, zeros
from PyMesh.Tool.Color import Value2Color, Value2ColorAlternate
from PyMesh.Core.Mesh import GetBoundingSphere
from PyMesh.Viewer.MeshViewer import MeshViewer


#
# Create an OpenGL frame with Qt
#
class OpenGLWidget( MeshViewer, QGLWidget ) :


	#
	# Initialisation
	#
	def __init__( self, parent=None ) :
		
		# Initialise QGLWidget with multisampling enabled and OpenGL 3 core only
		QGLWidget.__init__( self, QGLFormat( QGL.SampleBuffers | QGL.NoDeprecatedFunctions ), parent )

		# Track mouse events
		self.setMouseTracking( True )


	#
	# initializeGL
	#
	def initializeGL( self ) :

		# OpenGL initialization
		MeshViewer.Initialize( self, self.width(), self.height() )


	#
	# paintGL
	#
	def paintGL( self ) :

		# Display the mesh
		MeshViewer.Display( self )

		# Swap buffers
		self.swapBuffers()


	#
	# resizeGL
	#
	def resizeGL( self, width, height ) :

		# Resize the mesh viewer
		MeshViewer.Resize( self, width, height )


	#
	# mousePressEvent
	#
	def mousePressEvent( self, mouseEvent ) :

		# Left button
		if int(mouseEvent.buttons()) & QtCore.Qt.LeftButton : button = 1

		# Right button
		elif int(mouseEvent.buttons()) & QtCore.Qt.RightButton : button = 2

		# Unmanaged
		else : return

		# Update the trackball
		MeshViewer.MousePress( self, [ mouseEvent.x(), mouseEvent.y() ], button )


	#
	# mouseReleaseEvent
	#
	def mouseReleaseEvent( self, mouseEvent ) :

		# Update the trackball
		MeshViewer.MouseRelease( self )


	#
	# mouseMoveEvent
	#
	def mouseMoveEvent( self, mouseEvent ) :

		# Update the trackball
		if MeshViewer.Motion( self, mouseEvent.x(), mouseEvent.y() ) :

			# Refresh display
			self.update()


	#
	# wheelEvent
	#
	def wheelEvent( self, event ) :

		# Get the mouse wheel delta for normalisation
		delta = event.delta()

		# Update the trackball
		MeshViewer.WheelEvent( delta and delta // abs(delta) )

		# Refresh display
		self.update()


	#
	# OpenGLInfo
	#
	def OpenGLInfo( self ) :

		# Return OpenGL driver informations
		gl_vendor = glGetString( GL_VENDOR )
		gl_renderer = glGetString( GL_RENDERER )
		gl_version = glGetString( GL_VERSION )
		gl_shader = glGetString( GL_SHADING_LANGUAGE_VERSION )
		return ( gl_vendor, gl_renderer, gl_version, gl_shader )
