# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Shader.py
#                             -------------------
#    update               : 2013-11-25
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


#--
#
# External dependencies
#
#--
#
import OpenGL
OpenGL.FORWARD_COMPATIBLE_ONLY = True
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *


#-
#
#  LoadShader
#
#-
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


#-
#
#  CreateShader
#
#-
#
def CreateShader( filename, shader_type ) :

	# Initialisation
	shader_source = ''

	# Load shader source files
	with open( filename, 'rb') as shader_file :
		shader_source = shader_file.read().decode('utf-8')

	# Create the shaders
	shader_id = glCreateShader( shader_type )

	# Load shader source codes
	glShaderSource_compat( shader_id, shader_source )

	# Compile the shaders
	glCompileShader( shader_id )

	# Check the shaders
	if not glGetShaderiv( shader_id, GL_COMPILE_STATUS ) :
		raise RuntimeError( 'Shader compilation failed.\n' + glGetShaderInfoLog( shader_id ) )

	# Return the shader ID
	return shader_id



