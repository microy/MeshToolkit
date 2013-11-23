# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 ColorBar.py
#                             -------------------
#    update               : 2013-11-23
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
from Core.Color import Value2Color, Value2ColorAlternate
from .Shader import LoadShader
from .Transformation import OrthographicMatrix
import OpenGL
OpenGL.FORWARD_COMPATIBLE_ONLY = True
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from numpy import array, float32, zeros



#--
#
# ColorBar
#
#--
#
# Display a pseudo-color scale with OpenGL
#
class ColorBar :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self ) :

		# Generate vertices and colors
		self.size = 50
		vertices = zeros( (self.size * 2, 3), dtype=float32 )
		colors = zeros( (self.size * 2, 3), dtype=float32 )
		for i in range( self.size ) :
			vertices[i*2]   = [ -0.5, float(i) / (self.size-1) - 0.5, -0.5 ]
			vertices[i*2+1] = [ 0.5, float(i) / (self.size-1) - 0.5, -0.5 ]
			colors[i*2] = Value2ColorAlternate( float(i)/float(self.size-1) )
			colors[i*2+1] = Value2ColorAlternate( float(i)/float(self.size-1) )

		# Load the shader
		self.shader_program_id = LoadShader( 'AxisViewer' )

		# Use the shader program
		glUseProgram( self.shader_program_id )

		# Vertex array object
		self.vertex_array_id = glGenVertexArrays( 1 )
		glBindVertexArray( self.vertex_array_id )

		# Vertex buffer object
		self.vertex_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.vertex_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW )
		glEnableVertexAttribArray( 0 )
		glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Color buffer object
		self.color_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.color_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW )
		glEnableVertexAttribArray( 1 )
		glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Release the buffers
		glBindBuffer( GL_ARRAY_BUFFER, 0 )
		glBindVertexArray( 0 )

		# Release the shader program
		glUseProgram( 0 )

		# Initialise the Model-View-Projection matrix
		self.mvp_matrix = OrthographicMatrix( -1, 1, -1, 1, 0.1, 10.0 )





	#-
	#
	# Display
	#
	#-
	#
	def Display( self ) :

		# Use the shader program
		glUseProgram( self.shader_program_id )

		# Send the Model-View-Projection matrix to the shader
		glUniformMatrix4fv( glGetUniformLocation( self.shader_program_id, "MVP_Matrix" ), 1, GL_TRUE, self.mvp_matrix )

		# Vertex array object
		glBindVertexArray( self.vertex_array_id )

		# Draw the mesh
		glDrawArrays( GL_TRIANGLE_STRIP, 0, self.size*2 )

		# Release the vertex array object
		glBindVertexArray( 0 )

		# Release the shader program
		glUseProgram( 0 )




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


