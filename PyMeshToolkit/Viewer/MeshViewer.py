# -*- coding:utf-8 -*- 


#
# Display a mesh with OpenGL 3 core profile
#


#
# External dependencies
#
import math
import numpy as np
import OpenGL.GL as gl
import PyMeshToolkit
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
		gl.glClearColor( 1, 1, 1, 1 )

		# Enable depth test
		gl.glEnable( gl.GL_DEPTH_TEST )

		# Enable face culling
		gl.glEnable( gl.GL_CULL_FACE )

		# Enable blending function
		gl.glEnable( gl.GL_BLEND )
		gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )

		# Enable multisampling (antialiasing)
		gl.glEnable( gl.GL_MULTISAMPLE )

		# Initialise the projection transformation matrix
		self.SetProjectionMatrix( width, height )

		# Load the shaders
		self.smooth_shader = PyMeshToolkit.Viewer.Shader( 'Smooth' )
		self.flat_shader = PyMeshToolkit.Viewer.Shader( 'Flat' )
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
		if mesh.vertex_normal_number != mesh.vertex_number : mesh.UpdateNormals()

		# Cast input data (required for OpenGL)
		vertices = np.array( mesh.vertices, dtype=np.float32 )
		faces = np.array( mesh.faces, dtype=np.uint32 )
		normals = np.array( mesh.vertex_normals, dtype=np.float32 )
		colors = np.array( mesh.colors, dtype=np.float32 )

		# Normalize the model
		(center, radius) = mesh.GetBoundingSphere()
		vertices -= center
		vertices *= 10.0 / radius

		# Vertex array object
		self.vertex_array_id = gl.glGenVertexArrays( 1 )
		gl.glBindVertexArray( self.vertex_array_id )

		# Face buffer object
		self.face_buffer_id = gl.glGenBuffers( 1 )
		gl.glBindBuffer( gl.GL_ELEMENT_ARRAY_BUFFER, self.face_buffer_id )
		gl.glBufferData( gl.GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, gl.GL_STATIC_DRAW )

		# Vertex buffer object
		self.vertex_buffer_id = gl.glGenBuffers( 1 )
		gl.glBindBuffer( gl.GL_ARRAY_BUFFER, self.vertex_buffer_id )
		gl.glBufferData( gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW )
		gl.glEnableVertexAttribArray( 0 )
		gl.glVertexAttribPointer( 0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None )

		# Normal buffer object
		self.normal_buffer_id = gl.glGenBuffers( 1 )
		gl.glBindBuffer( gl.GL_ARRAY_BUFFER, self.normal_buffer_id )
		gl.glBufferData( gl.GL_ARRAY_BUFFER, normals.nbytes, normals, gl.GL_STATIC_DRAW )
		gl.glEnableVertexAttribArray( 1 )
		gl.glVertexAttribPointer( 1, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None )

		# Color buffer object
		if len( colors ) : 
			self.color_enabled = True
			self.color_buffer_id = gl.glGenBuffers( 1 )
			gl.glBindBuffer( gl.GL_ARRAY_BUFFER, self.color_buffer_id )
			gl.glBufferData( gl.GL_ARRAY_BUFFER, colors.nbytes, colors, gl.GL_STATIC_DRAW )
			gl.glEnableVertexAttribArray( 2 )
			gl.glVertexAttribPointer( 2, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None )

		# Release the buffers
		gl.glBindBuffer( gl.GL_ARRAY_BUFFER, 0 )
		gl.glBindBuffer( gl.GL_ELEMENT_ARRAY_BUFFER, 0 )
		gl.glBindVertexArray( 0 )

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
		gl.glDeleteBuffers( 1, np.array([ self.face_buffer_id ]) )
		gl.glDeleteBuffers( 1, np.array([ self.vertex_buffer_id ]) )
		gl.glDeleteBuffers( 1, np.array([ self.normal_buffer_id ]) )
		if self.color_enabled :	gl.glDeleteBuffers( 1, np.array([ self.color_buffer_id ]) )

		# Delete vertex array
		gl.glDeleteVertexArrays( 1, np.array([self.vertex_array_id]) )

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
		if enabled : gl.glEnable( gl.GL_MULTISAMPLE )
		else : gl.glDisable( gl.GL_MULTISAMPLE )

	#
	# Display
	#
	def Display( self ) :

		# Clear all pixels and depth buffer
		gl.glClear( gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT )

		# Nothing to display
		if not self.element_number : return

		# Display the mesh with solid rendering
		if self.wireframe_mode == 0 :

			# Display the mesh
			self.DisplayMesh()

		# Display the mesh with wireframe rendering
		elif self.wireframe_mode == 1 :

			# 1st pass : wireframe model
			gl.glPolygonMode( gl.GL_FRONT_AND_BACK, gl.GL_LINE )
			self.DisplayMesh( self.wireframe_mode )

			# 2nd pass : solid model
			gl.glPolygonMode( gl.GL_FRONT_AND_BACK, gl.GL_FILL )
			gl.glEnable( gl.GL_POLYGON_OFFSET_FILL )
			gl.glPolygonOffset( 1.0, 1.0 )
			self.DisplayMesh()
			gl.glDisable( gl.GL_POLYGON_OFFSET_FILL )

		# Display the mesh with hidden line removal rendering
		elif self.wireframe_mode == 2 :

			# 1st pass : wireframe model
			gl.glPolygonMode( gl.GL_FRONT_AND_BACK, gl.GL_LINE )
			self.DisplayMesh()

			# 2nd pass : hidden line removal
			gl.glPolygonMode( gl.GL_FRONT_AND_BACK, gl.GL_FILL )
			gl.glEnable( gl.GL_POLYGON_OFFSET_FILL )
			gl.glPolygonOffset( 1.0, 1.0 )
			self.DisplayMesh( self.wireframe_mode )
			gl.glDisable( gl.GL_POLYGON_OFFSET_FILL )

	#
	# DisplayMesh
	#
	def DisplayMesh( self, wireframe_mode = 0 ) :

		# Use the shader program
		gl.glUseProgram( self.shader_program.program_id )

		# Initialise Model-View transformation matrix
		modelview_matrix = np.identity( 4, dtype=np.float32 )

		# Position the scene (camera)
		modelview_matrix[3,2] = -30.0

		# Apply trackball transformation
		modelview_matrix = np.dot( self.transformation, modelview_matrix )

		# Send the transformation matrices to the shader
		gl.glUniformMatrix3fv( gl.glGetUniformLocation( self.shader_program.program_id, "Normal_Matrix" ),
			1, gl.GL_FALSE, np.array( self.transformation[ :3, :3 ] ) )
		gl.glUniformMatrix4fv( gl.glGetUniformLocation( self.shader_program.program_id, "MVP_Matrix" ),
			1, gl.GL_FALSE, np.dot( modelview_matrix, self.projection_matrix ) )

		# Activate color in the shader if necessary
		gl.glUniform1i( gl.glGetUniformLocation( self.shader_program.program_id, "color_enabled" ), self.color_enabled )
		
		# Activate hidden lines in the shader for wireframe rendering
		gl.glUniform1i( gl.glGetUniformLocation( self.shader_program.program_id, "wireframe_mode" ), wireframe_mode )
		
		# Vertex array object
		gl.glBindVertexArray( self.vertex_array_id )
		gl.glBindBuffer( gl.GL_ELEMENT_ARRAY_BUFFER, self.face_buffer_id )

		# Draw the mesh
		gl.glDrawElements( gl.GL_TRIANGLES, self.element_number, gl.GL_UNSIGNED_INT, None )

		# Release the vertex array object
		gl.glBindVertexArray( 0 )

		# Release the shader program
		gl.glUseProgram( 0 )

	#
	# Resize
	#
	def Resize( self, width, height ) :

		# Resize the viewport
		gl.glViewport( 0, 0, width, height )

		# Resize the trackball
		Trackball.Resize( self, width, height )

		# Compute perspective projection matrix
		self.SetProjectionMatrix( width, height )

	#
	# SetProjectionMatrix
	#
	def SetProjectionMatrix( self, width, height ) :

		fovy, aspect, near, far = 45.0, float(width)/height, 0.1, 100.0
		f = math.tan( math.pi * fovy / 360.0 )
		# Compute the perspective matrix
		self.projection_matrix = np.identity( 4, dtype=np.float32 )
		self.projection_matrix[0,0] = 1.0 / (f * aspect)
		self.projection_matrix[1,1] = 1.0 / f
		self.projection_matrix[2,2] = - (far + near) / (far - near)
		self.projection_matrix[2,3] = - 1.0
		self.projection_matrix[3,2] = - 2.0 * near * far / (far - near)
