#! /usr/bin/env python
# -*- coding:utf-8 -*- 


#
# Application to demonstrate the use of the PyMeshToolkit library
#


#
# External dependencies
#
import argparse
import sys
import numpy as np
from PyMeshToolkit import *



def Histogram( values ) :
	
	from matplotlib import pyplot
	
	pyplot.hist( values, 100 )
	pyplot.show()

	
# Initialisation
input_mesh = None

# Create a command line argument parser
parser = argparse.ArgumentParser( description='Process 3D triangular meshes.', usage='%(prog)s [options] input_mesh' )
parser.add_argument( 'input_mesh', nargs='?', default=None, help='Input mesh file in PLY format' )
parser.add_argument( '-i',  action='store_true', help='Print mesh informations' )
parser.add_argument( '-b',  action='store_true', help='Color vertices on a border' )
parser.add_argument( '-c', action='store_true', help='Check different mesh parameters' )
parser.add_argument( '-gc', action='store_true', help='Compute the surface gaussian curvature' )
parser.add_argument( '-nc', action='store_true', help='Compute the surface normal curvature' )
parser.add_argument( '-ul', nargs=2, metavar=('N', 'D'), help='Uniform laplacian smoothing with N iteration steps and D diffusion constant' )
parser.add_argument( '-ncf', nargs=2, metavar=('N', 'D'), help='Normalized curvature flow smoothing with N iteration steps and D diffusion constant' )
parser.add_argument( '-o', metavar='file', action='store', help='Write the resulting mesh to a PLY file' )
parser.add_argument( '-cm', default='CubeHelix', metavar='colormap', action='store', help='Colormap (default: cubehelix)' )
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
	input_mesh = ReadPly( args.input_mesh )
	print( 'done.' )

	# Compute surface normals
	sys.stdout.write( 'Compute normals... ' )
	sys.stdout.flush()
	input_mesh.UpdateNormals()
	print( 'done.' )

	# Register neighborhood informations
	sys.stdout.write( 'Register neighbors... ' )
	sys.stdout.flush()
	input_mesh.UpdateNeighbors()
	print( 'done.' )
	
# Launch standalone QtViewer
elif args.qt :

	import PySide.QtGui as qtgui
	sys.stdout.write( 'Launch Qt viewer... ' )
	sys.stdout.flush()
	app = qtgui.QApplication( sys.argv )
	window = QtViewer()
	window.show()
	print( 'done.' )
	sys.exit( app.exec_() )
	
# No input file
else :
	
	# Print help message
	print( '\nNo input mesh file given...\n' )
	parser.print_help()
	sys.exit()

# Print mesh informations
if args.i :

	print( 'Mesh informations...' )
	print( input_mesh )

# Check some mesh parameters
if args.c :

	sys.stdout.write( 'Check mesh... ' )
	sys.stdout.flush()
	log_message = Check( input_mesh )
	if log_message : print( 'Failed\n' + log_message )
	else : print( 'done.' )

# Color vertices on a border
if args.b :

	sys.stdout.write( 'Color border vertices... ' )
	sys.stdout.flush()
	input_mesh.colors = Colormap( args.cm ).ValueArrayToColor( GetBorderVertices( input_mesh ) )
	print( 'done.' )

# Compute gaussian curvature
if args.gc :

	sys.stdout.write( 'Compute gaussian curvature... ' )
	sys.stdout.flush()
	curvature = GetGaussianCurvature( input_mesh )
	Histogram( curvature )
	input_mesh.colors = Colormap( args.cm ).ValueArrayToColor( curvature )
	print( 'done.' )

# Compute normal curvature
if args.nc :

	sys.stdout.write( 'Compute normal curvature... ' )
	sys.stdout.flush()
	curvature = GetNormalCurvature( input_mesh )
	Histogram( np.sqrt( (curvature**2).sum(axis=1) ) )
	input_mesh.colors = Colormap( args.cm ).VectorArrayToColor( curvature )
	print( 'done.' )

# Apply uniform laplacian smoothing
if args.ul :
	
	sys.stdout.write( 'Uniform laplacian smoothing... ' )
	sys.stdout.flush()
	UniformLaplacianSmoothing( input_mesh, int( args.ul[0] ), float( args.ul[1] ) )
	print( 'done.' )

# Apply normalized curvature flow smoothing
if args.ncf :
	
	sys.stdout.write( 'Normalized curvature flow smoothing... ' )
	sys.stdout.flush()
	NormalizedCurvatureFlowSmoothing( input_mesh, int( args.ncf[0] ), float( args.ncf[1] ) )
	print( 'done.' )

# Test
if args.t :

	print( 'Test... ' )
	Test( input_mesh )

# Write resulting mesh
if args.o :

	sys.stdout.write( 'Write file ' + args.o + '... ' )
	sys.stdout.flush()
	WritePly( input_mesh, args.o )
	print( 'done.' )

# Launch GlutViewer
if args.glut :

	sys.stdout.write( 'Launch GLUT viewer... ' )
	sys.stdout.flush()
	v = GlutViewer( input_mesh )
	print( 'done.' )
	v.Run()

# Launch QtViewer
if args.qt :

	import PySide.QtGui as qtgui
	sys.stdout.write( 'Launch Qt viewer... ' )
	sys.stdout.flush()
	app = qtgui.QApplication( sys.argv )
	window = QtViewer( mesh=input_mesh )
	window.show()
	print( 'done.' )
	sys.exit( app.exec_() )
