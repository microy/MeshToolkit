#! /usr/bin/env python






if __name__ == "__main__" :

	test = True
	gui = False

	if test :

		from Core.Mesh import *
		from Core.Normal import *
		from Core.Neighbor import *
		from Core.Curvature import *
		from Core.Color import *
		from Core.Vrml import *
		from numpy import array, zeros
		from numpy.linalg import norm
		print '~~~ Read file ~~~'
		mesh = ReadVrml( 'bunny.wrl' )
		print '  Done.'
		print mesh
		print '~~~ Check mesh ~~~'
		CheckMesh( mesh )
		print '  Done.'
		print '~~~ Compute normals ~~~'
#		UpdateNormals( mesh )
		print '  Done.'
		print '~~~ Register neighbors ~~~'
		UpdateNeighbors( mesh )
		print '  Done.'
		print '~~~ Compute normal curvature ~~~'
		normal_curvature = GetNormalCurvature( mesh )
		print '  Done.'
		print '~~~ Color vertices ~~~'
		mesh.colors = Array2Color( normal_curvature )
		print '  Done.'
		print '~~~ Write file ~~~'
		WriteVrml( mesh, 'test.wrl' )
		print '  Done.'

	
	if gui :

		from Viewer.QtViewer import *
		import sys
		app = QtGui.QApplication( sys.argv )
		window = QtViewer()
		window.show()
		sys.exit( app.exec_() )

