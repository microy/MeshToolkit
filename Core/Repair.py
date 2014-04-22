# -*- coding:utf-8 -*- 


#
# External dependencies
#
from .Mesh import Mesh
from numpy import array, isfinite, zeros


#
# Check several parameters of a given mesh
#
def CheckMesh( mesh ) :

	# Initialisation
	log_message = ''

	# Vertex number
	if len(mesh.vertices) < 3 :
		log_message += 'Not enough vertices\n'

	# Face number
	if len(mesh.faces) < 1 :
		log_message += 'Not enough faces\n'

	# Face normal number
	if len(mesh.face_normals) and (len(mesh.face_normals) != len(mesh.faces)) :
		log_message += 'Face normal number doesn\'t match face number\n'

	# Vertex normal number
	if len(mesh.vertex_normals) and (len(mesh.vertex_normals) != len(mesh.vertices)) :
		log_message += 'Vertex normal number doesn\'t match vertex number\n'

	# Color number
	if len(mesh.colors) and (len(mesh.colors) != len(mesh.vertices)) :
		log_message += 'Color number doesn\'t match vertex number\n'

	# Texture coordinate number
	if len(mesh.textures) and (len(mesh.textures) != len(mesh.vertices)) :
		log_message += 'Texture coordinate number doesn\'t match vertex number\n'

	# Texture filename
	if len(mesh.textures) and not mesh.texture_name :
		log_message += 'Empty texture filename\n'

	# Face indices
	if (mesh.faces < 0).any() or (mesh.faces >= len(mesh.vertices)).any() :
		log_message += 'Bad face indices\n'

	# Vertex coordinates
	if not isfinite(mesh.vertices).all() :
		log_message += 'Bad vertex coordinates\n'
			
	# Face normals
	if not isfinite(mesh.face_normals).all() :
		log_message += 'Bad face normals\n'
			
	# Vertex normals
	if not isfinite(mesh.vertex_normals).all() :
		log_message += 'Bad vertex normals\n'
			
	# Colors
	if (mesh.colors < 0).any() or (mesh.colors > 1).any() :
		log_message += 'Bad color values\n'

	# Texture coordinates
	if (mesh.textures < 0).any() or (mesh.textures > 1).any() :
		log_message += 'Bad texture coordinates\n'

	# Return the log message
	return log_message


#
# Check neighborhood parameters of a given mesh
#
def CheckNeighborhood( mesh ) :

	# Initialization
	log_message = ''

	# Check isolated vertices
	if (array([len(neighbor) for neighbor in mesh.neighbor_faces]) == 0).any() :
		log_message += 'Isolated vertices\n'

	# Return the log message
	return log_message


#
# Remove the isolated vertices in a given mesh
# TODO : process colors and texture coordinates
#
def RemoveIsolatedVertices( mesh ) :

	# Register isolated vertices
	isolated_vertices = (array([len(neighbor) for neighbor in mesh.neighbor_faces]) == 0)

	#
	# Pouet
	#
	border_vertices = zeros( len(self.vertices) )
	border_vertices[ self.faces[:,0] ] += 1
	border_vertices[ self.faces[:,1] ] += 1
	border_vertices[ self.faces[:,2] ] += 1
	if any( border_vertices == 0 ) : print "Isolated vertices"


	# Do nothing if there is no isolated vertex
	if not isolated_vertices.any() : return

	# Create the new vertex array and a lookup table
	new_vertices = []
	index = 0
	lut = zeros( len(mesh.vertices), dtype=int )
	for ( v, isolated ) in enumerate( isolated_vertices ) :
		if isolated : continue
		new_vertices.append( mesh.vertices[v] )
		lut[v] = index
		index += 1

	# Create a new face array
	new_faces = lut[mesh.faces].reshape( len(mesh.faces), 3 )
	
	# Update the mesh
	mesh.vertices = array( new_vertices )
	mesh.faces = new_faces
	mesh.UpdateNormals()
	mesh.UpdateNeighbors()


#
# Remove the degenerated faces of a given mesh
#
def RemoveDegeneratedFaces( mesh ) :
		
	tris = mesh.vertices[ mesh.faces ]
	face_normals = cross( tris[::,1] - tris[::,0]  , tris[::,2] - tris[::,0] )
	print (sqrt((face_normals**2).sum(axis=1))>0).all()


#
# Invert the orientation of every face in a given mesh
#
def InvertFacesOrientation( mesh ) :

	# Swap two vertices in each face
	mesh.faces[ :, [0, 1, 2] ] = mesh.faces[ :, [1, 0, 2] ]

	# Recompute face and vertex normals
	mesh.UpdateNormals()
	
