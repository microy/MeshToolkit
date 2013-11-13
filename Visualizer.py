# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                Visualizer.py
#                             -------------------
#    update               : 2013-11-13
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
OpenGL.FORWARD_COMPATIBLE_ONLY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Mesh import *
from Shader import *
from Transformation import *
import math
import numpy



#--
#
# Visualizer
#
#--
#
# Display a mesh with OpenGL
#
class Visualizer :


	#
	# Initialisation
	#
	def __init__( self, mesh=None, title="Untitled Window", width=1024, height=768 ) :
		# Initialise member variables
		self.mesh = None
		self.width  = width
		self.height = height
		self.trackball_transform = numpy.identity( 4 )
		self.shader_program_id = 0
		self.vertex_array_id = 0
		self.vertex_buffer_id = 0
		self.face_buffer_id = 0
		self.normal_buffer_id = 0
		self.color_buffer_id = 0
		# Initialise OpenGL / GLUT
		glutInit()
		glutInitWindowSize( self.width, self.height )
		glutCreateWindow( title )
		glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH )
		# GLUT function binding
		glutReshapeFunc( self.Reshape )
		glutKeyboardFunc( self.Keyboard )
		glutDisplayFunc( self.Display )
		glutMouseFunc( self.Mouse )
		glutIdleFunc( self.Idle )
		glutCloseFunc( self.Close )
		# Color configuration
		glClearColor( 1, 1, 1, 1 )
		# Load mesh
		if mesh : self.LoadMesh( mesh )


	#
	# Load mesh
	#
	def LoadMesh( self, mesh ) :
		# Initialisation
		self.mesh = mesh
		# Create and compile GLSL program
		self.shader_program_id = LoadShaders()
		# Vertex array object
		self.vertex_array_id = glGenVertexArrays( 1 )
		glBindVertexArray( self.vertex_array_id )
		# Face buffer object
		self.face_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, self.face_buffer_id )
		glBufferData( GL_ELEMENT_ARRAY_BUFFER, mesh.faces, GL_STATIC_DRAW )
		# Vertex buffer object
		self.vertex_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.vertex_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, mesh.vertices, GL_STATIC_DRAW )
		glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, None )
		glEnableVertexAttribArray( 0 )
		# Normal buffer object
		self.normal_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.normal_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, mesh.vertex_normals, GL_STATIC_DRAW )
		glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 0, None )
		glEnableVertexAttribArray( 1 )
		# Color buffer object
		self.color_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.color_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, mesh.colors, GL_STATIC_DRAW )
		glVertexAttribPointer( 2, 3, GL_FLOAT, GL_FALSE, 0, None )
		glEnableVertexAttribArray( 2 )
		# Cleanup
		glBindBuffer( GL_ARRAY_BUFFER, 0 )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, 0 )
		glBindVertexArray( 0 )


	#
	# Keyboard
	#
	def Keyboard( self, key, mouseX, mouseY ) :
		glutPostRedisplay()

	#
	# Mouse
	#
	def Mouse( self, button, state, x, y ) :
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
	def MouseLeftClick( self, x, y ) :
		pass

	#
	# MouseMiddleClick
	#
	def MouseMiddleClick( self, x, y ) :
		pass

	#
	# MouseRightClick
	#
	def MouseRightClick( self, x, y ) :
		pass

	#
	# Reshape
	#
	def Reshape( self, width, height ) :
		self.width  = width
		self.height = height
		glViewport( 0, 0, self.width, self.height )


	#
	# Display
	#
	def Display( self ):
		# Clear all pixels and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		# Is there a mesh to display ?
		if self.mesh :
			# Draw the mesh
			glBindVertexArray( self.vertex_array_id )
			glDrawElements( GL_TRIANGLES, len(self.mesh.faces), GL_UNSIGNED_INT, 0 )
                # Swap buffers
		glutSwapBuffers()
		glutPostRedisplay()


	#
	# Idle
	#
	def Idle( self ) :
		glutPostRedisplay()


	#
	# Close
	#
	def Close( self ) :
		# Delete shader program
		glUseProgram( 0 )
		glDeleteProgram( self.shader_program_id )
		# Delete buffer objects
		glDeleteBuffers( 1, [ self.face_buffer_id ] )
		glDeleteBuffers( 1, [ self.vertex_buffer_id ] )
		glDeleteBuffers( 1, [ self.normal_buffer_id ] )
		glDeleteBuffers( 1, [ self.color_buffer_id ] )
		# Delete vertex array
		glDeleteVertexArrays( 1, [ self.vertex_array_id ] )

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
