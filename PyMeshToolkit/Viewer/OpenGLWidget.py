# -*- coding:utf-8 -*- 


#
# Create an OpenGL widget with Qt to display a 3D mesh
#


#
# External dependencies
#
import OpenGL.GL as gl
import PySide as qt
import PySide.QtOpenGL as qtgl
from PyMeshToolkit.Viewer.MeshViewer import MeshViewer


#
# Create an OpenGL frame with Qt
#
class OpenGLWidget( MeshViewer, qtgl.QGLWidget ) :

	#
	# Initialisation
	#
	def __init__( self, parent=None ) :
		
		# Initialise QGLWidget with multisampling enabled and OpenGL 3 core only
		qtgl.QGLWidget.__init__( self, qtgl.QGLFormat( qtgl.QGL.SampleBuffers | qtgl.QGL.NoDeprecatedFunctions ), parent )

		# Track mouse events
		self.setMouseTracking( True )
		
		# Mesh loaded at the initialisation
		self.init_mesh = None

	#
	# initializeGL
	#
	def initializeGL( self ) :

		# OpenGL initialization
		MeshViewer.Initialise( self, self.width(), self.height() )
		
		# Load the initial mesh
		if self.init_mesh : MeshViewer.LoadMesh( self, self.init_mesh )

	#
	# paintGL
	#
	def paintGL( self ) :

		# Display the mesh
		MeshViewer.Display( self )

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
		if int(mouseEvent.buttons()) & qt.QtCore.Qt.LeftButton : button = 1

		# Right button
		elif int(mouseEvent.buttons()) & qt.QtCore.Qt.RightButton : button = 2

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
		if MeshViewer.MouseMove( self, mouseEvent.x(), mouseEvent.y() ) :

			# Refresh display
			self.update()

	#
	# wheelEvent
	#
	def wheelEvent( self, event ) :

		# Get the mouse wheel delta for normalisation
		delta = event.delta()

		# Update the trackball
		MeshViewer.MouseWheel( self, delta and delta // abs(delta) )

		# Refresh display
		self.update()

	#
	# OpenGLInfo
	#
	def OpenGLInfo( self ) :

		# Return OpenGL driver informations
		gl_vendor = gl.glGetString( gl.GL_VENDOR )
		gl_renderer = gl.glGetString( gl.GL_RENDERER )
		gl_version = gl.glGetString( gl.GL_VERSION )
		gl_shader = gl.glGetString( gl.GL_SHADING_LANGUAGE_VERSION )
		return ( gl_vendor, gl_renderer, gl_version, gl_shader )
