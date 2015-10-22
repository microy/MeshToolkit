# -*- coding:utf-8 -*- 


#
# Provides functions to check and fix meshes
#


#
# External dependencies
#
import numpy as np


#
# Check several parameters of a given mesh
#
def Check( mesh ) :

	# Initialisation
	log_message = ''

	# Vertex number
	if len(mesh.vertices) < 3 :
		log_message += 'Not enough vertices\n'

	# Face number
	if len(mesh.faces) < 1 :
		log_message += 'Not enough faces\n'

	# Face normal number
	if mesh.face_normal_number and ( mesh.face_normal_number != mesh.face_number ) :
		log_message += 'Face normal number doesn\'t match face number\n'

	# Vertex normal number
	if mesh.vertex_normal_number and ( mesh.vertex_normal_number != mesh.vertex_number ) :
		log_message += 'Vertex normal number doesn\'t match vertex number\n'

	# Color number
	if mesh.color_number and ( mesh.color_number != mesh.vertex_number ) :
		log_message += 'Color number doesn\'t match vertex number\n'

	# Texture coordinate number
	if mesh.texture_number and ( mesh.texture_number != mesh.vertex_number ) :
		log_message += 'Texture coordinate number doesn\'t match vertex number\n'

	# Texture filename
	if mesh.texture_number and not mesh.texture_name :
		log_message += 'Empty texture filename\n'

	# Face indices
	if ( mesh.faces < 0 ).any() or ( mesh.faces >= mesh.vertex_number ).any() :
		log_message += 'Bad face indices\n'

	# Vertex coordinates
	if not np.isfinite( mesh.vertices ).all() :
		log_message += 'Bad vertex coordinates\n'
			
	# Face normals
	if not np.isfinite( mesh.face_normals ).all() :
		log_message += 'Bad face normals\n'
			
	# Vertex normals
	if not np.isfinite( mesh.vertex_normals ).all() :
		log_message += 'Bad vertex normals\n'
			
	# Colors
	if (mesh.colors < 0).any() or (mesh.colors > 1).any() :
		log_message += 'Bad color values\n'

	# Texture coordinates
	if (mesh.textures < 0).any() or (mesh.textures > 1).any() :
		log_message += 'Bad texture coordinates\n'

	# Check isolated vertices
	if (np.array([len(neighbor) for neighbor in mesh.neighbor_faces]) == 0).any() :
		log_message += 'Isolated vertices\n'
		
	# Check degenerated faces
	tris = mesh.vertices[ mesh.faces ]
	face_normals = np.cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	if ( np.sqrt( (face_normals ** 2).sum(axis=1) ) == 0 ).any() :
		log_message += 'Degenerated faces\n'

	# Return the log message
	return log_message


#
# Remove the isolated vertices in a given mesh
# TODO : process colors and texture coordinates
#
def RemoveIsolatedVertices( mesh ) :

	# Register isolated vertices
	isolated_vertices = (np.array([len(neighbor) for neighbor in mesh.neighbor_faces]) == 0)

	# Pouet
#	isolated_vertices = zeros( len(self.vertices) )
#	isolated_vertices[ self.faces[:,0] ] += 1
#	isolated_vertices[ self.faces[:,1] ] += 1
#	isolated_vertices[ self.faces[:,2] ] += 1
#	if any( isolated_vertices == 0 ) : print( "Isolated vertices" )

	# Do nothing if there is no isolated vertex
	if not isolated_vertices.any() : return

	# Create the new vertex array and a lookup table
	new_vertices = []
	index = 0
	lut = np.zeros( mesh.vertex_number, dtype=int )
	for ( v, isolated ) in enumerate( isolated_vertices ) :
		if isolated : continue
		new_vertices.append( mesh.vertices[v] )
		lut[v] = index
		index += 1

	# Create a new face array
	new_faces = lut[mesh.faces].reshape( len(mesh.faces), 3 )
	
	# Update the mesh
	mesh.vertices = np.array( new_vertices )
	mesh.faces = new_faces
	mesh.UpdateNormals()


#
# Remove the degenerated faces of a given mesh
#
def RemoveDegeneratedFaces( mesh ) :
		
	tris = mesh.vertices[ mesh.faces ]
	face_normals = np.cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	print (np.sqrt((face_normals**2).sum(axis=1))>0).all()


#
# Invert the orientation of every face in a given mesh
#
def InvertFacesOrientation( mesh ) :

	# Swap two vertices in each face
	mesh.faces[ :, [0, 1, 2] ] = mesh.faces[ :, [1, 0, 2] ]

	# Recompute face and vertex normals
	mesh.UpdateNormals()
	
