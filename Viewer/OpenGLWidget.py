# -*- coding:utf-8 -*- 


#
# External dependencies
#
import OpenGL
OpenGL.FORWARD_COMPATIBLE_ONLY = True
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
import PySide
from PySide import QtGui, QtCore, QtOpenGL
from PySide.QtOpenGL import QGLWidget, QGLFormat, QGL
from math import tan, pi
from numpy import array, identity, dot, float32, uint32, zeros
from Core.Color import Value2Color, Value2ColorAlternate
from .Trackball import Trackball


#
# Create an OpenGL frame with Qt
#
class OpenGLWidget( QGLWidget ) :


	#
	# Initialisation
	#
	def __init__( self, parent=None ) :
		
		# Initialise QGLWidget with multisampling enabled and OpenGL 3 core only
		QGLWidget.__init__( self, QGLFormat( QGL.SampleBuffers | QGL.NoDeprecatedFunctions ), parent )

		# Track mouse events
		self.setMouseTracking( True )

		# Initialise mouse position
		self.previous_mouse_position = [ 0, 0 ]

		# Initialise viewing parameters
		self.wireframe_mode = 0
		self.element_number = 0
		self.color_enabled = False
		self.colorbar_enabled = False


	#
	# initializeGL
	#
	def initializeGL( self ) :

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

		# Initialise the trackball
		self.trackball = Trackball( self.width(), self.height() )

		# Initialise the projection transformation matrix
		self.SetProjectionMatrix( self.width(), self.height() )

		# Load the shaders
		self.smooth_shader_id = LoadShader( 'SmoothShading' )
		self.flat_shader_id = LoadShader( 'FlatShading' )
		self.shader_program_id = self.smooth_shader_id

		# Color bar viewer initialisation
		self.InitColorBar()


	#
	# LoadMesh
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
		self.trackball.Reset()

		# Update the display
		self.update()


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

		# Update the display
		self.update()


	#
	# SetShader
	#
	def SetShader( self, shader ) :

		# Setup the shader program
		if shader == 'SmoothShading' : self.shader_program_id = self.smooth_shader_id
		elif shader == 'FlatShading' : self.shader_program_id = self.flat_shader_id

		# Update the display
		self.update()


	#
	# SetAntialiasing
	#
	def SetAntialiasing( self, enabled ) :

		# Enable / Disable antialiasing
		if enabled : glEnable( GL_MULTISAMPLE )
		else : glDisable( GL_MULTISAMPLE )

		# Update the display
		self.update()


	#
	# paintGL
	#
	def paintGL( self ) :

		# Clear all pixels and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

		# Nothing to display
		if not self.element_number :
			self.swapBuffers()
			return

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

		# Display the color bar
		if self.colorbar_enabled :

			# Resize the viewport
			glViewport( self.width()-50, self.height()/2-300, 50, 600 )

			# Use the shader program
			glUseProgram( self.colorbar_shader )

			# Vertex array object
			glBindVertexArray( self.colorbar_vertexarray )

			# Draw the mesh
			glDrawArrays( GL_TRIANGLE_STRIP, 0, 44 )

			# Release the vertex array object
			glBindVertexArray( 0 )

			# Release the shader program
			glUseProgram( 0 )

			# Restore the viewport
			glViewport( 0, 0, self.width(), self.height() )

		# Swap buffers
		self.swapBuffers()


	#
	# Display
	#
	def DisplayMesh( self, wireframe_mode = 0 ) :

		# Use the shader program
		glUseProgram( self.shader_program_id )

		# Initialise Model-View transformation matrix
		modelview_matrix = identity( 4, dtype=float32 )

		# Position the scene (camera)
		modelview_matrix[3,2] = -30.0

		# Apply trackball transformation
		modelview_matrix = dot( self.trackball.transformation, modelview_matrix )

		# Send the transformation matrices to the shader
		glUniformMatrix3fv( glGetUniformLocation( self.shader_program_id, "Normal_Matrix" ),
			1, GL_FALSE, array( self.trackball.transformation[ :3, :3 ] ) )
		glUniformMatrix4fv( glGetUniformLocation( self.shader_program_id, "MVP_Matrix" ),
			1, GL_FALSE, dot( modelview_matrix, self.projection_matrix ) )

		# Activate color in the shader if necessary
		glUniform1i( glGetUniformLocation( self.shader_program_id, "color_enabled" ), self.color_enabled )
		
		# Activate hidden lines in the shader for wireframe rendering
		glUniform1i( glGetUniformLocation( self.shader_program_id, "wireframe_mode" ), wireframe_mode )
		
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
	# resizeGL
	#
	def resizeGL( self, width, height ) :

		# Resize the viewport
		glViewport( 0, 0, width, height )

		# Resize the trackball
		self.trackball.Resize( width, height )

		# Compute perspective projection matrix
		self.SetProjectionMatrix( width, height )


	#
	# mousePressEvent
	#
	def mousePressEvent( self, mouseEvent ) :

		# Left button
		if int(mouseEvent.buttons()) & QtCore.Qt.LeftButton : button = 1

		# Right button
		elif int(mouseEvent.buttons()) & QtCore.Qt.RightButton : button = 2

		# Unmanaged
		else : return

		# Update the trackball
		self.trackball.MousePress( [ mouseEvent.x(), mouseEvent.y() ], button )


	#
	# mouseReleaseEvent
	#
	def mouseReleaseEvent( self, mouseEvent ) :

		# Update the trackball
		self.trackball.MouseRelease()


	#
	# mouseMoveEvent
	#
	def mouseMoveEvent( self, mouseEvent ) :

		# Update the trackball
		if self.trackball.Motion( [ mouseEvent.x(), mouseEvent.y() ] ) :

			# Refresh display
			self.update()


	#
	# wheelEvent
	#
	def wheelEvent( self, event ) :

		# Get the mouse wheel delta for normalisation
		delta = event.delta()

		# Update the trackball
		self.trackball.WheelEvent( delta and delta // abs(delta) )

		# Refresh display
		self.update()


	#
	# OpenGLInfo
	#
	def OpenGLInfo( self ) :

		# Return OpenGL driver informations
		gl_vendor = glGetString( GL_VENDOR ).decode('latin-1')
		gl_renderer = glGetString( GL_RENDERER ).decode('latin-1')
		gl_version = glGetString( GL_VERSION ).decode('latin-1')
		gl_shader = glGetString( GL_SHADING_LANGUAGE_VERSION ).decode('latin-1')
		return ( gl_vendor, gl_renderer, gl_version, gl_shader )


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
		
		
	#
	# Initialisation of a color bar
	#
	def InitColorBar( self ) :

		# Generate vertices and colors
		size = 22
		vertices = zeros( (size * 2, 3), dtype=float32 )
		colors = zeros( (size * 2, 3), dtype=float32 )
		for i in range( size ) :
			vertices[i*2]   = [ -0.5, i / (size - 1.0) - 0.5, 0 ]
			vertices[i*2+1] = [ 0.5, i / (size - 1.0) - 0.5, 0 ]
			colors[i*2] = Value2Color( i / (size - 1.0) )
			colors[i*2+1] = Value2Color( i / (size - 1.0) )

		# Load the shader
		self.colorbar_shader = LoadShader( 'SimpleColor' )

		# Use the shader program
		glUseProgram( self.colorbar_shader )

		# Vertex array object
		self.colorbar_vertexarray = glGenVertexArrays( 1 )
		glBindVertexArray( self.colorbar_vertexarray )

		# Vertex buffer object
		vertex_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, vertex_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW )
		glEnableVertexAttribArray( 0 )
		glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Color buffer object
		color_buffer_id = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, color_buffer_id )
		glBufferData( GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW )
		glEnableVertexAttribArray( 1 )
		glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 0, None )

		# Release the buffers
		glBindBuffer( GL_ARRAY_BUFFER, 0 )
		glBindVertexArray( 0 )

		# Release the shader program
		glUseProgram( 0 )


