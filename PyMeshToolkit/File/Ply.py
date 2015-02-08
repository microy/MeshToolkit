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
def ReadPly( filename ) :

	# Initialisation
	vertices = []
	faces = []
	normals = []
	colors = []
	texcoords = []
	material = ""
	file_type = None
	current_element = None
	vertex_number = 0
	face_number = 0
	ply_file = False
	
	# Read file header
	with open( filename, 'r' ) as plyfile :

		# Read each line in the file
		for line in plyfile :

			# Split the words in the line 
			words = line.split()
			
			# File type
			if words[0] == 'ply' :
				
				ply_file = True

			# PLY file format
			elif words[0] == 'format' :
				
				file_type = words[1]
				
			# Comments
			elif words[0] == 'comment' :
				
				continue
				
			# Elements
			elif words[0] == 'element' :
				
				# Save the current element
				current_element = words[1]
				
				# Vertex number
				if words[1] == 'vertex' :
					
					vertex_number = int( words[2] )
					
				# Face number
				elif words[1] == 'face' :
				
					face_number = int( words[2] )
			
			# Properties
			elif words[0] == 'property' :
				
				if current_element == 'vertex' :
				
					pass
					
			# Header end
			elif words[0] == 'end_header' :
				
				break
				
	print vertex_number, face_number
