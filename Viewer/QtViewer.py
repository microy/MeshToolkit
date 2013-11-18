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
from .QtViewerWidget import *




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
	def __init__( self, mesh=None, title="Untitled Window", width=1024, height=768 ) :

		# Initialise QMainWindow		
		QMainWindow.__init__( self )

		# Set the window title
		self.setWindowTitle( title )

		# Resize the main window
		self.resize( width, height )

		# Move the main window
		self.move( 100, 100 )

		# Create the OpenGL frame
		qtviewer_widget = QtViewerWidget( self, mesh )
		self.setCentralWidget( qtviewer_widget )







