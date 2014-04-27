# -*- coding:utf-8 -*- 


#
# Import OBJ / SMF files
#


#
# External dependencies
#
from numpy import array
from PyMesh.Core.Mesh import Mesh


#
# Import a mesh from a OBJ / SMF file
#
def ReadObj( filename ) :
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
		
		# Empty line / Comment
		if line.isspace() or line.startswith( '#' ) : continue

		# Split values in the line
		values = line.split()

		# Vertex
		if values[0] == 'v' :
			vertices.append( map( float, values[1:4] ) )

		# Face (index starts at 1)
		elif values[0] == 'f' :
			faces.append( map( int, values[1:4] ) )

		# Normal
		elif values[0] in [ 'n', 'vn' ] :
			normals.append( map( float, values[1:4] ) )

		# Color
		elif values[0] == 'c' :
			colors.append( map( float, values[1:4] ) )

		# Texture
		elif values[0] in [ 'r', 'vt' ] :
			texcoords.append( map( float, values[1:3] ) )

		# Texture filename
		elif values[0] == 'text' :
			material = values[1]
		
	# Remap face indices
	faces = array(faces) - 1

	# Return the final mesh
	return Mesh( name=filename, vertices=vertices, faces=faces, colors=colors,
		vertex_normals=normals,	textures=texcoords, texture_name=material )

