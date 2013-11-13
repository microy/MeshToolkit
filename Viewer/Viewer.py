# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                  Viewer.py
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
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLUT import *
from Core.Mesh import *
from Frame import *
from Shader import *
from Transformation import *
import math
import numpy



#--
#
# Viewer
#
#--
#
# Display a mesh with OpenGL
#
class Viewer( Frame ) :


	#
	# Initialisation
	#
	def __init__( self, mesh=None, title="Untitled Window", width=1024, height=768 ) :
		# Initialise base class
		Frame.__init__( self, title=title, width=width, height=height )
		# Initialise member variables
		self.mesh = None
		self.shader_program_id = 0
		self.vertex_array_id = 0
		self.vertex_buffer_id = 0
		self.face_buffer_id = 0
		self.normal_buffer_id = 0
		self.color_buffer_id = 0
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
		# Release the bindings
		glBindBuffer( GL_ARRAY_BUFFER, 0 )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, 0 )
		glBindVertexArray( 0 )


	#
	# Display
	#
	def Display( self ) :
		# Clear all pixels and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		# Framerate counter
		self.frame_count += 1
		# Is there a mesh to display ?
		if self.mesh :
		        # Use the shader program
		        glUseProgram( self.shader_program_id )
			# Draw the mesh
			glBindVertexArray( self.vertex_array_id )
			glDrawElements( GL_TRIANGLES, len(self.mesh.faces), GL_UNSIGNED_INT, 0 )
			# Release the bindings
			glBindVertexArray( 0 )
			glUseProgram( 0 )
		# Swap buffers
		glutSwapBuffers()
		glutPostRedisplay()


	#
	# Close
	#
	def Close( self ) :
		# Delete shader program
		glUseProgram( 0 )
		glDeleteProgram( self.shader_program_id )
		# Delete buffer objects
		glDeleteBuffers( 1, numpy.array([ self.face_buffer_id ]) )
		glDeleteBuffers( 1, numpy.array([ self.vertex_buffer_id ]) )
		glDeleteBuffers( 1, numpy.array([ self.normal_buffer_id ]) )
		glDeleteBuffers( 1, numpy.array([ self.color_buffer_id ]) )
		# Delete vertex array
		glDeleteVertexArrays( 1, numpy.array([ self.vertex_array_id ]) )

