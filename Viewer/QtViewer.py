# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 QtViewer.py
#                             -------------------
#    update               : 2013-11-18
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
# Qt
#
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from .QtViewerGLWidget import *
from Core.Vrml import *




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

		# Set the window title
		self.setWindowTitle( 'QtViewer' )

		# Resize the main window
		self.resize( 1024, 768 )

		# Move the main window
		self.move( 100, 100 )

		# Set the status bar
		self.statusBar()

		# Create actions
		open_action = QtGui.QAction( '&Open...', self )
		open_action.setShortcut( 'Ctrl+O' )
		open_action.setStatusTip( 'Open a file' )
		self.connect( open_action, QtCore.SIGNAL('triggered()'), self.OpenAction )
		close_action = QtGui.QAction( '&Close', self )
		close_action.setShortcut( 'Ctrl+W' )
		close_action.setStatusTip( 'Close the current file' )
		self.connect( close_action, QtCore.SIGNAL('triggered()'), self.CloseAction )
		exit_action = QtGui.QAction( '&Exit', self )
		exit_action.setShortcut( 'Esc' )
		exit_action.setStatusTip( 'Exit application' )
		self.connect( exit_action, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()') )

		# Create menu bar
		menubar = self.menuBar()
		fileMenu = menubar.addMenu( '&File' )
		fileMenu.addAction( open_action )
		fileMenu.addSeparator()
		fileMenu.addAction( close_action )
		fileMenu.addAction( exit_action )

		# Create the OpenGL frame
		self.opengl_widget = QtViewerGLWidget( self )
		self.setCentralWidget( self.opengl_widget )


	#-
	#
	# OpenAction
	#
	#-
	#
	def OpenAction( self ) :

 		filename = QFileDialog.getOpenFileName( self, 'Open VRML input File', '', 'VRML Files (*.wrl)' )
		if filename : self.opengl_widget.LoadMesh( ReadVrmlFile(filename) )





	#-
	#
	# CloseAction
	#
	#-
	#
	def CloseAction( self ) :

		self.opengl_widget.Close()







