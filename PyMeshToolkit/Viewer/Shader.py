# -*- coding:utf-8 -*- 


#
# OpenGL shaders
#


#
# External dependencies
#
import OpenGL
from OpenGL.GL import *


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
#  Load a shader
#
def LoadShader( name, geometry_enabled=False ) :
	
	# Shader program source code correspondance
	shader_vertex_name = { 'Flat' : flat_shader_vertex, 'Smooth' : smooth_shader_vertex }
	shader_fragment_name = { 'Flat' : flat_shader_fragment, 'Smooth' : smooth_shader_fragment }
	shader_geometry_name = {}

	# Create the shaders
	vertex_shader = CreateShader( shader_vertex_name[ name ], GL_VERTEX_SHADER )
	fragment_shader = CreateShader( shader_fragment_name[ name ], GL_FRAGMENT_SHADER )
	if geometry_enabled : geometry_shader = CreateShader( shader_geometry_name[ name ], GL_GEOMETRY_SHADER )

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
#  Create a shader from source code
#
def CreateShader( shader_source, shader_type ) :

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

