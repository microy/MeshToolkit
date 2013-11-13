# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 Shader.py
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
from OpenGL.GL import *


#
# Vertex shader code
#
vertex_shader_source = '''
#version 330 core

layout (location = 0) in vec3 vPosition;
layout (location = 1) in vec3 vNormal;
layout (location = 2) in vec3 vColor;

out vec3  color;

void main()
{
	color = vColor;
	gl_Position = vec4( vPosition, 1.0 );
}
'''


#
# Fragment shader code
#
fragment_shader_source = '''
#version 330 core

in vec3 color;
out vec3 fColor;

void main()
{
	fColor = color;
}
'''



#--
#
#  LoadShaders
#
#--
#
# Load OpenGL vertex and fragment shaders
#
def LoadShaders() :
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
		raise RuntimeError( glGetShaderInfoLog( vertex_shader ) )
	if not glGetShaderiv( fragment_shader, GL_COMPILE_STATUS ) :
		raise RuntimeError( glGetShaderInfoLog( fragment_shader ) )
	# Create the program
	program_id = glCreateProgram()
	# Attach the shaders to the program
	glAttachShader( program_id, vertex_shader )
	glAttachShader( program_id, fragment_shader )
	# Link the program
	glLinkProgram( program_id )
	# Check the program
	if not glGetProgramiv( program_id, GL_LINK_STATUS ) :
		raise RuntimeError( glGetProgramInfoLog( program_id ) )
	# Delete the shaders
	glDeleteShader( vertex_shader )
	glDeleteShader( fragment_shader )
	# Return shader program ID
	return program_id



