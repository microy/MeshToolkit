# -*- coding:utf-8 -*- 


#
# OpenGL shaders
#


#
# External dependencies
#
import OpenGL.GL as gl



#
# Class managing OpenGL shaders
#
class Shader( object ) :

	#
	# Initialisation
	#
	def __init__( self, name='Smooth', geometry_enabled=False ) :
		
		# Compile the shaders
		vertex_shader = self.CreateShader( self.vertex_shader_source[ name ], gl.GL_VERTEX_SHADER )
		fragment_shader = self.CreateShader( self.fragment_shader_source[ name ], gl.GL_FRAGMENT_SHADER )
		if geometry_enabled : geometry_shader = self.CreateShader( self.geometry_shader_source[ name ], gl.GL_GEOMETRY_SHADER )

		# Create the program
		self.program_id = gl.glCreateProgram()

		# Attach the shaders to the program
		gl.glAttachShader( self.program_id, vertex_shader )
		gl.glAttachShader( self.program_id, fragment_shader )
		if geometry_enabled : gl.glAttachShader( program_id, geometry_shader )

		# Link the program
		gl.glLinkProgram( self.program_id )

		# Check the program
		if not gl.glGetProgramiv( self.program_id, gl.GL_LINK_STATUS ) :
			raise RuntimeError( 'Shader program linking failed.\n' + gl.glGetProgramInfoLog( program_id ) )

		# Detach the shaders from the program
		gl.glDetachShader( self.program_id, vertex_shader )
		gl.glDetachShader( self.program_id, fragment_shader )
		if geometry_enabled : gl.glDetachShader( self.program_id, geometry_shader )

		# Delete the shaders
		gl.glDeleteShader( vertex_shader )
		gl.glDeleteShader( fragment_shader )
		if geometry_enabled : gl.glDeleteShader( geometry_shader )

	#
	#  Create a shader from source code
	#
	def CreateShader( self, shader_source, shader_type ) :

		# Create the shaders
		shader_id = gl.glCreateShader( shader_type )

		# Load shader source codes
		gl.glShaderSource( shader_id, shader_source )

		# Compile the shaders
		gl.glCompileShader( shader_id )

		# Check the shaders
		if not gl.glGetShaderiv( shader_id, gl.GL_COMPILE_STATUS ) :
			raise RuntimeError( 'Shader compilation failed.\n' + gl.glGetShaderInfoLog( shader_id ) )

		# Return the shader ID
		return shader_id

	#
	# Flat shading - Vertex shader
	#
	flat_shader_vertex = '''#version 330 core

	layout (location = 0) in vec4 Vertex;
	layout (location = 1) in vec3 Normal;
	layout (location = 2) in vec3 Color;

	uniform mat4 MVP_Matrix;
	uniform mat3 Normal_Matrix;
	uniform int color_enabled = 0;
	uniform int wireframe_mode = 0;

	flat out vec4 FragColor;

	void main( void ) {

		vec3 Norm = normalize( Normal_Matrix * Normal );
		vec3 LightDir = vec3( 0.0, 0.0, 1.0 );

		float Dot = max( 0.0, dot(Norm, LightDir) ); 

		if( wireframe_mode == 1 ) {
			FragColor.xyz = vec3( 0.7, 0.2, 0.2 );
		}	
		else if( wireframe_mode == 2 ) {
			FragColor.xyz = vec3( 1.0, 1.0, 1.0 );
		}	
		else if( color_enabled == 0 ) {
			FragColor.xyz = vec3( 0.7, 0.7, 0.7 ) * Dot;
		}
		else {
			FragColor.xyz = Color * Dot;
		}

		FragColor.a = 1.0;

		gl_Position = MVP_Matrix * Vertex;
	}'''


	#
	# Flat shading - Fragment shader
	#
	flat_shader_fragment = '''#version 330 core

	flat in vec4 FragColor;

	out vec4 Color;

	void main( void ) {

		Color = FragColor;

	}'''


	#
	# Smooth shading - Vertex shader
	#
	smooth_shader_vertex = '''#version 330 core

	layout (location = 0) in vec4 Vertex;
	layout (location = 1) in vec3 Normal;
	layout (location = 2) in vec3 Color;

	uniform mat4 MVP_Matrix;
	uniform mat3 Normal_Matrix;
	uniform int color_enabled = 0;
	uniform int wireframe_mode = 0;

	out vec4 FragColor;

	void main( void ) {

		vec3 Norm = normalize( Normal_Matrix * Normal );
		vec3 LightDir = vec3( 0.0, 0.0, 1.0 );

		float Dot = max( 0.0, dot(Norm, LightDir) ); 

		if( wireframe_mode == 1 ) {
			FragColor.xyz = vec3( 0.7, 0.2, 0.2 );
		}
		else if( wireframe_mode == 2 ) {
			FragColor.xyz = vec3( 1.0, 1.0, 1.0 );
		}
		else if( color_enabled == 0 ) {
			FragColor.xyz = vec3( 0.7, 0.7, 0.7 ) * Dot;
		}
		else {
			FragColor.xyz = Color * Dot;
		}

		FragColor.a = 1.0;

		gl_Position = MVP_Matrix * Vertex;
	}'''


	#
	# Smooth shading - Fragment shader
	#
	smooth_shader_fragment = '''#version 330 core

	in vec4 FragColor;

	out vec4 Color;

	void main( void ) {

		Color = FragColor;

	}'''

	#
	# Shader program source code correspondance
	#
	vertex_shader_source = { 'Flat' : flat_shader_vertex, 'Smooth' : smooth_shader_vertex }
	fragment_shader_source = { 'Flat' : flat_shader_fragment, 'Smooth' : smooth_shader_fragment }
	geometry_shader_source = {}

