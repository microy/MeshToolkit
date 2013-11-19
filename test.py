#! /usr/bin/env python


from Core.Mesh import *
from Core.Normal import *
from Core.Neighbor import *
from Core.Curvature import *
from Core.Vrml import *

#from Viewer.QtViewer import *
#import sys


if __name__ == "__main__":

	print '~~~ Read file ~~~'
	mesh = ReadVrml( 'bunny.wrl' )
	print '  Done.'
	print mesh
	print '~~~ Check mesh ~~~'
	CheckMesh( mesh )
	print '  Done.'
	print '~~~ Compute normals ~~~'
	UpdateNormals( mesh )
	print '  Done.'
	print '~~~ Register neighbors ~~~'
	UpdateNeighbors( mesh )
	print '  Done.'
	print '~~~ Compute normal curvature ~~~'
	ComputeNormalCurvature( mesh )
	print '  Done.'
	

#	app = QtGui.QApplication( sys.argv )
#	window = QtViewer()
#	window.show()
#	sys.exit( app.exec_() )

