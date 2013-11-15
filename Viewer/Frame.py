# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                  Frame.py
#                             -------------------
#    update               : 2013-11-15
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
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
from numpy import *
from Shader import *
from Transformation import *



#--
#
# ErrorCheckup
#
#--
#
# Check for OpenGL errors
#
def ErrorCheckup( info='' ) :
	error = glGetError()
	if error != GL_NO_ERROR :
		raise RuntimeError( info + '\n' + gluErrorString(error) )




#--
#
# Frame
#
#--
#
# Create an OpenGL frame
#
class Frame :


	#
	# Initialisation
	#
	def __init__( self, title="Untitled Window", width=1024, height=768 ) :

		# Initialise member variables
		self.title = title
		self.width  = width
		self.height = height
		self.frame_count = 0
		self.mvp_matrix_id = -1
		self.shader_program_id = -1
		self.projection_matrix = identity( 4, dtype=float32 )
		self.view_matrix = identity( 4, dtype=float32 )
		self.model_matrix = identity( 4, dtype=float32 )
		self.mvp_matrix = identity( 4, dtype=float32 )
		self.trackball_transform = identity( 4, dtype=float32 )

		# Initialise OpenGL / GLUT
		glutInit()
		glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH )
		glutInitWindowSize( self.width, self.height )
		glutInitWindowPosition( 100, 100 )
		glutCreateWindow( title )

		# GLUT function binding
		glutCloseFunc( self.Close )
		glutDisplayFunc( self.Display )
		glutIdleFunc( self.Idle )
		glutKeyboardFunc( self.Keyboard )
		glutMouseFunc( self.Mouse )
		glutReshapeFunc( self.Reshape )
		glutTimerFunc( 0, self.Timer, 0 )

		# OpenGL configuration
		glClearColor( 1, 1, 1, 1 )
#		glEnable( GL_DEPTH_TEST )
#		glDepthFunc( GL_LESS )
#		glEnable( GL_CULL_FACE )

		# Load the shader
		self.shader_program_id = LoadShaders( 'Color' )

		# Initialise the transformation matrices
#		RotateMatrixZ(self.model_matrix, 45 )
#		TranslateMatrix( self.model_matrix, 0.5, 0.5, 5.0 )
#		self.projection_matrix = PerspectiveMatrix( 60.0, float(self.width) / float(self.height), 0.1, 100.0 )
#		self.projection_matrix = OrthoMatrix( -10.0, 10.0, -10.0, 10.0, 0.1, 100.0 )
#		self.view_matrix = LookAt( array([4.0,3.0,3.0]), array([0.0,0.0,0.0]), array([0.0,1.0,0.0]) )

		# Compute Model-View-Projection matrix
		self.mvp_matrix = dot( self.projection_matrix, dot( self.view_matrix, self.model_matrix ) )

		# Get a handle for the transformation matrix
		self.mvp_matrix_id = glGetUniformLocation( self.shader_program_id, "MVP_Matrix" )

		# Send the transformation matrices to the shader
		glUniformMatrix4fv( self.mvp_matrix_id, 1, GL_FALSE, self.mvp_matrix )

		# Error checkup
		ErrorCheckup( 'Initialisation failed.' )




	#
	# PrintInfo
	#
	def PrintInfo( self ) :

		# Display OpenGL driver informations
		print '~~~ OpenGL Informations ~~~'
		print '  Vendor :   ' + glGetString( GL_VENDOR )
		print '  Renderer : ' + glGetString( GL_RENDERER )
		print '  Version :  ' + glGetString( GL_VERSION )
		print '  Shader :   ' + glGetString( GL_SHADING_LANGUAGE_VERSION )


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

		# Resize the viewport
		self.width  = width
		self.height = height
		glViewport( 0, 0, self.width, self.height )
#		self.projection_matrix = PerspectiveMatrix( 60, float(self.width) / float(self.height), 0.1, 100.0 )
#		glUniformMatrix4fv( self.projection_matrix_id, 1, GL_FALSE, self.projection_matrix )


	#
	# Display
	#
	def Display( self ) :
		# Clear all pixels and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		# Framerate counter
		self.frame_count += 1
		# Swap buffers
		glutSwapBuffers()
		glutPostRedisplay()


	#
	# Idle
	#
	def Idle( self ) :

		# Redraw
		glutPostRedisplay()


	#
	# Close
	#
	def Close( self ) :

		# Delete shader program
		glUseProgram( 0 )
		glDeleteProgram( self.shader_program_id )

		# Error checkup
		ErrorCheckup( 'Error while deleting the shader program' )

		# Initialise member variables
		self.mvp_matrix_id = -1
		self.shader_program_id = -1
		self.projection_matrix = identity( 4, dtype=float32 )
		self.view_matrix = identity( 4, dtype=float32 )
		self.model_matrix = identity( 4, dtype=float32 )
		self.mvp_matrix = identity( 4, dtype=float32 )
		self.trackball_transform = identity( 4, dtype=float32 )



	#
	# TrackballMapping
	#
	def TrackballMapping( self, x, y ) :
		# Adapted from Nate Robins' programs
		# http://www.xmission.com/~nate
		v = zeros( 3 )
		v[0] = ( 2.0 * float(x) - float(self.width) ) / float(self.width)
		v[1] = ( float(self.height) - 2.0 * float(y) ) / float(self.height)
		d = norm( v )
		if d > 1.0 : d = 1.0
		v[2] = cos( pi / 2.0 * d )
		return v / norm(v)


	#
	# Timer
	#
	def Timer( self, value ) :

		# Framerate counter
		if value :
			title = self.title + ' - {} FPS @ {} x {}'.format( self.frame_count * 4, self.width, self.height )
			glutSetWindowTitle( title )     
		self.frame_count = 0
		glutTimerFunc( 250, self.Timer, 1 )
	

	#
	# Run
	#
	@staticmethod
	def Run() :
		# Start up the main loop
		glutMainLoop()




