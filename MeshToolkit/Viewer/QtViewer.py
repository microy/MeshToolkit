# -*- coding:utf-8 -*-


#
# Create a Qt application to display a 3D mesh with OpenGL
#


#
# External dependencies
#
import sys
import PySide as qt
import PySide.QtCore as qtcore
import PySide.QtGui as qtgui
import PySide.QtOpenGL as qtgl
import MeshToolkit as mtk


#
# Main application to display a mesh
#
class QtViewer( qtgui.QApplication ) :

	#
	# Initialisation
	#
	def __init__( self, mesh = None ) :

		# Initialize parent class
		super( QtViewer, self ).__init__( sys.argv )

		# Show the widget used to display the mesh
		self.qtopenglwidget = QtOpenGLWidget( mesh = mesh )
		self.qtopenglwidget.show()

		# Enter Qt main loop
		sys.exit( self.exec_() )


#
# Customize the Qt OpenGL widget
# to get our mesh viewer
#
class QtOpenGLWidget( qtgl.QGLWidget ) :

	#
	# Initialisation
	#
	def __init__( self, parent = None, mesh = None ) :

		# Initialise QGLWidget with multisampling enabled and OpenGL 3 core only
		super( QtOpenGLWidget, self ).__init__( qtgl.QGLFormat( qtgl.QGL.SampleBuffers | qtgl.QGL.NoDeprecatedFunctions ), parent )

		# Track mouse events
		self.setMouseTracking( True )

		# Change the widget position and size
		self.setGeometry( 100, 100, 1024, 768 )

		# Mesh loaded at the initialisation
		self.mesh = mesh

	#
	# initializeGL
	#
	def initializeGL( self ) :

		# Create the mesh viewer
		self.meshviewer = mtk.MeshViewer()

		# OpenGL initialization
		self.meshviewer.InitialiseOpenGL( self.width(), self.height() )

		# Mesh during initialization ?
		if self.mesh :

			# Load the mesh
			self.meshviewer.LoadMesh( self.mesh )

			# Set the window title
			self.setWindowTitle( self.mesh.name )

	#
	# paintGL
	#
	def paintGL( self ) :

		# Display the mesh
		self.meshviewer.Display()

	#
	# resizeGL
	#
	def resizeGL( self, width, height ) :

		# Resize the mesh viewer
		self.meshviewer.Resize( width, height )

	#
	# mousePressEvent
	#
	def mousePressEvent( self, mouseEvent ) :

		# Left button
		if int( mouseEvent.buttons() ) & qtcore.Qt.LeftButton : button = 1

		# Right button
		elif int( mouseEvent.buttons() ) & qtcore.Qt.RightButton : button = 2

		# Unmanaged
		else : return

		# Update the trackball
		self.meshviewer.trackball.MousePress( [ mouseEvent.x(), mouseEvent.y() ], button )

	#
	# mouseReleaseEvent
	#
	def mouseReleaseEvent( self, mouseEvent ) :

		# Update the trackball
		self.meshviewer.trackball.MouseRelease()

	#
	# mouseMoveEvent
	#
	def mouseMoveEvent( self, mouseEvent ) :

		# Update the trackball
		if self.meshviewer.trackball.MouseMove( mouseEvent.x(), mouseEvent.y() ) :

			# Refresh display
			self.update()

	#
	# wheelEvent
	#
	def wheelEvent( self, event ) :

		# Get the mouse wheel delta for normalisation
		delta = event.delta()

		# Update the trackball
		self.meshviewer.trackball.MouseWheel( delta and delta // abs(delta) )

		# Refresh display
		self.update()

	#
	# Keyboard event
	#
	def keyPressEvent( self, event ) :

		# Escape
		if event.key() == qtcore.Qt.Key_Escape :

			# Exit
			self.close()

		# A
		elif event.key() == qtcore.Qt.Key_A :

			# Antialiasing
			self.meshviewer.ToggleAntialiasing()

		# F
		elif event.key() == qtcore.Qt.Key_F :

			# Flat shading
			self.meshviewer.SetShader( 'Flat' )

		# G
		elif event.key() == qtcore.Qt.Key_G :

			# Smooth shading
			self.meshviewer.SetShader( 'Smooth' )

		# O
		elif event.key() == qtcore.Qt.Key_O :

			# Open file dialog
			( filename, selected_filter ) = qtgui.QFileDialog.getOpenFileName( self, 'Open a Stanford PLY file...', '',
				'Stanford PLY files (*.ply);;All files (*.*)' )

			# Check filename
			if not filename : return

			# Read PLY file
			self.mesh = mtk.ReadPly( filename )

			# Send the mesh to the OpenGL viewer
			self.meshviewer.LoadMesh( self.mesh )

			# Set the window title
			self.setWindowTitle( self.mesh.name )

		# R
		elif event.key() == qtcore.Qt.Key_R :

			# Reset model translation and rotation
			self.meshviewer.trackball.Reset()

		# S
		elif event.key() == qtcore.Qt.Key_S :

			# Nothing to save
			if not self.mesh : return

			# Open file dialog
			( filename, selected_filter ) = qtgui.QFileDialog.getSaveFileName( self, 'Save to a Stanford PLY file...', '',
				'Stanford PLY files (*.ply);;All files (*.*)' )

			# Check filename
			if not filename : return

			# Save PLY file
			mtk.WritePly( self.mesh, filename )

		# W
		elif event.key() == qtcore.Qt.Key_W :

			# Close the mesh
			self.meshviewer.Close()
			self.mesh = None

			# Set the window title
			self.setWindowTitle( '' )

		# X
		elif event.key() == qtcore.Qt.Key_X :

			# Nothing to check
			if not self.mesh : return

			# Check different parameters of the mesh
			mtk.Check( self.mesh )

		# 1
		elif event.key() == qtcore.Qt.Key_1 :

			# Display the mesh with solid rendering
			self.meshviewer.wireframe_mode = 0

		# 2
		elif event.key() == qtcore.Qt.Key_2 :

			# Display the mesh with wireframe rendering
			self.meshviewer.wireframe_mode = 1

		# 3
		elif event.key() == qtcore.Qt.Key_3 :

			# Display the mesh with hidden line removal rendering
			self.meshviewer.wireframe_mode = 2

		# Unmanaged key
		else : return

		# Refresh display
		self.update()
