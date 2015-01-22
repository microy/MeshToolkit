# -*- coding:utf-8 -*- 


#
# Display a mesh with OpenGL 3 core profile
#


#
# External dependencies
#
import OpenGL
from OpenGL.GL import *
from math import tan, pi
from numpy import array, identity, dot, float32, uint32, zeros
from PyMeshToolkit.Viewer.Shader import LoadShader
from PyMeshToolkit.Viewer.Trackball import Trackball


#
# Display a mesh with OpenGL
#
class MeshViewer( Trackball ) :


	#
	# Initialisation of OpenGL
	#
	def Initialise( self, width, height ) :

		# Initialise the trackball
		Trackball.Initialise( self, width, height )

		# Default background color
		glClearColor( 1, 1, 1, 1 )

		# Enable depth test
		glEnable( GL_DEPTH_TEST )

		# Enable face culling
		glEnable( GL_CULL_FACE )

		# Enable blending function
		glEnable( GL_BLEND )
		glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

		# Enable multisampling (antialiasing)
		glEnable( GL_MULTISAMPLE )

		# Initialise the projection transformation matrix
		self.SetProjectionMatrix( width, height )

		# Load the shaders
		self.smooth_shader = LoadShader( 'Smooth' )
		self.flat_shader = LoadShader( 'Flat' )
		self.shader_program = self.smooth_shader

		# Initialise viewing parameters
		self.wireframe_mode = 0
		self.element_number = 0
		self.color_enabled = False
		

	#
	# Load the mesh to display
	#
	def LoadMesh( self, mesh ) :

		# Close previous mesh
		self.Close()

		# Compute mesh normals if necessary
		if len(mesh.vertex_normals) != len(mesh.vertices) :	mesh.UpdateNormals()

		# Cast input data (required for OpenGL)
		vertices = array( mesh.vertices, dtype=float32 )
		faces = array( mesh.faces, dtype=uint32 )
		normals = array( mesh.vertex_normals, dtype=float32 )
		colors = array( mesh.colors, dtype=float32 )

		# Normalize the model
		(center, radius) = mesh.GetBoundingSphere()
		vertices -= center
		vertices *= 10.0 / radius

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
		if len( colors ) : 
			self.color_enabled = True
			self.color_buffer_id = glGenBuffers( 1 )
			glBindBuffer( GL_ARRAY_BUFFER, self.color_buffer_id )
			glBufferData( GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW )
			glEnableVertexAttribArray( 2 )
			glVertexAttribPointer( 2, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Release the buffers
		glBindBuffer( GL_ARRAY_BUFFER, 0 )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, 0 )
		glBindVertexArray( 0 )

		# Setup model element number
		self.element_number = len(faces) * 3

		# Reset the trackball
		Trackball.Reset( self )


	#
	# Close
	#
	def Close( self ) :

		# Need to initialise ?
		if not self.element_number : return

		# Delete buffer objects
		glDeleteBuffers( 1, array([ self.face_buffer_id ]) )
		glDeleteBuffers( 1, array([ self.vertex_buffer_id ]) )
		glDeleteBuffers( 1, array([ self.normal_buffer_id ]) )
		if self.color_enabled :	glDeleteBuffers( 1, array([ self.color_buffer_id ]) )

		# Delete vertex array
		glDeleteVertexArrays( 1, array([self.vertex_array_id]) )

		# Initialise the model parameters
		self.element_number = 0
		self.color_enabled = False


	#
	# SetShader
	#
	def SetShader( self, shader ) :

		# Setup the shader program
		if shader == 'SmoothShading' : self.shader_program = self.smooth_shader
		elif shader == 'FlatShading' : self.shader_program = self.flat_shader


	#
	# SetAntialiasing
	#
	def SetAntialiasing( self, enabled ) :

		# Enable / Disable antialiasing
		if enabled : glEnable( GL_MULTISAMPLE )
		else : glDisable( GL_MULTISAMPLE )


	#
	# Display
	#
	def Display( self ) :

		# Clear all pixels and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

		# Nothing to display
		if not self.element_number : return

		# Display the mesh with solid rendering
		if self.wireframe_mode == 0 :

			# Display the mesh
			self.DisplayMesh()

		# Display the mesh with wireframe rendering
		elif self.wireframe_mode == 1 :

			# 1st pass : wireframe model
			glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
			self.DisplayMesh( self.wireframe_mode )

			# 2nd pass : solid model
			glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
			glEnable( GL_POLYGON_OFFSET_FILL )
			glPolygonOffset( 1.0, 1.0 )
			self.DisplayMesh()
			glDisable( GL_POLYGON_OFFSET_FILL )

		# Display the mesh with hidden line removal rendering
		elif self.wireframe_mode == 2 :

			# 1st pass : wireframe model
			glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
			self.DisplayMesh()

			# 2nd pass : hidden line removal
			glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
			glEnable( GL_POLYGON_OFFSET_FILL )
			glPolygonOffset( 1.0, 1.0 )
			self.DisplayMesh( self.wireframe_mode )
			glDisable( GL_POLYGON_OFFSET_FILL )


	#
	# DisplayMesh
	#
	def DisplayMesh( self, wireframe_mode = 0 ) :

		# Use the shader program
		glUseProgram( self.shader_program )

		# Initialise Model-View transformation matrix
		modelview_matrix = identity( 4, dtype=float32 )

		# Position the scene (camera)
		modelview_matrix[3,2] = -30.0

		# Apply trackball transformation
		modelview_matrix = dot( self.transformation, modelview_matrix )

		# Send the transformation matrices to the shader
		glUniformMatrix3fv( glGetUniformLocation( self.shader_program, "Normal_Matrix" ),
			1, GL_FALSE, array( self.transformation[ :3, :3 ] ) )
		glUniformMatrix4fv( glGetUniformLocation( self.shader_program, "MVP_Matrix" ),
			1, GL_FALSE, dot( modelview_matrix, self.projection_matrix ) )

		# Activate color in the shader if necessary
		glUniform1i( glGetUniformLocation( self.shader_program, "color_enabled" ), self.color_enabled )
		
		# Activate hidden lines in the shader for wireframe rendering
		glUniform1i( glGetUniformLocation( self.shader_program, "wireframe_mode" ), wireframe_mode )
		
		# Vertex array object
		glBindVertexArray( self.vertex_array_id )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, self.face_buffer_id )

		# Draw the mesh
		glDrawElements( GL_TRIANGLES, self.element_number, GL_UNSIGNED_INT, None )

		# Release the vertex array object
		glBindVertexArray( 0 )

		# Release the shader program
		glUseProgram( 0 )


	#
	# Resize
	#
	def Resize( self, width, height ) :

		# Resize the viewport
		glViewport( 0, 0, width, height )

		# Resize the trackball
		Trackball.Resize( self, width, height )

		# Compute perspective projection matrix
		self.SetProjectionMatrix( width, height )


	#
	# SetProjectionMatrix
	#
	def SetProjectionMatrix( self, width, height ) :

		fovy, aspect, near, far = 45.0, float(width)/height, 0.1, 100.0
		f = tan( pi * fovy / 360.0 )
		# Compute the perspective matrix
		self.projection_matrix = identity( 4, dtype=float32 )
		self.projection_matrix[0,0] = 1.0 / (f * aspect)
		self.projection_matrix[1,1] = 1.0 / f
		self.projection_matrix[2,2] = - (far + near) / (far - near)
		self.projection_matrix[2,3] = - 1.0
		self.projection_matrix[3,2] = - 2.0 * near * far / (far - near)
