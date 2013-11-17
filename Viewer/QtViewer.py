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
# OpenGL, QT, NumPy
#
import OpenGL
OpenGL.FORWARD_COMPATIBLE_ONLY = True
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *

from PyQt4 import QtGui, QtCore
from PyQt4.QtOpenGL import *

from math import *
from numpy import *

from AxesViewer import *
from MeshViewer import *
from Transformation import *




#--
#
# QtViewer
#
#--
#
# Create a mesh viewer with Qt
#
class QtViewer( QtGui.QMainWindow ) :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self, mesh=None, title="Untitled Window", width=1024, height=768 ) :

		# Initialise QMainWindow		
		QtGui.QMainWindow.__init__( self )

		# Set the window title
		self.setWindowTitle( title )

		# Resize the main window
		self.resize( width, height )

		# Move the main window
		self.move( 100, 100 )

		# Create OpenGL frame
		qtviewer_widget = QtViewerWidget( self, mesh )
		self.setCentralWidget( qtviewer_widget )






#--
#
# QtViewerWidget
#
#--
#
# Create an OpenGL frame with Qt
#
class QtViewerWidget( QGLWidget ) :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self, parent=None, mesh=None ) :

		# Initialise QtGLWidget
		QGLWidget.__init__( self, parent )
		self.setMouseTracking( True )

		# Initialise member variables
		self.mesh = mesh
		self.mesh_viewer = None
		self.axes_viewer = None
		self.frame_count = 0
		self.previous_mouse_position = array( [0, 0] )
		self.previous_trackball_position = array( [0.0, 0.0, 0.0] )
		self.motion_state = 0


	#-
	#
	# initializeGL
	#
	#-
	#
	def initializeGL( self ) :

		# OpenGL configuration
		glClearColor( 1, 1, 1, 1 )
		glEnable( GL_DEPTH_TEST )
		glDepthFunc( GL_LESS )
		glEnable( GL_CULL_FACE )

		# Mesh viewer initialisation
		self.mesh_viewer = MeshViewer( self.mesh, self.width(), self.height() )

		# XYZ axes viewer initialisation
		self.axes_viewer = AxesViewer()


	#-
	#
	# paintGL
	#
	#-
	#
	def paintGL( self ) :

		# Framerate counter
		self.frame_count += 1

		# Clear all pixels and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

		# Display the mesh
		self.mesh_viewer.Display()

		# Resize the viewport
		glViewport( 0, 0, 100, 100 )

		# Display the XYZ axes
		self.axes_viewer.Display()

		# Restore the viewport
		glViewport( 0, 0, self.width(), self.height() )

		# Swap buffers
		self.swapBuffers()


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
		self.mesh_viewer.SetPerspectiveMatrix( width, height )




	#-
	#
	# mousePressEvent
	#
	#-
	#
	def mousePressEvent( self, mouseEvent ) :

		# Left button
		if int(mouseEvent.buttons()) & QtCore.Qt.LeftButton :

			# Trackball rotation
			self.motion_state = 1
			self.previous_trackball_position = self.TrackballMapping( mouseEvent.x(), mouseEvent.y() )

		# Middle button
		elif int(mouseEvent.buttons()) & QtCore.Qt.MidButton :

			# XY translation
			self.motion_state = 2
			self.previous_mouse_position = array([ mouseEvent.x(), mouseEvent.y() ])

		# Right button
		elif int(mouseEvent.buttons()) & QtCore.Qt.RightButton :

			# Z translation
			self.motion_state = 3
			self.previous_mouse_position = array([ mouseEvent.x(), mouseEvent.y() ])


	#-
	#
	# mouseReleaseEvent
	#
	#-
	#
	def mouseReleaseEvent( self, mouseEvent ) :

		# Stop motion
		self.motion_state = 0
		# Update display
		self.update()



	#-
	#
	# mouseMoveEvent
	#
	#-
	#
	def mouseMoveEvent( self, mouseEvent ) :

		# Trackball rotation
                if self.motion_state == 1 :

                        current_position = self.TrackballMapping( mouseEvent.x(), mouseEvent.y() )
                        rotation_axis = cross( self.previous_trackball_position, current_position )
                        rotation_angle = 90.0 * norm(current_position - self.previous_trackball_position) * 1.5
                        self.previous_trackball_position = current_position
			RotateMatrix( self.mesh_viewer.trackball_transform, rotation_angle, rotation_axis[0], rotation_axis[1], rotation_axis[2] )
			self.axes_viewer.trackball_transform = self.mesh_viewer.trackball_transform
			self.update()

		# XY translation
                elif self.motion_state ==  2 :

                        self.mesh_viewer.model_translation[0] -= float(self.previous_mouse_position[0]-mouseEvent.x())*0.001
                        self.mesh_viewer.model_translation[1] += float(self.previous_mouse_position[1]-mouseEvent.y())*0.001
                        self.previous_mouse_position = array([ mouseEvent.x(), mouseEvent.y() ])
			self.update()

		# Z translation
                elif self.motion_state ==  3 :

                        self.mesh_viewer.model_translation[2] -= float(self.previous_mouse_position[1]-mouseEvent.y()) * 0.001
                        self.previous_mouse_position = array([ mouseEvent.x(), mouseEvent.y() ])
			self.update()





	#-
	#
	# TrackballMapping
	#
	#-
	#
	# Map the mouse coordinates to a ball
	# Adapted from Nate Robins' programs
	# http://www.xmission.com/~nate
	#
	def TrackballMapping( self, x, y ) :

		v = zeros( 3 )
		v[0] = ( 2.0 * float(x) - float(self.width()) ) / float(self.width())
		v[1] = ( float(self.height()) - 2.0 * float(y) ) / float(self.height())
		d = norm( v )
		if d > 1.0 : d = 1.0
		v[2] = cos( pi / 2.0 * d )

		return v / norm(v)



