# -*- coding:utf-8 -*- 


#
# Import / Export PLY files
#


#
# Source code adapted from the 'io_mesh_ply' Blender addon
# http://www.blender.org/
#


#
# External dependencies
#
import re
import struct as st
import numpy as np
import PyMeshToolkit


#
# Represents the element stored in the PLY file
#
class PlyElement( object ) :

	#
	# Initialise a PLY element
	#
	def __init__( self, name, count ) :
		
		# Element name
		self.name = name
		
		# Element number
		self.count = count
		
		# List of element properties
		self.properties = []

	#
	# Read the element properties in the PLY file
	#
	def Load( self, file_format, ply_file ) :
		
		# If the file is in ASCII format, read a line, and split the words
		if file_format == b'ascii' : ply_file = ply_file.readline().split()
			
		# Read all the properties of this element
		return [ p.Load( file_format, ply_file ) for p in self.properties ]

	#
	# Return the index of a property contained in the element
	#
	def Index( self, name ) :
		
		# Find the property
		for i, p in enumerate( self.properties ) :
			
			# Return its index
			if p.name == name :	return i
			
		# Property not found
		return -1


#
# Represents the properties stored in the PLY file
#
class PlyProperty( object ) :

	#
	# Initialise the element property
	#
	def __init__( self, name, list_type, numeric_type ) :
		
		# Property name
		self.name = name
		
		# Property type (scalar or list)
		self.list_type = list_type
		
		# Property numeric type (e.g. int, float...)
		self.numeric_type = numeric_type

	#
	# Read the element property in the PLY file
	#
	def Load( self, file_format, ply_file ) :
		
		# List property
		if self.list_type is not None :
			
			# List number
			count = int( self.Read( file_format, 1, self.list_type, ply_file )[0] )
			return self.Read( file_format, count, self.numeric_type, ply_file )
			
		# Scalar property
		else :
			
			return self.Read( file_format, 1, self.numeric_type, ply_file )[0]

	#
	# Read the element property in the PLY file according to the file format
	#
	def Read( self, file_format, count, num_type, ply_file ) :
		
		# ASCII file format
		if file_format == b'ascii' :
			
			# Map the text to the correct value type
			if num_type == 'f' or num_type == 'd' : mapper = float
			else : mapper = int
			
			# Read each property
			ans = [ mapper(x) for x in ply_file[ :count ] ]
			ply_file[ :count ] = []
			
			# Return the property
			return ans
			
		# Binary file format
		else :

			# Property binary format
			# TODO: Modify to use 'format'
			fmt = '%s%i%s' % ( file_format, count, num_type )

			# Read the property
			data = ply_file.read( st.calcsize( fmt ) )
			
			# Return the property
			return st.unpack( fmt, data )


