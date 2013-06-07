# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                Visualizer.py
#                             -------------------
#    update               : 2013-06-07
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


#
# External dependencies
#
import OpenGL
OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_LOGGING = False
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Mesh import *
import math
import numpy


class Visualizer :


	#
	# Initialisation
	#
	def __init__( self, mesh=None, title="Untitled Window", width=640, height=480 ) :
		self.LoadMesh( mesh )
		self.width  = width
		self.height = height
		self.keybindings = {chr(27):exit}
		self.trackball_transform = numpy.identity( 4 )
		glutInit()
		glutInitWindowSize( self.width, self.height )
		glutCreateWindow( title )
		glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH )
		glClearColor( 0, 0, 0, 0 )
		glutReshapeFunc( self.Reshape )
		glutKeyboardFunc( self.Keyboard )
		glutDisplayFunc( self.Display )
		glutMouseFunc( self.Mouse )
		glShadeModel( GL_FLAT )

	#
	# Load mesh
	#
	def LoadMesh( self, mesh ) :
		self.mesh = mesh
		if mesh is None : pass
		pass

	#
	# Keyboard
	#
	def Keyboard( self, key, mouseX, mouseY ):
#		self.keybindings.get(key, noop)()
		glutPostRedisplay()

	#
	# Mouse
	#
	def Mouse( self, button, state, x, y ):
		if button == GLUT_LEFT_BUTTON:
			self.MouseLeftClick(x, y)
		elif button == GLUT_MIDDLE_BUTTON:
			self.MouseMiddleClick(x, y)
		elif button == GLUT_RIGHT_BUTTON:
			self.MouseRightClick(x, y)
		else:
			raise ValueError(button)
		glutPostRedisplay()

	#
	# MouseLeftClick
	#
	def MouseLeftClick( self, x, y ):
		pass

	#
	# MouseMiddleClick
	#
	def MouseMiddleClick( self, x, y ):
		pass

	#
	# MouseRightClick
	#
	def MouseRightClick( self, x, y ):
		pass

	#
	# Reshape
	#
	def Reshape( self, width, height ):
		self.width  = width
		self.height = height
		glViewport( 0, 0, self.width, self.height )
		glMatrixMode( GL_PROJECTION )
		glLoadIdentity()
		aspect = float(self.height) / float(self.width)
		gluPerspective( 30, 1.0/aspect, 1, 20 )
		glMatrixMode( GL_MODELVIEW )
		glLoadIdentity()

	#
	# Display
	#
	def Display( self ):
		# Clear all pixels
		glClear(GL_COLOR_BUFFER_BIT)
		# Draw white polygon (rectangle) with corners at (0.25, 0.25, 0) and (0.75, 0.75, 0)
		glColor3f(1, 1, 1)
		glLoadIdentity()
		gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
		glScalef(1, 2, 1)
		glutWireCube(1)
		glFlush()

	#--
	#
	# TrackballMapping
	#
	#--
	# Adapted from Nate Robins programs
	# http://www.xmission.com/~nate
	def TrackballMapping( x, y ) :
		v = numpy.zeros( 3 )
		v[0] = ( 2.0 * float(x) - float(self.width) ) / float(self.width)
		v[1] = ( float(self.height) - 2.0 * float(y) ) / float(self.height)
		d = numpy.linalg.norm( v )
		if d > 1.0 : d = 1.0
		v[2] = math.cos( math.pi / 2.0 * d );
		return v / numpy.linalg.norm(v)

	#
	# Run
	#
	@staticmethod
	def Run():
		# Start up the main loop
		glutMainLoop()
