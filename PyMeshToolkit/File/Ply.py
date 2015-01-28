# -*- coding:utf-8 -*- 


#
# Import / Export PLY files
#


#
# External dependencies
#
import numpy as np
from PyMeshToolkit.Core.Mesh import Mesh


#
# Import a mesh from a PLY file
#
def ReadPlyHeader( filename ) :
	
	# Initialization
	count = 0
	header = []

	# Open the file
	plyfile = open( filename, 'r' )

	# Check the file format
#	header = vrmlfile.readline()
#	if header is not 'ply' :
		
		# Unknown file header
		# Close the file
#		plyfile.close()
		
		# Raise an error
#		raise RuntimeError( 'Wrong PLY file format !' )

	# Open the file
	with open( filename, 'r' ) as plyfile :

		# Read each line in the file
		for line in plyfile :

			# Store the header line
			header.append( line )
			
			# Count the line
			count += 1
			
			# Header seems to be too long, so we're quitting
			if count > 100 : break
			
			# End of the header
			if line == 'end_header' : break

	# Return the PLY file header
	return header


#
# Import a mesh from a PLY file
#
def ReadPly( filename ) :

	# Initialisation
	vertices = []
	faces = []
	normals = []
	colors = []
	texcoords = []
	material = ""
	
	# Open the file
	plyfile = open( filename, 'r' )

	# Check the header
	header = vrmlfile.readline()
	if header is not 'ply' :
		
		# Unknown file header
		plyfile.close()
		raise RuntimeError( 'Wrong PLY file format !' )

	# Read the file header
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
			faces.append( map( int, [ (v.split('/'))[0] for v in values[1:4] ] ) )

		# Normal
		elif values[0] == 'vn' :
			normals.append( map( float, values[1:4] ) )

		# Color
		elif values[0] == 'c' :
			colors.append( map( float, values[1:4] ) )

		# Texture
		elif values[0] == 'vt' :
			texcoords.append( map( float, values[1:3] ) )

		# Texture filename
		elif values[0] == 'mtllib' :
			material = values[1]
		
	# Remap face indices
	faces = np.array(faces) - 1

	# Return the final mesh
	return Mesh( name=filename, vertices=vertices, faces=faces, colors=colors,
		vertex_normals=normals,	textures=texcoords, texture_name=material )

