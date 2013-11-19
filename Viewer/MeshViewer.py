# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                MeshViewer.py
#                             -------------------
#    update               : 2013-11-19
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

from numpy import *

from Core.Mesh import *
from Core.BoundingContainer import *
from Shader import *
from Transformation import *




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

		# Initialise member variables
		self.element_number = 0
		self.shader_program_id = -1
		self.vertex_array_id = -1
		self.vertex_buffer_id = -1
		self.face_buffer_id = -1
		self.normal_buffer_id = -1
		self.color_buffer_id = -1
		self.projection_matrix = identity( 4, dtype=float32 )
		self.view_matrix = identity( 4, dtype=float32 )
		self.model_matrix = identity( 4, dtype=float32 )
		self.model_scale_factor = 1.0
		self.model_center = array( [0, 0, 0], dtype=float32 )
		self.model_translation = array( [0, 0, 0], dtype=float32 )
		self.trackball_transform = identity( 4, dtype=float32 )

		# Initialise the view matrix
		self.view_matrix = LookAtMatrix( [0, 0, 30], [0, 0, 0], [0, 1, 0] )

		# Initialise the projection matrix
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

		# Compute mesh normals
		if len(mesh.vertex_normals) != len(mesh.vertices) :
			UpdateNormals( mesh )

		# Cast input data (required for OpenGL)
		vertices = array( mesh.vertices, dtype=float32 )
		faces = array( mesh.faces, dtype=uint32 )
		normals = array( mesh.vertex_normals, dtype=float32 )
		colors = array( mesh.colors, dtype=float32 )

		# Load the shader
#		if len(mesh.colors) == len(mesh.vertices) :
#			self.shader_program_id = LoadShaders( 'NormalColor' )
#		else :
#			self.shader_program_id = LoadShaders( 'Normal' )
		self.shader_program_id = LoadShader( 'Test' )

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
		if len(mesh.colors) == len(mesh.vertices) :
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

		# Compute initial model transformations
		(center, radius) = GetBoundingSphere( mesh )
		self.model_scale_factor = 10.0 / radius
		self.model_center = array( center, dtype=float32 )
		self.trackball_transform = identity( 4, dtype=float32 )

		# Enable display
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

		# Compute model transformation matrix
		self.model_matrix = identity( 4, dtype=float32 )
		self.model_matrix = TranslateMatrix( self.model_matrix, self.model_translation )
		self.model_matrix = TranslateMatrix( self.model_matrix, -self.model_center )
		self.model_matrix = ScaleMatrix( self.model_matrix, self.model_scale_factor )

		viewmatrix = dot( self.view_matrix, self.trackball_transform )

		# Send the transformation matrices to the shader
		glUniformMatrix4fv( glGetUniformLocation( self.shader_program_id, "View_Matrix" ), 1, GL_TRUE, viewmatrix )
		glUniformMatrix4fv( glGetUniformLocation( self.shader_program_id, "Model_Matrix" ), 1, GL_TRUE, self.model_matrix )
		glUniformMatrix3fv( glGetUniformLocation( self.shader_program_id, "Normal_Matrix" ), 1, GL_TRUE, NormalMatrix( viewmatrix ) )
		glUniform3f( glGetUniformLocation( self.shader_program_id, "LightPosition" ), 0.0, 0.0, 30.0 )
		glUniformMatrix4fv( glGetUniformLocation( self.shader_program_id, "MVP_Matrix" ), 1, GL_TRUE,
			dot( self.projection_matrix, dot( viewmatrix, self.model_matrix ) ) )

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
	# SetPerspectiveMatrix
	#
	#-
	#
	def SetPerspectiveMatrix( self, width, height ) :

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

		# Disable display
		self.element_number = 0

		# Delete shader program
		glUseProgram( 0 )
		glDeleteProgram( self.shader_program_id )

		# Delete buffer objects
		glDeleteBuffers( 1, array([ self.face_buffer_id ]) )
		glDeleteBuffers( 1, array([ self.vertex_buffer_id ]) )
		if self.normal_buffer_id != -1 :
			glDeleteBuffers( 1, array([ self.normal_buffer_id ]) )
		if self.color_buffer_id != -1 :
			glDeleteBuffers( 1, array([ self.color_buffer_id ]) )

		# Delete vertex array
		glDeleteVertexArrays( 1, array([self.vertex_array_id]) )

		# Initialise member variables
		self.shader_program_id = -1
		self.vertex_array_id = -1
		self.vertex_buffer_id = -1
		self.face_buffer_id = -1
		self.normal_buffer_id = -1
		self.color_buffer_id = -1
		self.model_scale_factor = 1.0
		self.model_center = array( [0, 0, 0], dtype=float32 )
		self.model_translation = array( [0, 0, 0], dtype=float32 )
		self.trackball_transform = identity( 4, dtype=float32 )



