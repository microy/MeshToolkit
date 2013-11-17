# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                MeshViewer.py
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
	def __init__( self, mesh=None, shader='Color', width=1024, height=768 ) :

		# Initialise member variables
		self.mesh = None
		self.shader_program_id = -1
		self.vertex_array_id = -1
		self.vertex_buffer_id = -1
		self.face_buffer_id = -1
		self.normal_buffer_id = -1
		self.color_buffer_id = -1
		self.projection_matrix = identity( 4, dtype=float32 )
		self.view_matrix = identity( 4, dtype=float32 )
		self.model_matrix = identity( 4, dtype=float32 )
		self.mvp_matrix = identity( 4, dtype=float32 )
		self.model_scale_factor = 1.0
		self.model_center = array( [0, 0, 0], dtype=float32 )
		self.model_translation = array( [0, 0, 0], dtype=float32 )
		self.trackball_transform = identity( 4, dtype=float32 )

		# Load mesh
		if mesh : self.LoadMesh( mesh, shader )

		# Initialise the view matrix
		self.view_matrix = LookAtMatrix( [0, 0, 20], [0, 0, 0], [0, 1, 0] )

		# Initialise the projection matrix
		self.projection_matrix = PerspectiveMatrix( 45.0, float(width)/float(height), 0.1, 100.0 )




	#-
	#
	# LoadMesh
	#
	#-
	#
	def LoadMesh( self, mesh, shader='Color' ) :

		# Initialisation
		self.mesh = mesh

		# Load the shader
		self.shader_program_id = LoadShaders( shader )

		# Use the shader program
		glUseProgram( self.shader_program_id )

		# Vertex array object
		self.vertex_array_id = glGenVertexArrays( 1 )
		glBindVertexArray( self.vertex_array_id )

		# Face buffer object
		self.face_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, self.face_buffer_id )
		glBufferData( GL_ELEMENT_ARRAY_BUFFER, mesh.faces.nbytes, mesh.faces, GL_STATIC_DRAW )

		# Vertex buffer object
		self.vertex_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.vertex_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, mesh.vertices.nbytes, mesh.vertices, GL_STATIC_DRAW )
		glEnableVertexAttribArray( 0 )
		glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Normal buffer object
		self.normal_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.normal_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, mesh.vertex_normals.nbytes, mesh.vertex_normals, GL_STATIC_DRAW )
		glEnableVertexAttribArray( 1 )
		glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Color buffer object
		if len(self.mesh.colors) :
			self.color_buffer_id = glGenBuffers( 1 )
			glBindBuffer( GL_ARRAY_BUFFER, self.color_buffer_id )
			glBufferData( GL_ARRAY_BUFFER, mesh.colors.nbytes, mesh.colors, GL_STATIC_DRAW )
			glEnableVertexAttribArray( 2 )
			glVertexAttribPointer( 2, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Release the buffers
		glBindBuffer( GL_ARRAY_BUFFER, 0 )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, 0 )
		glBindVertexArray( 0 )

		# Release the shader program
		glUseProgram( 0 )

		# OpenGL error checking
		if glGetError() != GL_NO_ERROR :
			raise RuntimeError('OpenGL error while loading the mesh.' )

		# Compute initial model transformations
		(center, radius) = GetBoundingSphere( mesh )
		self.model_scale_factor = 10.0 / radius
		self.model_center = array( center, dtype=float32 )

		

	#-
	#
	# Display
	#
	#-
	#
	def Display( self ) :

		# Is there a mesh to display ?
		if not self.mesh : return

		# Use the shader program
		glUseProgram( self.shader_program_id )

		# Compute model transformation matrix
		self.model_matrix = identity( 4, dtype=float32 )
		self.model_matrix = TranslateMatrix( self.model_matrix, self.model_translation )
		self.model_matrix = dot( self.model_matrix, self.trackball_transform )
		self.model_matrix = TranslateMatrix( self.model_matrix, -self.model_center )
		self.model_matrix = ScaleMatrix( self.model_matrix, self.model_scale_factor )

		# Compute Model-View-Projection matrix
		self.mvp_matrix = dot( self.projection_matrix, dot( self.view_matrix, self.model_matrix ) )

		# Send the transformation matrices to the shader
#		glUniformMatrix4fv( glGetUniformLocation( self.shader_program_id, "View_Matrix" ), 1, GL_TRUE, self.view_matrix )
#		glUniformMatrix4fv( glGetUniformLocation( self.shader_program_id, "Model_Matrix" ), 1, GL_TRUE, self.model_matrix )
#		glUniform3f( glGetUniformLocation( self.shader_program_id, "LightPosition_worldspace" ), 4.0, 4.0, 4.0 )
		glUniformMatrix4fv( glGetUniformLocation( self.shader_program_id, "MVP_Matrix" ), 1, GL_TRUE, self.mvp_matrix )

		# Vertex array object
		glBindVertexArray( self.vertex_array_id )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, self.face_buffer_id )

		# Draw the mesh
		glDrawElements( GL_TRIANGLES, len(self.mesh.faces)*3, GL_UNSIGNED_INT, None )

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
		if not self.mesh : return

		# Delete shader program
		glUseProgram( 0 )
		glDeleteProgram( self.shader_program_id )

		# Delete buffer objects
		glDeleteBuffers( 1, array([ self.face_buffer_id ]) )
		glDeleteBuffers( 1, array([ self.vertex_buffer_id ]) )
		glDeleteBuffers( 1, array([ self.normal_buffer_id ]) )
		if len(self.mesh.colors) :
			glDeleteBuffers( 1, array([ self.color_buffer_id ]) )

		# Delete vertex array
		glDeleteVertexArrays( 1, array([self.vertex_array_id]) )

		# OpenGL error checking
		if glGetError() != GL_NO_ERROR :
			raise RuntimeError('OpenGL error while closing the mesh.' )

		# Initialise member variables
		self.mesh = None
		self.shader_program_id = -1
		self.vertex_array_id = -1
		self.vertex_buffer_id = -1
		self.face_buffer_id = -1
		self.normal_buffer_id = -1
		self.color_buffer_id = -1
		self.projection_matrix = identity( 4, dtype=float32 )
		self.view_matrix = identity( 4, dtype=float32 )
		self.model_matrix = identity( 4, dtype=float32 )
		self.mvp_matrix = identity( 4, dtype=float32 )
		self.model_scale_factor = 1.0
		self.model_center = array( [0, 0, 0], dtype=float32 )
		self.model_translation = array( [0, 0, 0], dtype=float32 )
		self.trackball_transform = identity( 4, dtype=float32 )



