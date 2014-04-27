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
from PyMesh.Core.Mesh import *
from PyMesh.File.Vrml import *
from PyMesh.Tool.Color import *
from PyMesh.Tool.Curvature import *
from PyMesh.Tool.Repair import *
from PyMesh.Tool.Denoising import *
from test import Test

	
#
# Main
#
if __name__ == "__main__" :
	
	# Initialisation
	input_mesh = None

	# Create a command line argument parser
	parser = argparse.ArgumentParser( prog='pymesh', description='Process 3D triangular meshes.',
		usage='%(prog)s [-h] [options] input_mesh' )
	parser.add_argument( 'input_mesh', nargs='?', default=None, help='Input mesh file in VRML format' )
	parser.add_argument( '-i',  action='store_true', help='Print mesh informations' )
	parser.add_argument( '-b',  action='store_true', help='Color vertices on a border' )
	parser.add_argument( '-c', action='store_true', help='Check different mesh parameters' )
	parser.add_argument( '-nc', action='store_true', help='Compute the surface normal curvature' )
	parser.add_argument( '-ul', nargs=2, metavar=('n', 'd'), help='Uniform laplacian smoothing with n iteration and d diffusion' )
	parser.add_argument( '-o', metavar='file', action='store', help='Write the resulting mesh to a VRML file' )
	parser.add_argument( '-t', action='store_true', help='Test function' )
	parser.add_argument( '-qt', action='store_true', help='Launch OpenGL viewer with Qt' )
	parser.add_argument( '-glut', action='store_true', help='Launch OpenGL viewer with GLUT' )

	# Process command line parameters
	args = parser.parse_args()
	
	# Input mesh
	if args.input_mesh :

		# Read the input mesh file
		sys.stdout.write( 'Read file ' + args.input_mesh + '... ' )
		sys.stdout.flush()
		input_mesh = ReadVrml( args.input_mesh )
		print( 'done.' )

		# Compute surface normals
		sys.stdout.write( 'Compute normals... ' )
		sys.stdout.flush()
		UpdateNormals( input_mesh )
		print( 'done.' )

		# Register neighborhood informations
		sys.stdout.write( 'Register neighbors... ' )
		sys.stdout.flush()
		UpdateNeighbors( input_mesh )
		print( 'done.' )

		# Print mesh informations
		if args.i :

			print( 'Mesh informations...' )
			print( input_mesh )
	
		# Check some mesh parameters
		if args.c :

			sys.stdout.write( 'Check mesh... ' )
			sys.stdout.flush()
			log_message = CheckMesh( input_mesh )
			if log_message : print( 'Failed\n' + log_message )
			else : print( 'done.' )

		# Color vertices on a border
		if args.b :

			sys.stdout.write( 'Color border vertices... ' )
			sys.stdout.flush()
			input_mesh.colors = Array2Colors( GetBorderVertices( input_mesh ) )
			print( 'done.' )

		# Compute normal curvature
		if args.nc :

			sys.stdout.write( 'Compute curvature... ' )
			sys.stdout.flush()
			input_mesh.colors = VectorArray2Colors( GetNormalCurvature( input_mesh ) )
			print( 'done.' )

		# Apply uniform laplacian smoothing
		if args.ul :
			
			sys.stdout.write( 'Uniform laplacian smoothing... ' )
			sys.stdout.flush()
			UniformLaplacianSmoothing( input_mesh, int( args.ul[0] ), float( args.ul[1] ) )
			print( 'done.' )

		# Test
		if args.t :

			print( 'Test... ' )
			Test( input_mesh )

		# Write resulting mesh
		if args.o :

			sys.stdout.write( 'Write file ' + args.o + '... ' )
			sys.stdout.flush()
			WriteVrml( input_mesh, args.o )
			print( 'done.' )

		# Launch GlutViewer
		if args.glut :

			print( 'Launch GLUT viewer...' )
			from PyMesh.Viewer.GlutViewer import GlutViewer
			v = GlutViewer( input_mesh )
			v.Run()

	# No input file
	elif not args.qt :
		
		# Print help message
		print( 'No input mesh file given...' )
		parser.print_help()
	
	# Launch QtViewer
	if args.qt :

		print( 'Launch Qt viewer...' )
		import sys
		from PySide import QtGui
		from PyMesh.Viewer.QtViewer import QtViewer
		app = QtGui.QApplication( sys.argv )
		window = QtViewer( mesh=input_mesh )
		window.show()
		sys.exit( app.exec_() )

		




