#! /usr/bin/env python
# -*- coding:utf-8 -*-


#
# Application to demonstrate the use of the MeshToolkit library
#


#
# External dependencies
#
import argparse
import sys
import numpy as np
import MeshToolkit as mtk


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
	print( 'Read file ' + args.input_mesh + '... ' )
	input_mesh = mtk.ReadPly( args.input_mesh )

	# Compute surface normals
	print( 'Compute normals... ' )
	input_mesh.UpdateNormals()

	# Register neighborhood informations
	print( 'Register neighbors... ' )
	input_mesh.UpdateNeighbors()

# Launch standalone QtViewer
elif args.qt :

	print( 'Launch Qt viewer... ' )
	mtk.QtViewer()

# Launch standalone Test
elif args.t :

	print( 'Test... ' )
	mtk.Test()

# No input file
else :

	# Print help message
	print( '\nNo input mesh file given...\n' )
	parser.print_help()
	sys.exit()

# Print mesh informations
if args.i :

	print( input_mesh )

# Check some mesh parameters
if args.c :

	print( 'Check mesh... ' )
	print( mtk.Check( input_mesh ) )

# Color vertices on a border
if args.b :

	print( 'Color border vertices... ' )
	input_mesh.colors = mtk.Colormap( args.cm ).ValueArrayToColor( input_mesh.GetBorderVertices() )

# Compute gaussian curvature
if args.gc :

	print( 'Compute gaussian curvature... ' )
	curvature = mtk.GetGaussianCurvatureReference( input_mesh )
	mtk.Histogram( curvature )
	input_mesh.colors = mtk.Colormap( args.cm ).ValueArrayToColor( curvature )

# Compute normal curvature
if args.nc :

	print( 'Compute normal curvature... ' )
	curvature = mtk.GetNormalCurvature( input_mesh )
	mtk.Statistics( np.sqrt( (curvature**2).sum(axis=1) ) )
	mtk.Histogram( np.sqrt( (curvature**2).sum(axis=1) ) )
	input_mesh.colors = mtk.Colormap( args.cm ).VectorArrayToColor( curvature )

# Apply uniform laplacian smoothing
if args.ul :

	print( 'Uniform laplacian smoothing... ' )
	mtk.UniformLaplacianSmoothing( input_mesh, int( args.ul[0] ), float( args.ul[1] ) )

# Apply normalized curvature flow smoothing
if args.ncf :

	print( 'Normalized curvature flow smoothing... ' )
	mtk.NormalizedCurvatureFlowSmoothing( input_mesh, int( args.ncf[0] ), float( args.ncf[1] ) )

# Test
if args.t and args.input_mesh :

	print( 'Test... ' )
	mtk.Test( input_mesh )

# Write resulting mesh
if args.o :

	print( 'Write file ' + args.o + '... ' )
	mtk.WritePly( input_mesh, args.o )

# Launch GlutViewer
if args.glut :

	print( 'Launch GLUT viewer... ' )
	mtk.GlutViewer( input_mesh ).Run()

# Launch QtViewer
if args.qt :

	print( 'Launch Qt viewer... ' )
	mtk.QtViewer( mesh=input_mesh )
