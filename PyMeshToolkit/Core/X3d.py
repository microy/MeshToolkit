# -*- coding:utf-8 -*- 


#
# Import and export X3D files
#


#
# External dependencies
#
from xml.etree.ElementTree import parse
from numpy import fromstring
from PyMesh.Core.Mesh import Mesh


#
# Import a triangular mesh from a X3D file
#
def ReadX3d( filename ) :

	# Initialisation
	faces = []
	vertices = []

	# Read XML file
	tree = parse( filename )
	root = tree.getroot()
	
	for face in root.iter( 'IndexedFaceSet' ) :
		faces = fromstring( face.get( 'coordIndex' ).replace( '-1', '' ), dtype=int, sep=' ' ).reshape( -1, 3 )

	for vertex in root.iter( 'Coordinate' ) :
		vertices = fromstring( vertex.get( 'point' ), sep=' ' ).reshape( -1, 3 )
		
	# Return the final mesh
	return Mesh( name=filename, vertices=vertices, faces=faces )


#
# Export a mesh to a X3D file
#
def WriteX3d( mesh, filename ) :

	pass
