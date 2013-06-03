#! /usr/bin/env python

from Mesh import *
from SmfFile import *
from pylab import *
from mpl_toolkits.mplot3d import Axes3D


if __name__ == "__main__":

	m = ReadSmfFile("swirl.smf")
	m.ComputeFaceNormals()
	m.ComputeVertexNormals()
	m.CollectNeighbors()
	print m

	fig = figure()
	ax = Axes3D(fig)

	ax.plot( m.vertices[:,0], m.vertices[:,1], m.vertices[:,2], 'o' )


	show()

