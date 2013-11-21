#! /usr/bin/env python





if __name__ == "__main__" :

	test = False
	gui = True

	if test :

		from Core.Mesh import *
		from Core.Normal import *
		from Core.Neighbor import *
		from Core.Curvature import *
		from Core.Vrml import *
		from numpy import array, zeros
		print '~~~ Read file ~~~'
		mesh = ReadVrml( 'swirl.wrl' )
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
		print '~~~ Color vertices on the border ~~~'
		mesh.colors = zeros( (len(mesh.vertices), 3) )
		for i in range( len(mesh.vertices) ) :
			if IsBorderVertex( mesh, i ) : mesh.colors[i] = array( [1.0, 0.0, 0.0] )
			else : mesh.colors[i] = array( [0.6, 0.6, 0.6] )
		print '  Done.'
		print '~~~ Compute normal curvature ~~~'
		ComputeNormalCurvature( mesh )
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

