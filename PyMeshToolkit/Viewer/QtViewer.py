# -*- coding:utf-8 -*- 


#
# Create a Qt application to display a 3D mesh with OpenGL
#


#
# External dependencies
#
import platform
import PySide as qt
import PySide.QtGui as qtgui
from PyMeshToolkit.Core.Repair import Check
from PyMeshToolkit.File.Ply import ReadPly, WritePly
from .QtViewerUI import Ui_MainWindow


#
# Create a mesh viewer with Qt
#
class QtViewer( qtgui.QMainWindow, Ui_MainWindow ) :

	#
	# Initialisation
	#
	def __init__( self, parent = None, mesh = None ) :

		# Initialise the main window
		super( QtViewer, self ).__init__( parent ) 

		# Initialise the UI
		self.setupUi( self )

		# Initialise the mesh
		self.mesh = mesh
		self.opengl_widget.init_mesh = mesh

	#
	# File -> Open
	#
	def FileOpen( self ) :

		# Open file dialog
		( filename, selected_filter ) = qtgui.QFileDialog.getOpenFileName( self, 'Open a PLY file...', '',
			'PLY files (*.ply);;All files (*.*)' )

		# Check filename
		if not filename : return

		# Read PLY file
		self.mesh = ReadPly( filename )

		# Send the mesh to the OpenGL viewer
		self.opengl_widget.LoadMesh( self.mesh )

	#
	# File -> Save
	#
	def FileSave( self ) :

		# Nothing to save
		if not self.mesh : return

		# Open file dialog
		( filename, selected_filter ) = qtgui.QFileDialog.getSaveFileName( self, 'Save to a PLY file...', '',
			'PLY files (*.ply);;All files (*.*)' )

		# Check filename
		if not filename : return

		# Save PLY file
		WritePly( self.mesh, filename )

	#
	# File -> Check
	#
	def FileCheck( self ) :

		# Nothing to check
		if not self.mesh : return

		# Check different parameters of the mesh
		Check( self.mesh )

	#
	# File -> Close
	#
	def FileClose( self ) :

		# Close the mesh
		self.opengl_widget.Close()
		self.mesh = None
		self.opengl_widget.update()

	#
	# View -> Flat
	#
	def ViewFlat( self ) :

		# Set flat shading
		self.action_view_flat.setChecked( True )
		self.action_view_smooth.setChecked( False )
		self.opengl_widget.SetShader( 'FlatShading' )
		self.opengl_widget.update()

	#
	# View -> Smooth
	#
	def ViewSmooth( self ) :

		# Set smooth shading
		self.action_view_flat.setChecked( False )
		self.action_view_smooth.setChecked( True )
		self.opengl_widget.SetShader( 'SmoothShading' )
		self.opengl_widget.update()

	#
	# View -> Solid
	#
	def ViewSolid( self ) :

		# Enable / Disable solid rendering
		self.action_view_solid.setChecked( True )
		self.action_view_wireframe.setChecked( False )
		self.action_view_hiddenlines.setChecked( False )
		self.opengl_widget.wireframe_mode = 0
		self.opengl_widget.update()

	#
	# View -> Wireframe
	#
	def ViewWireframe( self ) :

		# Enable / Disable wireframe rendering
		self.action_view_solid.setChecked( False )
		self.action_view_wireframe.setChecked( True )
		self.action_view_hiddenlines.setChecked( False )
		self.opengl_widget.wireframe_mode = 1
		self.opengl_widget.update()

	#
	# View -> Hidden lines
	#
	def ViewHiddenlines( self ) :

		# Enable / Disable hideen lines rendering
		self.action_view_solid.setChecked( False )
		self.action_view_wireframe.setChecked( False )
		self.action_view_hiddenlines.setChecked( True )
		self.opengl_widget.wireframe_mode = 2
		self.opengl_widget.update()

	#
	# View -> Antialiasing
	#
	def ViewAntialiasing( self ) :

		# Enable / Disable antialiasing
		self.action_view_antialiasing.setChecked( self.action_view_antialiasing.isChecked() )
		self.opengl_widget.SetAntialiasing( self.action_view_antialiasing.isChecked() )
		self.opengl_widget.update()

	#
	# View -> Reset
	#
	def ViewReset( self ) :

		# Reset model transformation
		self.opengl_widget.Reset()
		self.opengl_widget.update()

	#
	# Help -> About
	#
	def HelpAbout( self ) :

		qtgui.QMessageBox.about( self, 'About QtViewer',
		'''<b>PyMeshToolkit QtViewer</b>
        <p>Copyright (c) 2013-2015 Michael Roy.</p>
        <p>All rights reserved in accordance with the MIT License.</p>
        <i><p>Python {}</p><p>PySide version {}</p><p>Qt version {} on {}</p></i>'''.format(
        platform.python_version(), qt.__version__, qt.QtCore.__version__,
        platform.system()))

	#
	# Help -> About Qt
	#
	def HelpAboutQt( self ) :
		
		qtgui.QMessageBox.aboutQt( self, 'About Qt' )
		
	#
	# Help -> About OpenGL
	#
	def HelpAboutOpenGL( self ) :
		
		( gl_vendor, gl_renderer, gl_version, gl_shader ) = self.opengl_widget.OpenGLInfo()
		
		qtgui.QMessageBox.about( self, 'About OpenGL', '''<p><b>Vendor :</b> {}</p>
			<p><b>Renderer :</b> {}</p>
			<p><b>Version :</b> {}</p>
			<p><b>Shader :</b> {}</p>'''.format( gl_vendor, gl_renderer, gl_version, gl_shader ) )

