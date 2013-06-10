# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                Visualizer.py
#                             -------------------
#    update               : 2013-06-10
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
		# Initialise member variables
		self.width  = width
		self.height = height
		self.keybindings = {chr(27):exit}
		self.trackball_transform = numpy.identity( 4 )
		# Initialise OpenGL / GLUT
		glutInit()
		glutInitContextVersion( 3, 3 )
		glutInitContextFlags( GLUT_FORWARD_COMPATIBLE )
		glutInitContextProfile( GLUT_CORE_PROFILE )
		glutInitWindowSize( self.width, self.height )
		glutCreateWindow( title )
		glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH )
		glClearColor( 0, 0, 0, 0 )
		# GLUT function binding
		glutReshapeFunc( self.Reshape )
		glutKeyboardFunc( self.Keyboard )
		glutDisplayFunc( self.Display )
		glutMouseFunc( self.Mouse )
		glutIdleFunc( self.Idle )
		glutCloseFunc( self.Close )
		# OpenGL parameters
		glShadeModel( GL_FLAT )
		glEnable( GL_DEPTH_TEST )
		glDepthFunc( GL_LESS )
		glEnable( GL_CULL_FACE )
		glCullFace( GL_FRONT_AND_BACK )
		glFrontFace( GL_CCW )
#		glEnableClientState( GL_VERTEX_ARRAY )
#		glEnableClientState( GL_COLOR_ARRAY )
#		glEnableClientState( GL_NORMAL_ARRAY )
		glEnable( GL_POLYGON_SMOOTH )
		glEnable( GL_BLEND )
		glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
		glHint( GL_POLYGON_SMOOTH_HINT, GL_NICEST )
		# Load mesh
		self.LoadMesh( mesh )

	#
	# Load mesh
	#
	def LoadMesh( self, mesh=None ) :
		# Initialisation
		self.Close()		
		self.vertex_array_id = 0
		self.vertex_buffer_id = 0
		self.face_buffer_id = 0
		self.mesh = mesh
		# Return if no mesh
		if mesh is None : pass
		# Vertex Array Object
		glGenVertexArrays( 1, vertex_array_id )
		glBindVertexArray( vertex_array_id )
		# Vertex buffer object
		glGenBuffers( 1, vertex_buffer_id )
		glBindBuffer( GL_ARRAY_BUFFER, vertex_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, len(mesh.vertices), mesh.vertices, GL_STATIC_DRAW )
		# Face buffer object
		glGenBuffers( 2, face_buffer_id )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, face_buffer_id )
		glBufferData( GL_ELEMENT_ARRAY_BUFFER, len(mesh.faces), mesh.faces, GL_STATIC_DRAW )


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
		# Initialisation
		# Clear all pixels and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		glColor3f(1, 1, 1)
		glLoadIdentity()
		gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
		glScalef(1, 2, 1)

		# Is there a mesh to display ?
		if mesh is None : pass

		glBindVertexArray( self.vertex_array_id )
		glDrawElements( GL_TRIANGLES, len(self.mesh.faces), GL_INT, 0 )
		glBindVertexArray (0);

		glutSwapBuffers()
		glutPostRedisplay()

	#
	# Idle
	#
	def Idle( self ):
		glutPostRedisplay()


	#
	# Close
	#
	def Close( self ):
		# TODO:
		# Destroy Buffer Objects
#		glDisableVertexAttribArray(1);
#		glDisableVertexAttribArray(0);
#		glBindBuffer( GL_ARRAY_BUFFER, 0 )
#		glDeleteBuffers( 1, self.BufferId )
#		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, 0 )
#		glDeleteBuffers( 2, self.IndexBufferId )
#		glBindVertexArray( 0 )
#		glDeleteVertexArrays( 1, self.VaoId )

	#
	# TrackballMapping
	#
	def TrackballMapping( self, x, y ) :
		# Adapted from Nate Robins' programs
		# http://www.xmission.com/~nate
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
