# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 QtViewer.py
#                             -------------------
#    update               : 2013-11-25
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

from PySide import QtGui, QtCore
from PySide.QtGui import *

from .OpenGLWidget import OpenGLWidget
from Core.Mesh import CheckMesh, CheckNeighborhood
from Core.Vrml import ReadVrml, WriteVrml


#--
#
# QtViewer
#
#--
#
# Create a mesh viewer with Qt
#
class QtViewer( QMainWindow ) :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self ) :

		# Initialise QMainWindow		
		QMainWindow.__init__( self )

		# Initialise the mesh
		self.mesh = None

		# Set the window title
		self.setWindowTitle( 'QtViewer' )

		# Resize the main window
		self.resize( 1024, 768 )

		# Move the main window
		self.move( 100, 100 )

		# Set the status bar
		self.statusBar()

		# Create the file menu actions
		file_open_action = QtGui.QAction( '&Open...', self )
		file_open_action.setShortcut( 'O' )
		file_open_action.setStatusTip( 'Open a file' )
		self.connect( file_open_action, QtCore.SIGNAL('triggered()'), self.FileOpenAction )

		file_save_action = QtGui.QAction( '&Save...', self )
		file_save_action.setShortcut( 'S' )
		file_save_action.setStatusTip( 'Save the current mesh' )
		self.connect( file_save_action, QtCore.SIGNAL('triggered()'), self.FileSaveAction )

		file_check_action = QtGui.QAction( '&Check', self )
		file_check_action.setStatusTip( 'Check different parameters of the mesh' )
		self.connect( file_check_action, QtCore.SIGNAL('triggered()'), self.FileCheckAction )

		file_close_action = QtGui.QAction( '&Close', self )
		file_close_action.setShortcut( 'W' )
		file_close_action.setStatusTip( 'Close the current file' )
		self.connect( file_close_action, QtCore.SIGNAL('triggered()'), self.FileCloseAction )

		file_exit_action = QtGui.QAction( '&Exit', self )
		file_exit_action.setShortcut( 'Esc' )
		file_exit_action.setStatusTip( 'Exit application' )
		self.connect( file_exit_action, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()') )

		# Create the view menu actions
		self.view_flat_action = QtGui.QAction( '&Flat shading', self )
		self.view_flat_action.setShortcut( 'F' )
		self.view_flat_action.setCheckable( True )
		self.view_flat_action.setChecked( False )
		self.view_flat_action.setStatusTip( 'Render the mesh with flat shading' )
		self.connect( self.view_flat_action, QtCore.SIGNAL('triggered()'), self.ViewFlatAction )

		self.view_smooth_action = QtGui.QAction( '&Smooth shading', self )
		self.view_smooth_action.setShortcut( 'G' )
		self.view_smooth_action.setCheckable( True )
		self.view_smooth_action.setChecked( True )
		self.view_smooth_action.setStatusTip( 'Render the mesh with smooth shading' )
		self.connect( self.view_smooth_action, QtCore.SIGNAL('triggered()'), self.ViewSmoothAction )

		self.view_wireframe_action = QtGui.QAction( '&Wireframe', self )
		self.view_wireframe_action.setShortcut( 'D' )
		self.view_wireframe_action.setCheckable( True )
		self.view_wireframe_action.setChecked( False )
		self.view_wireframe_action.setStatusTip( 'Enable / Disable wireframe rendering' )
		self.connect( self.view_wireframe_action, QtCore.SIGNAL('triggered()'), self.ViewWireframeAction )

		self.view_aliasing_action = QtGui.QAction( '&Antialiasing', self )
		self.view_aliasing_action.setShortcut( 'A' )
		self.view_aliasing_action.setCheckable( True )
		self.view_aliasing_action.setChecked( True )
		self.view_aliasing_action.setStatusTip( 'Enable / Disable antialiasing' )
		self.connect( self.view_aliasing_action, QtCore.SIGNAL('triggered()'), self.ViewAliasingAction )

		self.view_colorbar_action = QtGui.QAction( '&Color bar', self )
		self.view_colorbar_action.setShortcut( 'C' )
		self.view_colorbar_action.setCheckable( True )
		self.view_colorbar_action.setChecked( False )
		self.view_colorbar_action.setStatusTip( 'Enable / Disable color bar display' )
		self.connect( self.view_colorbar_action, QtCore.SIGNAL('triggered()'), self.ViewColorBarAction )

		view_reset_action = QtGui.QAction( '&Reset', self )
		view_reset_action.setShortcut( 'R' )
		view_reset_action.setStatusTip( 'Reset the viewing parameters' )
		self.connect( view_reset_action, QtCore.SIGNAL('triggered()'), self.ViewResetAction )

		# Create the menu bar
		menu_bar = self.menuBar()

		file_menu = menu_bar.addMenu( '&File' )
		file_menu.addAction( file_open_action )
		file_menu.addAction( file_save_action )
		file_menu.addSeparator()
		file_menu.addAction( file_check_action )
		file_menu.addSeparator()
		file_menu.addAction( file_close_action )
		file_menu.addAction( file_exit_action )

		view_menu = menu_bar.addMenu( '&View' )
		view_menu.addAction( self.view_flat_action )
		view_menu.addAction( self.view_smooth_action )
		view_menu.addSeparator()
		view_menu.addAction( self.view_wireframe_action )
		view_menu.addAction( self.view_aliasing_action )
		view_menu.addSeparator()
		view_menu.addAction( self.view_colorbar_action )
		view_menu.addSeparator()
		view_menu.addAction( view_reset_action )

		# Create the OpenGL frame
		self.opengl_widget = OpenGLWidget( self )
		self.setCentralWidget( self.opengl_widget )


	#-
	#
	# FileOpenAction
	#
	#-
	#
	def FileOpenAction( self ) :

		# Open file dialog
		(filename, selected_filter) = QFileDialog.getOpenFileName( self, 'Open a VRML File', '',
			'VRML files (*.vrml *.wrl *.x3d *.x3dv *.iv);;All files (*.*)' )

		# Check filename
		if not filename : return

		# Read VRML/X3D/Inventor file
		self.mesh = ReadVrml( unicode(filename) )

		# Compute mesh normals if necessary
		if len(self.mesh.vertex_normals) != len(self.mesh.vertices) :
			self.mesh.UpdateNormals()

		# Record neighborhood informations
		self.mesh.UpdateNeighbors()

		# Send the mesh to the OpenGL viewer
		self.opengl_widget.LoadMesh( self.mesh )


	#-
	#
	# FileSaveAction
	#
	#-
	#
	def FileSaveAction( self ) :

		# Nothing to save
		if not self.mesh : return

		# Open file dialog
		(filename, selected_filter) = QFileDialog.getSaveFileName( self, 'Save to a VRML File', '',
			'VRML files (*.vrml *.wrl *.x3d *.x3dv *.iv);;All files (*.*)' )

		# Check filename
		if not filename : return

		# Save VRML/X3D/Inventor file
		WriteVrml( self.mesh, unicode(filename) )


	#-
	#
	# FileCheckAction
	#
	#-
	#
	def FileCheckAction( self ) :

		# Nothing to check
		if not self.mesh : return

		# Check different parameters of the mesh
		CheckMesh( self.mesh )
		CheckNeighborhood( self.mesh )


	#-
	#
	# FileCloseAction
	#
	#-
	#
	def FileCloseAction( self ) :

		# Close the mesh
		self.opengl_widget.Close()
		self.mesh = None


	#-
	#
	# ViewFlatAction
	#
	#-
	#
	def ViewFlatAction( self ) :

		# Set flat shading
		self.view_flat_action.setChecked( True )
		self.view_smooth_action.setChecked( False )
		self.opengl_widget.SetShader( 'FlatShading' )


	#-
	#
	# ViewSmoothAction
	#
	#-
	#
	def ViewSmoothAction( self ) :

		# Set smooth shading
		self.view_flat_action.setChecked( False )
		self.view_smooth_action.setChecked( True )
		self.opengl_widget.SetShader( 'SmoothShading' )


	#-
	#
	# ViewWireframeAction
	#
	#-
	#
	def ViewWireframeAction( self ) :

		# Enable / Disable wireframe
		self.view_wireframe_action.setChecked( self.view_wireframe_action.isChecked() )
		self.opengl_widget.SetWireframe( self.view_wireframe_action.isChecked() )


	#-
	#
	# ViewAliasingAction
	#
	#-
	#
	def ViewAliasingAction( self ) :

		# Enable / Disable antialiasing
		self.view_aliasing_action.setChecked( self.view_aliasing_action.isChecked() )
		self.opengl_widget.SetAntialiasing( self.view_aliasing_action.isChecked() )


	#-
	#
	# ViewColorBarAction
	#
	#-
	#
	def ViewColorBarAction( self ) :

		# Enable / Disable color bar display
		self.view_colorbar_action.setChecked( self.view_colorbar_action.isChecked() )
		self.opengl_widget.SetColorBar( self.view_colorbar_action.isChecked() )


	#-
	#
	# ViewResetAction
	#
	#-
	#
	def ViewResetAction( self ) :

		# Reset model transformation
		self.opengl_widget.Reset()







