#! /usr/bin/env python
# -*- coding:utf-8 -*- 


#
# Application to demonstrate the use of the PyMesh library
#


#
# External dependencies
#
import argparse
import sys
from PyMesh.File.Vrml import *
from PyMesh.Tool.Color import *
from PyMesh.Tool.Curvature import *
from PyMesh.Tool.Repair import *
from test import TestNormals

	
#
# Main
#
if __name__ == "__main__" :
	
	# Initialisation
	mesh = None

	# Create a command line argument parser
	parser = argparse.ArgumentParser( prog='pymesh', description='Process 3D triangular meshes.',
		usage='%(prog)s [-h] [options] input_mesh_file' )
	parser.add_argument( 'input_mesh_file', nargs='?', default=None, help='Input mesh file in VRML format' )
	parser.add_argument( '-info',  action='store_true', help='Print mesh informations' )
	parser.add_argument( '-check', action='store_true', help='Check different mesh parameters' )
	parser.add_argument( '-normals', action='store_true', help='Compute the surface normals' )
	parser.add_argument( '-normalcurvature', action='store_true', help='Compute the surface normal curvature of the mesh' )
	parser.add_argument( '-output', metavar='filename', action='store', help='Write the resulting mesh to a VRML file' )
	parser.add_argument( '-test', action='store_true', help='Test function' )
	parser.add_argument( '-qtviewer', action='store_true', help='Launch OpenGL viewer with Qt' )
	parser.add_argument( '-glutviewer', action='store_true', help='Launch OpenGL viewer with GLUT' )

	# Process command line parameters
	args = parser.parse_args()
	
	# Read the input mesh file
	if args.input_mesh_file :

		sys.stdout.write( 'Read file ' + args.input_mesh_file + '... ' )
		sys.stdout.flush()
		mesh = ReadVrml( args.input_mesh_file )
		print( 'done.' )

		# Print mesh informations
		if args.info :

			print( 'Mesh informations...' )
			print( mesh )
	
		# Compute face and vertex normals
		if args.normals :

			sys.stdout.write( 'Compute normals... ' )
			sys.stdout.flush()
			UpdateNormals( mesh )
			print( 'done.' )

		# Check some mesh parameters
		if args.check :

			sys.stdout.write( 'Check mesh... ' )
			sys.stdout.flush()
			log_message = CheckMesh( mesh )
			if log_message : print( 'Failed\n' + log_message )
			else : print( 'done.' )

		# Compute normal curvature
		if args.normalcurvature :

			sys.stdout.write( 'Compute curvature... ' )
			sys.stdout.flush()
			curvature = GetNormalCurvature( mesh )
			mesh.colors = VectorArray2Colors( curvature )
			print( 'done.' )

		# Test
		if args.test :

			print( 'Test... ' )
			TestNormals( mesh )

		# Write resulting mesh
		if args.output :

			sys.stdout.write( 'Write file ' + args.output + '... ' )
			sys.stdout.flush()
			WriteVrml( mesh, args.output )
			print( 'done.' )

		# Launch GlutViewer
		if args.glutviewer :

			print( 'Launch GLUT viewer...' )
			from PyMesh.Viewer.GlutViewer import GlutViewer
			v = GlutViewer( mesh )
			v.Run()

	# No input file
	elif not args.qtviewer :
		
		# Print help message
		print( 'No input mesh file given...' )
		parser.print_help()
	
	# Launch QtViewer
	if args.qtviewer :

		print( 'Launch Qt viewer...' )
		import sys
		from PySide import QtGui
		from PyMesh.Viewer.QtViewer import QtViewer
		app = QtGui.QApplication( sys.argv )
		window = QtViewer( mesh=mesh )
		window.show()
		sys.exit( app.exec_() )

#	print( '~~ Color border vertices ~~' )
#	border = GetBorderVertices( mesh )
#	mesh.colors = Array2Colors( border )
#	print( '  Done.' )

#	print( '~~ Test normals ~~' )
#	TestNormals( mesh )
#	print( '  Done.' )

		




