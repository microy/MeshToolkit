# -*- coding:utf-8 -*- 


#--
#
# External dependencies
#
#--
#
import platform
import PySide
from PySide import QtGui, QtCore
from PySide.QtGui import QMainWindow, QFileDialog, QMessageBox
from Core.Repair import CheckMesh, CheckNeighborhood
from Core.Vrml import ReadVrml, WriteVrml
from QtViewerUI import Ui_MainWindow


#--
#
# QtViewer
#
#--
#
# Create a mesh viewer with Qt
#
class QtViewer( QMainWindow, Ui_MainWindow ) :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self, parent=None ) :

		# Initialise the main window
		super( QtViewer, self ).__init__( parent ) 

		# Initialise the UI
		self.setupUi( self )

		# Initialise the mesh
		self.mesh = None


	#-
	#
	# FileOpen
	#
	#-
	#
	def FileOpen( self ) :

		# Open file dialog
		(filename, selected_filter) = QFileDialog.getOpenFileName( self, 'Open a VRML file...', '',
			'VRML files (*.vrml *.wrl *.x3d *.x3dv *.iv);;All files (*.*)' )

		# Check filename
		if not filename : return

		# Read VRML/X3D/Inventor file
		self.mesh = ReadVrml( unicode(filename) )

		# Compute mesh normals if necessary
		if len(self.mesh.vertex_normals) != len(self.mesh.vertices) :
			self.mesh.UpdateNormals()

		# Send the mesh to the OpenGL viewer
		self.opengl_widget.LoadMesh( self.mesh )


	#-
	#
	# FileSave
	#
	#-
	#
	def FileSave( self ) :

		# Nothing to save
		if not self.mesh : return

		# Open file dialog
		(filename, selected_filter) = QFileDialog.getSaveFileName( self, 'Save to a VRML file...', '',
			'VRML files (*.vrml *.wrl *.x3d *.x3dv *.iv);;All files (*.*)' )

		# Check filename
		if not filename : return

		# Save VRML/X3D/Inventor file
		WriteVrml( self.mesh, unicode(filename) )


	#-
	#
	# FileCheck
	#
	#-
	#
	def FileCheck( self ) :

		# Nothing to check
		if not self.mesh : return

		# Record neighborhood informations
		self.mesh.UpdateNeighbors()

		# Check different parameters of the mesh
		CheckMesh( self.mesh )
		CheckNeighborhood( self.mesh )


	#-
	#
	# FileClose
	#
	#-
	#
	def FileClose( self ) :

		# Close the mesh
		self.opengl_widget.Close()
		self.mesh = None


	#-
	#
	# ViewFlat
	#
	#-
	#
	def ViewFlat( self ) :

		# Set flat shading
		self.action_view_flat.setChecked( True )
		self.action_view_smooth.setChecked( False )
		self.opengl_widget.SetShader( 'FlatShading' )


	#-
	#
	# ViewSmooth
	#
	#-
	#
	def ViewSmooth( self ) :

		# Set smooth shading
		self.action_view_flat.setChecked( False )
		self.action_view_smooth.setChecked( True )
		self.opengl_widget.SetShader( 'SmoothShading' )


	#-
	#
	# ViewSolid
	#
	#-
	#
	def ViewSolid( self ) :

		# Enable / Disable solid rendering
		self.action_view_solid.setChecked( True )
		self.action_view_wireframe.setChecked( False )
		self.action_view_hiddenlines.setChecked( False )
		self.opengl_widget.wireframe_mode = 0
		self.opengl_widget.update()


	#-
	#
	# ViewWireframe
	#
	#-
	#
	def ViewWireframe( self ) :

		# Enable / Disable wireframe rendering
		self.action_view_solid.setChecked( False )
		self.action_view_wireframe.setChecked( True )
		self.action_view_hiddenlines.setChecked( False )
		self.opengl_widget.wireframe_mode = 1
		self.opengl_widget.update()


	#-
	#
	# ViewHiddenlines
	#
	#-
	#
	def ViewHiddenlines( self ) :

		# Enable / Disable hideen lines rendering
		self.action_view_solid.setChecked( False )
		self.action_view_wireframe.setChecked( False )
		self.action_view_hiddenlines.setChecked( True )
		self.opengl_widget.wireframe_mode = 2
		self.opengl_widget.update()


	#-
	#
	# ViewAntialiasing
	#
	#-
	#
	def ViewAntialiasing( self ) :

		# Enable / Disable antialiasing
		self.action_view_antialiasing.setChecked( self.action_view_antialiasing.isChecked() )
		self.opengl_widget.SetAntialiasing( self.action_view_antialiasing.isChecked() )


	#-
	#
	# ViewColorbar
	#
	#-
	#
	def ViewColorbar( self ) :

		# Enable / Disable color bar display
		self.action_view_colorbar.setChecked( self.action_view_colorbar.isChecked() )
		self.opengl_widget.colorbar_enabled = self.action_view_colorbar.isChecked()
		self.opengl_widget.update()


	#-
	#
	# ViewReset
	#
	#-
	#
	def ViewReset( self ) :

		# Reset model transformation
		self.opengl_widget.trackball.Reset()
		self.opengl_widget.update()


	#-
	#
	# HelpAbout
	#
	#-
	#
	def HelpAbout( self ) :

		QMessageBox.about( self, 'About QtViewer',
		'''<b>PyMesh QtViewer</b>
        <p>Copyright (c) 2013-2014 Michael Roy.</p>
        <p>All rights reserved in accordance with MIT License.</p>
        <i><p>Python {}</p><p>PySide version {}</p><p>Qt version {} on {}</p></i>'''.format(
        platform.python_version(), PySide.__version__, PySide.QtCore.__version__,
        platform.system()))


	#-
	#
	# HelpAboutQt
	#
	#-
	#
	def HelpAboutQt( self ) :
		
		QMessageBox.aboutQt( self, 'About Qt' )
		
		
	#-
	#
	# HelpAboutOpenGL
	#
	#-
	#
	def HelpAboutOpenGL( self ) :
		
		( gl_vendor, gl_renderer, gl_version, gl_shader ) = self.opengl_widget.OpenGLInfo()
		
		QMessageBox.about( self, 'About OpenGL', '''<p><b>Vendor :</b> {}</p>
			<p><b>Renderer :</b> {}</p>
			<p><b>Version :</b> {}</p>
			<p><b>Shader :</b> {}</p>'''.format( gl_vendor, gl_renderer, gl_version, gl_shader ) )