#
# Import a mesh from a PLY file
#
def ReadPly( filename ) :

	# File format specifications
	format_specs = { b'binary_little_endian': '<',
					 b'binary_big_endian': '>',
					 b'ascii': b'ascii' }

	# Data format specifications
	type_specs = { b'char': 'b',
				   b'uchar': 'B',
				   b'int8': 'b',
				   b'uint8': 'B',
				   b'int16': 'h',
				   b'uint16': 'H',
				   b'ushort': 'H',
				   b'int': 'i',
				   b'int32': 'i',
				   b'uint': 'I',
				   b'uint32': 'I',
				   b'float': 'f',
				   b'float32': 'f',
				   b'float64': 'd',
				   b'double': 'd' }

	# Read the PLY file
	with open( filename, 'rb' ) as ply_file :
		
		# Check the file signature
		if not ply_file.readline().startswith( b'ply' ) :
				print( 'Invalid PLY file signature...' )
				return None
		
		# Initialise the elements contained in the PLY file
		elements = []

		# Read and parse the file header
		while True :

			# Read one line of the file header
			line = ply_file.readline()
			
			# Split the words
			words = re.split( br'[ \r\n]+', line )
			
			# PLY file format
			if words[0] == b'format' :
				
				# Store the file format
				file_format = format_specs[ words[1] ]
				
			# Elements
			elif words[0] == b'element' :
				
				# Store the current element name and number
				elements.append( PlyElement( words[1], int( words[2] ) ) )

			# Properties
			elif words[0] == b'property' :

				# List property
				if words[1] == b'list' :
					
					# Add a list property to the current element
					elements[-1].properties.append( PlyProperty( words[4], type_specs[words[2]], type_specs[words[3]] ) )
				
				# Scalar property
				else :
					
					# Add a scalar property to the current element
					elements[-1].properties.append( PlyProperty( words[2], None, type_specs[words[1]] ) )
					
			# Header end
			elif words[0] == b'end_header' :

				# Stop reading the header
				break
			
		# Read the element data
		data = dict( [ ( e.name, [ e.Load( file_format, ply_file ) for j in range( e.count ) ] ) for e in elements ] )

	# Register property indices
	for element in elements :
			
		# Vertex property indices
		if element.name == b'vertex' :

			# Coordinates
			vindices = ( element.Index(b'x'), element.Index(b'y'), element.Index(b'z') )
			
			# Normals
			noindices = ( element.Index(b'nx'), element.Index(b'ny'), element.Index(b'nz') )
			if -1 in noindices : noindices = None
			
			# Textures
			uvindices = ( element.Index(b's'), element.Index(b't') )
			if -1 in uvindices : uvindices = None
			
			# Colors
			colindices = element.Index(b'red'), element.Index(b'green'), element.Index(b'blue')
			if -1 in colindices : colindices = None
				
		# Face property indices
		elif element.name == b'face' :
			
			# Vertex indices
			findex = element.Index( b'vertex_indices' )

	# Convert vertex data to numpy array for easy slicing
	vertex_data = np.array( data[b'vertex'] )

	# Vertex array
	vertices = vertex_data[ :, vindices[0]:vindices[2]+1 ]
	
	# Color array
	colors = []
	if colindices :
		colors = vertex_data[ :, colindices[0]:colindices[2]+1 ]

	# Texture coordinate array
	textures = []
	if uvindices :
		textures = vertex_data[ :, uvindices[0]:uvindices[2]+1 ]

	# Vertex normal array
	normals = []
	if noindices :
		normals = vertex_data[ :, noindices[0]:noindices[2]+1 ]

	# Face array
	faces = np.array( data[ b'face' ] )[ :, findex ]
	
	# Return the resulting mesh from the PLY file data
	return PyMeshToolkit.Core.Mesh( filename, vertices, faces, colors, '', textures, [], normals )
	

#
# Export a mesh to a PLY file
#
def WritePly( filename, mesh, binary = False ) :

	# Open the target PLY file
	with open( filename, 'wb' ) as ply_file :
	
		# Write the PLY file header
		ply_file.write( 'ply\n' )
		if binary : ply_file.write( 'format binary_little_endian 1.0\n')
		else : ply_file.write( 'format ascii 1.0\n')
		ply_file.write( 'element vertex {}\n'.format( mesh.vertex_number ) )
		ply_file.write( 'property float x\n' )
		ply_file.write( 'property float y\n' )
		ply_file.write( 'property float z\n' )
		if mesh.vertex_normal_number :
			ply_file.write( 'property float nx\n' )
			ply_file.write( 'property float ny\n' )
			ply_file.write( 'property float nz\n' )
		if mesh.texture_number :
			ply_file.write( 'property float s\n' )
			ply_file.write( 'property float t\n' )
		if mesh.color_number :
			ply_file.write( 'property uchar red\n' )
			ply_file.write( 'property uchar green\n' )
			ply_file.write( 'property uchar blue\n' )
		ply_file.write( 'element face {}\n'.format( mesh.face_number ) )
		ply_file.write( 'property list uchar int vertex_indices\n' )
		ply_file.write( 'end_header\n' )

		# Binary data
		if binary :
			
			pass
		
		# ASCII data
		else :
			
			# Write the vertex element
			for i in range( mesh.vertex_number ) :
				ply_file.write( '{} {} {}'.format( *mesh.vertices[i] ) )
				if mesh.vertex_normal_number :
					ply_file.write( ' {} {} {}'.format( *mesh.vertex_normals[i] ) )
				if mesh.texture_number :
					ply_file.write( ' {} {}'.format( *mesh.textures[i] ) )
				if mesh.color_number :
					ply_file.write( ' {} {} {}'.format( *mesh.colors[i] ) )
				ply_file.write( '\n' )

			# Write the face element
			for face in mesh.faces :
				ply_file.write('3 {} {} {}\n'.format( *face ) )


#
# Test
#
if __name__ == "__main__" :
	
	import sys
	
	mesh = ReadPly( sys.argv[1] )
	
	print( mesh )

	if len(sys.argv) > 2 :
		
		PyMeshToolkit.File.Ply.WritePly( sys.argv[2], mesh )
