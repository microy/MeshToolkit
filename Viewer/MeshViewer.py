# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                MeshViewer.py
#                             -------------------
#    update               : 2013-11-24
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




#-
#
# External dependencies
#
#-
#
from Core.Container import GetBoundingSphere
from Shader import LoadShader
from Transformation import PerspectiveMatrix, TranslateMatrix
import OpenGL
OpenGL.FORWARD_COMPATIBLE_ONLY = True
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from numpy import array, identity, dot, float32, uint32





#--
#
# MeshViewer
#
#--
#
# Display a mesh with OpenGL
#
class MeshViewer() :


	#-
	#
	# Initialisation
	#
	#-
	#
	def __init__( self, width=1024, height=768 ) :

		# Initialise the OpenGL buffer IDs
		self.shader_program_id = -1
		self.vertex_array_id = -1
		self.vertex_buffer_id = -1
		self.face_buffer_id = -1
		self.normal_buffer_id = -1
		self.color_buffer_id = -1

		# Initialise the model parameters
		self.element_number = 0

		# Initialise the trackball transformation matrix
		self.trackball_transform = identity( 4, dtype=float32 )

		# Initialise the Projection transformation matrix
		self.projection_matrix = PerspectiveMatrix( 45.0, float(width)/float(height), 0.1, 100.0 )


	#-
	#
	# LoadMesh
	#
	#-
	#
	def LoadMesh( self, mesh ) :

		# Close previous mesh
		self.Close()

		# Cast input data (required for OpenGL)
		vertices = array( mesh.vertices, dtype=float32 )
		faces = array( mesh.faces, dtype=uint32 )
		normals = array( mesh.vertex_normals, dtype=float32 )
		colors = array( mesh.colors, dtype=float32 )

		# Normalize the model
		(center, radius) = GetBoundingSphere( mesh )
		vertices -= center
		vertices /= radius

		# Load the shader
		self.shader_program_id = LoadShader( 'SmoothShading' )

		# Use the shader program
		glUseProgram( self.shader_program_id )

		# Vertex array object
		self.vertex_array_id = glGenVertexArrays( 1 )
		glBindVertexArray( self.vertex_array_id )

		# Face buffer object
		self.face_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, self.face_buffer_id )
		glBufferData( GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW )

		# Vertex buffer object
		self.vertex_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.vertex_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW )
		glEnableVertexAttribArray( 0 )
		glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Normal buffer object
		self.normal_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.normal_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW )
		glEnableVertexAttribArray( 1 )
		glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Color buffer object
		if len(colors) :
			self.color_buffer_id = glGenBuffers( 1 )
			glBindBuffer( GL_ARRAY_BUFFER, self.color_buffer_id )
			glBufferData( GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW )
			glEnableVertexAttribArray( 2 )
			glVertexAttribPointer( 2, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Release the buffers
		glBindBuffer( GL_ARRAY_BUFFER, 0 )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, 0 )
		glBindVertexArray( 0 )

		# Release the shader program
		glUseProgram( 0 )

		# Setup model element number
		self.element_number = len(faces) * 3

		

	#-
	#
	# Display
	#
	#-
	#
	def Display( self ) :

		# Is there a mesh to display ?
		if not self.element_number : return

		# Use the shader program
		glUseProgram( self.shader_program_id )

		# Initialise Model-View transformation matrix
		modelview_matrix = identity( 4, dtype=float32 )

		# Position the scene
		modelview_matrix = TranslateMatrix( modelview_matrix, [ 0.0, 0.0, -3.0 ] )

		# Apply trackball transformation to the model matrix
		modelview_matrix = dot( modelview_matrix, self.trackball_transform )

		# Set the normal matrix
		normal_matrix = array( self.trackball_transform[ :3, :3 ], dtype=float32 )

		# Send the transformation matrices to the shader
		glUniformMatrix3fv( glGetUniformLocation( self.shader_program_id, "Normal_Matrix" ), 1, GL_TRUE, normal_matrix )
		glUniformMatrix4fv( glGetUniformLocation( self.shader_program_id, "MVP_Matrix" ), 1, GL_TRUE,
			dot( self.projection_matrix, modelview_matrix ) )

		# Activate color in the shader if necessary
		if self.color_buffer_id != -1 :
			glUniform1i( glGetUniformLocation( self.shader_program_id, "color_enabled" ), 1 )

		# Vertex array object
		glBindVertexArray( self.vertex_array_id )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, self.face_buffer_id )

		# Draw the mesh
		glDrawElements( GL_TRIANGLES, self.element_number, GL_UNSIGNED_INT, None )

		# Release the vertex array object
		glBindVertexArray( 0 )

		# Release the shader program
		glUseProgram( 0 )


	#-
	#
	# Resize
	#
	#-
	#
	def Resize( self, width, height ) :

		# Compute perspective projection matrix
		self.projection_matrix = PerspectiveMatrix( 45.0, float(width)/float(height), 0.1, 100.0 )


	#-
	#
	# Close
	#
	#-
	#
	def Close( self ) :

		# Need to initialise ?
		if not self.element_number : return

		# Delete shader program
		glUseProgram( 0 )
		glDeleteProgram( self.shader_program_id )

		# Delete buffer objects
		glDeleteBuffers( 1, array([ self.face_buffer_id ]) )
		glDeleteBuffers( 1, array([ self.vertex_buffer_id ]) )
		glDeleteBuffers( 1, array([ self.normal_buffer_id ]) )
		if self.color_buffer_id != -1 :
			glDeleteBuffers( 1, array([ self.color_buffer_id ]) )

		# Delete vertex array
		glDeleteVertexArrays( 1, array([self.vertex_array_id]) )

		# Initialise the OpenGL buffer IDs
		self.shader_program_id = -1
		self.vertex_array_id = -1
		self.vertex_buffer_id = -1
		self.face_buffer_id = -1
		self.normal_buffer_id = -1
		self.color_buffer_id = -1

		# Initialise the model element number
		self.element_number = 0

		# Initialise the trackball transformation matrix
		self.trackball_transform = identity( 4, dtype=float32 )



