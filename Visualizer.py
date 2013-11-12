# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                Visualizer.py
#                             -------------------
#    update               : 2013-11-12
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
import math
import numpy


#
# Vertex shader code
#
vertex_shader_source = '''
#version 330
 
in vec4 position;
void main()
{
	gl_Position = position;
}
'''


#
# Fragment shader code
#
fragment_shader_source = '''
#version 330
 
void main()
{
	gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
'''



#--
#
# Visualizer
#
#--
#
# Displaying a mesh with OpenGL 3.3+
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
		self.vertex_array_id = 0
		self.vertex_buffer_id = 0
		self.face_buffer_id = 0
		self.normal_buffer_id = 0
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
		# Create and compile GLSL program
		global vertex_shader_source, fragment_shader_source
		self.program_id = self.LoadShaders( vertex_shader_source, fragment_shader_source )
		# Load mesh
		if mesh : self.LoadMesh( mesh )


	#
	# Load OpenGL shaders
	#
	def LoadShaders( self, vertex_source, fragment_source ) :
		# Compile vertex shader
		vertex_shader = glCreateShader( GL_VERTEX_SHADER )
		glShaderSource( vertex_shader, vertex_source )
		glCompileShader( vertex_shader )
		# Check vertex shader
		if not glGetShaderiv( vertex_shader, GL_COMPILE_STATUS ) :
			print '~~~ Vertex shader info log :\n' + glGetShaderInfoLog( vertex_shader )
		# Compile fragment shader
		fragment_shader = glCreateShader( GL_FRAGMENT_SHADER )
		glShaderSource( fragment_shader, fragment_source )
		glCompileShader( fragment_shader )
		# Check fragment shader
		if not glGetShaderiv( fragment_shader, GL_COMPILE_STATUS ) :
			print '~~~ Fragment shader info log :\n' + glGetShaderInfoLog( fragment_shader )
		# Link the program
		program_id = glCreateProgram()
		glAttachShader( program_id, vertex_shader )
		glAttachShader( program_id, fragment_shader )
		glLinkProgram( program_id )
		# Check the program
		if not glGetProgramiv( program_id, GL_LINK_STATUS ) :
			print '~~~ Shader program info log :\n' + glGetProgramInfoLog( program_id )
		# Delete the shaders
		glDeleteShader( vertex_shader )
		glDeleteShader( fragment_shader )
		return program_id


	#
	# Load mesh
	#
	def LoadMesh( self, mesh ) :
		# Initialisation
		self.mesh = mesh
		# Vertex array object
		self.vertex_array_id = glGenVertexArrays( 1 )
		glBindVertexArray( self.vertex_array_id )
		# Vertex buffer object
		self.vertex_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.vertex_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, mesh.vertices, GL_STATIC_DRAW )
		# Normal buffer object
		self.normal_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.normal_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, mesh.vertex_normals, GL_STATIC_DRAW )
		# Face buffer object
		self.face_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, self.face_buffer_id )
		glBufferData( GL_ELEMENT_ARRAY_BUFFER, mesh.faces, GL_STATIC_DRAW )


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
		# Clear all pixels and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		# Is there a mesh to display ?
		if self.mesh is None : pass
                # Shader program
                glUseProgram( self.program_id )
		# Vertex buffer
		glEnableVertexAttribArray( 0 )
		glBindBuffer( GL_ARRAY_BUFFER, self.vertex_buffer_id )
		glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, None )
		# Normal buffer
		glEnableVertexAttribArray( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.normal_buffer_id )
		glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 0, None )
		# Face buffer
                glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, self.face_buffer_id )
		# Draw the mesh
		glDrawElements( GL_TRIANGLES, len(self.mesh.faces), GL_UNSIGNED_INT, 0 )
		# Cleanup
                glDisableVertexAttribArray( 0 )
                glDisableVertexAttribArray( 1 )
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
		# Delete buffer objects
		glDeleteBuffers( 1, [ self.vertex_buffer_id ] )
		glDeleteBuffers( 1, [ self.normal_buffer_id ] )
		glDeleteBuffers( 1, [ self.face_buffer_id ] )
		# Delete vertex array
		glDeleteVertexArrays( 1, [ self.vertex_array_id ] )
		# Delete shader program
		glDeleteProgram( self.program_id )

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
