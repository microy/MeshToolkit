# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                Visualizer.py
#                             -------------------
#    update               : 2013-06-03
#    copyright            : (C) 2013 by Michaël Roy
#    email                : michael.roy@u-bourgogne.fr
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


class Visualizer :


	#
	# Initialisation
	#
	def __init__( self, title="Untitled Window", width=500, height=500 ):
		self.width  = width
		self.height = height
		self.keybindings = {chr(27):exit}
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

	def Keyboard( self, key, mouseX, mouseY ):
#		self.keybindings.get(key, noop)()
		glutPostRedisplay()

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

	def MouseLeftClick( self, x, y ):
		pass

	def MouseMiddleClick( self, x, y ):
		pass

	def MouseRightClick( self, x, y ):
		pass

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

	def Display( self ):
		raise NotImplementedError

	@staticmethod
	def run():
		# Start up the main loop
		glutMainLoop()
