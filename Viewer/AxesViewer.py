# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                AxesViewer.py
#                             -------------------
#    update               : 2013-11-17
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
import OpenGL
OpenGL.FORWARD_COMPATIBLE_ONLY = True
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from numpy import *
from Shader import *
from Transformation import *



#--
#
# AxesViewer
#
#--
#
# Display XYZ-axes in OpenGL
#
class AxesViewer() :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self ) :

		# Vertices
		self.vertices = array( [
			[0, 0, 0], [1, 0, 0],
			[0, 0, 0], [0, 1, 0],
			[0, 0, 0], [0, 0, 1] ] , dtype=float32 )

		# Colors
		self.colors = array( [
			[1, 0, 0], [1, 0, 0],
			[0, 1, 0], [0, 1, 0],
			[0, 0, 1], [0, 0, 1] ] , dtype=float32 )

		# Load the shader
		self.shader_program_id = LoadShaders( 'Color' )

		# Use the shader program
		glUseProgram( self.shader_program_id )

		# Vertex array object
		self.vertex_array_id = glGenVertexArrays( 1 )
		glBindVertexArray( self.vertex_array_id )

		# Vertex buffer object
		self.vertex_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.vertex_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW )
		glEnableVertexAttribArray( 0 )
		glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Color buffer object
		self.color_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.color_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, self.colors.nbytes, self.colors, GL_STATIC_DRAW )
		glEnableVertexAttribArray( 1 )
		glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Release the buffers
		glBindBuffer( GL_ARRAY_BUFFER, 0 )
		glBindVertexArray( 0 )

		# Release the shader program
		glUseProgram( 0 )

		# OpenGL error checking
		if glGetError() != GL_NO_ERROR :
			raise RuntimeError('Error while creating XYZ axes viewer.' )

		# Initialise the view matrix
		self.view_matrix = LookAtMatrix( [0, 0, 2], [0, 0, 0], [0, 1, 0] )

		# Initialise the projection matrix
		self.projection_matrix = PerspectiveMatrix( 45.0, 1, 0.1, 100.0 )

		# Initialise rotation
		self.trackball_transform = identity( 4, dtype=float32 )





	#-
	#
	# Display
	#
	#-
	#
	def Display( self ) :

		# Increase line width
		glLineWidth( 2.0 )

		# Use the shader program
		glUseProgram( self.shader_program_id )

		# Compute model transformation matrix
		self.model_matrix = identity( 4, dtype=float32 )
		self.model_matrix = dot( self.model_matrix, self.trackball_transform )

		# Compute Model-View-Projection matrix
		self.mvp_matrix = dot( self.projection_matrix, dot( self.view_matrix, self.model_matrix ) )

		# Send the transformation matrices to the shader
		glUniformMatrix4fv( glGetUniformLocation( self.shader_program_id, "MVP_Matrix" ), 1, GL_TRUE, self.mvp_matrix )

		# Vertex array object
		glBindVertexArray( self.vertex_array_id )

		# Draw the mesh
		glDrawArrays( GL_LINES, 0, 6)

		# Release the vertex array object
		glBindVertexArray( 0 )

		# Release the shader program
		glUseProgram( 0 )

		# Restore line width
		glLineWidth( 1.0 )





	#-
	#
	# Close
	#
	#-
	#
	def Close( self ) :

		# Delete shader program
		glUseProgram( 0 )
		glDeleteProgram( self.shader_program_id )

		# Delete buffer objects
		glDeleteBuffers( 1, array([ self.vertex_buffer_id ]) )
		glDeleteBuffers( 1, array([ self.color_buffer_id ]) )

		# Delete vertex array
		glDeleteVertexArrays( 1, array([self.vertex_array_id]) )

		# OpenGL error checking
		if glGetError() != GL_NO_ERROR :
			raise RuntimeError('OpenGL error while closing the mesh.' )


