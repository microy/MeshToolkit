# -*- coding:utf-8 -*-

#
# Import OBJ files
#

# External dependencies
import os
import numpy as np
import MeshToolkit as mtk

# Import a mesh from a OBJ / SMF file
def ReadObj( filename ) :
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
			vertices.append( list( map( float, values[1:4] ) ) )
		# Face (index starts at 1)
		elif values[0] == 'f' :
			faces.append( list( map( int, [ (v.split('/'))[0] for v in values[1:4] ] ) ) )
		# Normal
		elif values[0] == 'vn' :
			normals.append( list( map( float, values[1:4] ) ) )
		# Color
		elif values[0] == 'c' :
			colors.append( list( map( float, values[1:4] ) ) )
		# Texture
		elif values[0] == 'vt' :
			texcoords.append( list( map( float, values[1:3] ) ) )
		# Texture filename
		elif values[0] == 'mtllib' :
			material = values[1]
	# Remap face indices
	faces = np.array( faces ) - 1
	# Return the final mesh
	return mtk.Mesh( os.path.splitext(os.path.basename(filename))[0], vertices, faces, colors, material, texcoords, [], normals )
