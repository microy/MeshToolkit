# -*- coding:utf-8 -*- 


#
# External dependencies
#
from Mesh import Mesh
from numpy import array


#
# Import mesh from a OBJ file
#
def ReadObjFile( filename ) :
#
# TODO: Bindings !
#
	# Initialisation
	vertices = []
	faces = []
	normals = []
	colors = []
	texcoords = []
        material = ""
	# Read each line in the file
	for line in open( filename, "r" ) :
		# Empty line
		if line.isspace() : continue
		# Comment
		if line.startswith( '#' ) : continue
		# Split values in the line
		values = line.split()
		# Vertex
		if values[0] == 'v' :
			vertices.append( map( float, values[1:4] ) )
		# Face (index starts at 1)
		elif values[0] == 'f' :
			faces.append( [ x-1 for x in map( int, values[1:4] ) ] )
		# Normal
		elif values[0] == 'n' :
			normals.append( map( float, values[1:4] ) )
		# Color
		elif values[0] == 'c' :
			colors.append( map( float, values[1:4] ) )
		# Texture
		elif values[0] == 'r' :
			texcoords.append( map( float, values[1:3] ) )
		# Texture filename
		elif values[0] == 'text' :
			material = values[1]
	# Return the final mesh
	return Mesh( name=filename, vertices=array(vertices), faces=array(faces),
		vertex_normals=array(normals), colors=array(colors),
		textures=array(texcoords), texture_name=material )

