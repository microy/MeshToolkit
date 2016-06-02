# -*- coding:utf-8 -*-

#
# Test playground
#

# External dependencies
import numpy as np
import MeshToolkit as mtk

# Generate a "saddle" surface
def GenerateSaddleSurface( xsize = 200, ysize = 200 ) :
	# Compute vertex X-Y coordinates
	X, Y = np.meshgrid( np.linspace( -2, 2, xsize ), np.linspace( -2, 2, ysize ) )
	# Generate the saddle surface
	Z = ( X ** 2 - Y ** 2 ) * 0.5
	# Return a triangular mesh from the grid above
	return mtk.Mesh( 'Saddle' ).CreateFromGrid( X, Y, Z )
