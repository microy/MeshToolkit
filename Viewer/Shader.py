# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Shader.py
#                             -------------------
#    update               : 2013-11-18
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
#  LoadShaders
#
#-
#
def LoadShaders( name='Simple' ) :

	# Initialisation
	vertex_shader_source = ''
	fragment_shader_source = ''
	geometry_shader_source = ''

	if name == 'NormalView' :
		geometry_shader_enabled = True
	else :
		geometry_shader_enabled = False

	# Load shader source files
	with open('Viewer/Shader-'+name+'.vert.glsl', 'r') as vertex_shader_file :
		vertex_shader_source = vertex_shader_file.read()
	with open('Viewer/Shader-'+name+'.frag.glsl', 'r') as fragment_shader_file :
		fragment_shader_source = fragment_shader_file.read()
	if geometry_shader_enabled :
		with open('Viewer/Shader-'+name+'.geom.glsl', 'r') as geometry_shader_file :
			geometry_shader_source = geometry_shader_file.read()

	# Create the shaders
	vertex_shader = glCreateShader( GL_VERTEX_SHADER )
	fragment_shader = glCreateShader( GL_FRAGMENT_SHADER )
	if geometry_shader_enabled :
		geometry_shader = glCreateShader( GL_GEOMETRY_SHADER )

	# Load shader source codes
	glShaderSource( vertex_shader, vertex_shader_source )
	glShaderSource( fragment_shader, fragment_shader_source )
	if geometry_shader_enabled :
		glShaderSource( geometry_shader, geometry_shader_source )

	# Compile the shaders
	glCompileShader( vertex_shader )
	glCompileShader( fragment_shader )
	if geometry_shader_enabled :
		glCompileShader( geometry_shader )

	# Check the shaders
	if not glGetShaderiv( vertex_shader, GL_COMPILE_STATUS ) :
		raise RuntimeError( 'Vertex shader compilation failed.\n' + glGetShaderInfoLog( vertex_shader ) )
	if not glGetShaderiv( fragment_shader, GL_COMPILE_STATUS ) :
		raise RuntimeError( 'Fragment shader compilation failed.\n' + glGetShaderInfoLog( fragment_shader ) )
	if geometry_shader_enabled :
		if not glGetShaderiv( geometry_shader, GL_COMPILE_STATUS ) :
			raise RuntimeError( 'Geometry shader compilation failed.\n' + glGetShaderInfoLog( geometry_shader ) )

	# Create the program
	program_id = glCreateProgram()

	# Attach the shaders to the program
	glAttachShader( program_id, vertex_shader )
	glAttachShader( program_id, fragment_shader )
	if geometry_shader_enabled :
		glAttachShader( program_id, geometry_shader )

	# Link the program
	glLinkProgram( program_id )

	# Check the program
	if not glGetProgramiv( program_id, GL_LINK_STATUS ) :
		raise RuntimeError( 'Shader program linking failed.\n' + glGetProgramInfoLog( program_id ) )

	# Detach the shaders from the program
	glDetachShader( program_id, vertex_shader )
	glDetachShader( program_id, fragment_shader )
	if geometry_shader_enabled :
		glDetachShader( program_id, geometry_shader )

	# Delete the shaders
	glDeleteShader( vertex_shader )
	glDeleteShader( fragment_shader )
	if geometry_shader_enabled :
		glDeleteShader( geometry_shader )

	# Return shader program ID
	return program_id


