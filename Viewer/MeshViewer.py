# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                MeshViewer.py
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

from numpy import array

from Core.Mesh import *





#--
#
# MeshViewer
#
#--
#
# Display a mesh with OpenGL
#
class MeshViewer() :


	#
	# Initialisation
	#
	def __init__( self, mesh=None ) :

		# Initialise member variables
		self.mesh = None
		self.shader_program_id = -1
		self.vertex_array_id = -1
		self.vertex_buffer_id = -1
		self.face_buffer_id = -1
		self.normal_buffer_id = -1
		self.color_buffer_id = -1

		# Load mesh
		if mesh : self.LoadMesh( mesh )



	#
	#  LoadShaders
	#
	def LoadShaders( self, name='Simple' ) :

		# Initialisation
		vertex_shader_source = ''
		fragment_shader_source = ''

		# Load shader source files
		with open('Viewer/Shader-'+name+'.vert.glsl', 'r') as f : vertex_shader_source = f.read()
		with open('Viewer/Shader-'+name+'.frag.glsl', 'r') as f : fragment_shader_source = f.read()

		# Create the shaders
		vertex_shader = glCreateShader( GL_VERTEX_SHADER )
		fragment_shader = glCreateShader( GL_FRAGMENT_SHADER )

		# Load shader source codes
		glShaderSource( vertex_shader, vertex_shader_source )
		glShaderSource( fragment_shader, fragment_shader_source )

		# Compile the shaders
		glCompileShader( vertex_shader )
		glCompileShader( fragment_shader )

		# Check the shaders
		if not glGetShaderiv( vertex_shader, GL_COMPILE_STATUS ) :
			raise RuntimeError( 'Vertex shader compilation failed.\n' + glGetShaderInfoLog( vertex_shader ) )
		if not glGetShaderiv( fragment_shader, GL_COMPILE_STATUS ) :
			raise RuntimeError( 'Fragment shader compilation failed.\n' + glGetShaderInfoLog( fragment_shader ) )

		# Create the program
		program_id = glCreateProgram()

		# Attach the shaders to the program
		glAttachShader( program_id, vertex_shader )
		glAttachShader( program_id, fragment_shader )

		# Link the program
		glLinkProgram( program_id )

		# Check the program
		if not glGetProgramiv( program_id, GL_LINK_STATUS ) :
			raise RuntimeError( 'Shader program linking failed.\n' + glGetProgramInfoLog( program_id ) )

		# Use the shader program
		glUseProgram( program_id )

		# Delete the shaders
		glDeleteShader( vertex_shader )
		glDeleteShader( fragment_shader )

		# Return shader program ID
		self.shader_program_id = program_id





	#
	# LoadMesh
	#
	def LoadMesh( self, mesh ) :

		# Initialisation
		self.mesh = mesh

		# Load the shader
		self.LoadShaders( 'Color' )

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

		# Color buffer object
		if len(self.mesh.colors) :
			# Color buffer object
			self.color_buffer_id = glGenBuffers( 1 )
			glBindBuffer( GL_ARRAY_BUFFER, self.color_buffer_id )
			glBufferData( GL_ARRAY_BUFFER, mesh.colors.nbytes, mesh.colors, GL_STATIC_DRAW )
			glEnableVertexAttribArray( 1 )
			glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 0, None )


		# Normal buffer object
#		self.normal_buffer_id = glGenBuffers( 1 )
#		glBindBuffer( GL_ARRAY_BUFFER, self.normal_buffer_id )
#		glBufferData( GL_ARRAY_BUFFER, len(mesh.vertex_normals)*4, mesh.vertex_normals, GL_STATIC_DRAW )
#		glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 0, None )
#		glEnableVertexAttribArray( 1 )

		if glGetError() != GL_NO_ERROR :
			raise RuntimeError('OpenGL error while loading the mesh.' )



	#
	# Display
	#
	def Display( self ) :

		# Is there a mesh to display ?
		if not self.mesh : return

		# Draw the mesh
		glDrawElements( GL_TRIANGLES, len(self.mesh.vertices), GL_UNSIGNED_INT, None )


	#
	# Close
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
#		glDeleteBuffers( 1, numpy.array([ self.normal_buffer_id ]) )
		if len(self.mesh.colors) :
			glDeleteBuffers( 1, array([ self.color_buffer_id ]) )

		# Delete vertex array
		glDeleteVertexArrays( 1, array([self.vertex_array_id]) )

		# Initialise member variables
		self.mesh = None
		self.shader_program_id = -1
		self.vertex_array_id = -1
		self.vertex_buffer_id = -1
		self.face_buffer_id = -1
		self.normal_buffer_id = -1
		self.color_buffer_id = -1