#
#  LoadShader
#
def LoadShader( name, geometry_enabled=False ) :

	# Create the shaders
	vertex_shader = CreateShader( 'Viewer/Shaders/'+name+'.vert.glsl', GL_VERTEX_SHADER )
	fragment_shader = CreateShader( 'Viewer/Shaders/'+name+'.frag.glsl', GL_FRAGMENT_SHADER )
	if geometry_enabled : geometry_shader = CreateShader( 'Viewer/Shaders/'+name+'.geom.glsl', GL_GEOMETRY_SHADER )

	# Create the program
	program_id = glCreateProgram()

	# Attach the shaders to the program
	glAttachShader( program_id, vertex_shader )
	glAttachShader( program_id, fragment_shader )
	if geometry_enabled : glAttachShader( program_id, geometry_shader )

	# Link the program
	glLinkProgram( program_id )

	# Check the program
	if not glGetProgramiv( program_id, GL_LINK_STATUS ) :
		raise RuntimeError( 'Shader program linking failed.\n' + glGetProgramInfoLog( program_id ) )

	# Detach the shaders from the program
	glDetachShader( program_id, vertex_shader )
	glDetachShader( program_id, fragment_shader )
	if geometry_enabled : glDetachShader( program_id, geometry_shader )

	# Delete the shaders
	glDeleteShader( vertex_shader )
	glDeleteShader( fragment_shader )
	if geometry_enabled : glDeleteShader( geometry_shader )

	# Return shader program ID
	return program_id


#
#  CreateShader
#
def CreateShader( filename, shader_type ) :

	# Load shader source files
	with open( filename, 'r') as shader_file :
		shader_source = shader_file.read()

	# Create the shaders
	shader_id = glCreateShader( shader_type )

	# Load shader source codes
	glShaderSource( shader_id, shader_source )

	# Compile the shaders
	glCompileShader( shader_id )

	# Check the shaders
	if not glGetShaderiv( shader_id, GL_COMPILE_STATUS ) :
		raise RuntimeError( 'Shader compilation failed.\n' + glGetShaderInfoLog( shader_id ) )

	# Return the shader ID
	return shader_id
