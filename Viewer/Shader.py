# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 Shader.py
#                             -------------------
#    update               : 2013-11-14
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


#--
#
#  LoadShaders
#
#--
#
# Load OpenGL vertex and fragment shaders
#
def LoadShaders( name='Simple' ) :

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
	return program_id



