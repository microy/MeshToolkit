#! /usr/bin/env python
# -*- coding:utf-8 -*- 


#
# External dependencies
#
import argparse
import sys
import timeit
from numpy import bincount, cross, sqrt, zeros, allclose
from PyMesh.Core.Mesh import *
from PyMesh.File.Vrml import *
from PyMesh.Tool.Color import *
from PyMesh.Tool.Curvature import *
from PyMesh.Tool.Repair import *

	
#
# Command line argument parser
#
def Parser() :
	
	parser = argparse.ArgumentParser( prog='pymesh', description='Process 3D triangular meshes.' )
	parser.add_argument( 'filename', metavar='filename', help='Name of the VRML file representing the mesh to process' )
	parser.add_argument( '--info', action='store_true', help='Print mesh informations' )
	parser.add_argument( '--check', action='store_true', help='Check different mesh parameters' )
	parser.add_argument( '--normals', action='store_true', help='Compute the surface normals' )
	parser.add_argument( '--normalcurvature', action='store_true', help='Compute the surface normal curvature of the mesh' )
	return parser.parse_args()


#
# Main
#
if __name__ == "__main__" :

	# Process command line parameters
	args = Parser()
	
	# Read the mesh file
	print( '~~ Read file ' + args.filename + ' ~~' )
	mesh = ReadVrml( args.filename )
	print( '  Done.' )

	# Print mesh informations
	if args.info :
		print( '~~ Mesh informations ~~' )
		print( mesh )
	
	# Compute face and vertex normals
	if args.normals :
		print( '~~ Compute normals ~~' )
		UpdateNormals( mesh )
		print( '  Done.' )

	# Check some mesh parameters
	if args.check :
		print( '~~ Check mesh ~~' )
		log_message = CheckMesh( mesh )
		if log_message : print( log_message )
		print( '  Done.' )

	# Compute normal curvature
	if args.normalcurvature :
		print( '~~ Compute curvature ~~' )
		curvature = GetNormalCurvature( mesh )
		mesh.colors = VectorArray2Colors( curvature )
		print( '  Done.' )

#	print( '~~ Color border vertices ~~' )
#	border = GetBorderVertices( mesh )
#	mesh.colors = Array2Colors( border )
#	print( '  Done.' )

#	print( '~~ Test curvature ~~' )
#	TestCurvature( mesh )
#	print( '  Done.' )

#	print( '~~ Test normals ~~' )
#	TestNormals( mesh )
#	print( '  Done.' )

#	print( '~~ Write file ' + sys.argv[2] + ' ~~' )
#	WriteVrml( mesh, sys.argv[2] )
#	print( '  Done.' )
		

def QtViewer() :

	from PySide import QtGui
	from PyMesh.Viewer.QtViewer import QtViewer
	app = QtGui.QApplication( sys.argv )
	window = QtViewer()
	window.show()
	sys.exit( app.exec_() )


