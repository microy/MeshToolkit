#! /usr/bin/env python
# -*- coding:utf-8 -*- 


#
# External dependencies
#
import sys
import timeit
from numpy import bincount, cross, sqrt, zeros, allclose
from PyMesh.Core.Mesh import *
from PyMesh.File.Vrml import *
from PyMesh.Tool.Color import *
from PyMesh.Tool.Curvature import *
from PyMesh.Tool.Repair import *

	
	
#
# Main
#
if __name__ == "__main__" :

	filename = ''

	if len(sys.argv) < 2 : filename = 'Models/cube.wrl'
	else : filename = sys.argv[1]

	print( '~~ Read file ' + filename + ' ~~' )
	mesh = ReadVrml( filename )
	print( '  Done.' )

	print( mesh )
	
	print( '~~ Compute normals ~~' )
	UpdateNormals( mesh )
	print( '  Done.' )

	print( '~~ Check mesh ~~' )
	log_message = CheckMesh( mesh )
	if log_message : print( log_message )
	print( '  Done.' )

#	print( '~~ Check neighborhood ~~' )
#	print( CheckNeighborhood( mesh ) )
#	print( '  Done.' )

#	print( '~~ Register edges ~~' )
#	mesh.UpdateEdges()
#	print( '  Done.' )
#	print len( mesh.edges.keys() )
#	print mesh.edges

	print( '~~ Compute curvature ~~' )
	curvature = GetNormalCurvature( mesh )
#	curvature = GetGaussianCurvature( mesh )
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

	print( mesh )

	if len(sys.argv) == 3 :

		print( '~~ Write file ' + sys.argv[2] + ' ~~' )
		WriteVrml( mesh, sys.argv[2] )
		print( '  Done.' )
		

def QtViewer() :

	from PySide import QtGui
	from PyMesh.Viewer.QtViewer import QtViewer
	app = QtGui.QApplication( sys.argv )
	window = QtViewer()
	window.show()
	sys.exit( app.exec_() )


