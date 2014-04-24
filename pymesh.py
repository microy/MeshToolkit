#! /usr/bin/env python
# -*- coding:utf-8 -*- 


#
# External dependencies
#
import argparse
from PyMesh.File.Vrml import *
from PyMesh.Tool.Color import *
from PyMesh.Tool.Curvature import *
from PyMesh.Tool.Repair import *

	
#
# Main
#
if __name__ == "__main__" :

	# Create a command line argument parser
	parser = argparse.ArgumentParser( prog='pymesh', description='Process 3D triangular meshes.',
		usage='%(prog)s [-h] [options] input_mesh_file' )
	parser.add_argument( 'input_mesh_file', nargs='?', default=None, help='Input mesh file in VRML format' )
	parser.add_argument( '-info',  action='store_true', help='Print mesh informations' )
	parser.add_argument( '-check', action='store_true', help='Check different mesh parameters' )
	parser.add_argument( '-normals', action='store_true', help='Compute the surface normals' )
	parser.add_argument( '-normalcurvature', action='store_true', help='Compute the surface normal curvature of the mesh' )
	parser.add_argument( '-output', metavar='filename', action='store', help='Write the resulting mesh to a VRML file' )
	parser.add_argument( '-qtviewer', action='store_true', help='Launch OpenGL viewer with Qt' )
	parser.add_argument( '-glutviewer', action='store_true', help='Launch OpenGL viewer with GLUT' )

	# Process command line parameters
	args = parser.parse_args()
	
	# Read the input mesh file
	if args.input_mesh_file :

		print( '~~ Read file ' + args.input_mesh_file + ' ...' )
		mesh = ReadVrml( args.input_mesh_file )
		print( '  Done.' )

		# Print mesh informations
		if args.info :

			print( '~~ Mesh informations ...' )
			print( mesh )
	
		# Compute face and vertex normals
		if args.normals :

			print( '~~ Compute normals ...' )
			UpdateNormals( mesh )
			print( '  Done.' )

		# Check some mesh parameters
		if args.check :

			print( '~~ Check mesh ...' )
			log_message = CheckMesh( mesh )
			if log_message : print( log_message )
			print( '  Done.' )

		# Compute normal curvature
		if args.normalcurvature :

			print( '~~ Compute curvature ...' )
			curvature = GetNormalCurvature( mesh )
			mesh.colors = VectorArray2Colors( curvature )
			print( '  Done.' )

		# Write resulting mesh
		if args.output :

			print( '~~ Write file ' + args.output + ' ...' )
			WriteVrml( mesh, args.output )
			print( '  Done.' )

		# Launch GlutViewer
		if args.glutviewer :

			from PyMesh.Viewer.GlutViewer import GlutViewer
			v = GlutViewer( mesh )
			v.PrintInfo()
			v.Run()

	# No input file
	else : print( 'No input mesh file given...' )
	
	# Launch QtViewer
	if args.qtviewer :

		import sys
		from PySide import QtGui
		from PyMesh.Viewer.QtViewer import QtViewer
		app = QtGui.QApplication( sys.argv )
		window = QtViewer()
		window.show()
		sys.exit( app.exec_() )
		
	# Print help message
	else : parser.print_help()



#	print( '~~ Color border vertices ~~' )
#	border = GetBorderVertices( mesh )
#	mesh.colors = Array2Colors( border )
#	print( '  Done.' )

#	print( '~~ Test normals ~~' )
#	TestNormals( mesh )
#	print( '  Done.' )

		




