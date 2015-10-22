# -*- coding:utf-8 -*-


#
# Provide a class to convert values to pseudo-colors
#


#
# External dependencies
#
import math
import numpy as np


#
# Class to map values to RGB colors
#
class Colormap( object ) :
	
	#
	# Initialization
	#
	def __init__ ( self, palette='CubeHelix' ) :
		
		if palette == 'Jet' :
			self.colormap = self.ColormapJet
		elif palette == 'Grayscale' :
			self.colormap = self.ColormapGrayscale
		elif palette == 'ColdToHot' :
			self.colormap = self.ColormapColdToHot
		elif palette == 'Rainbow' :
			self.colormap = self.ColormapRainbow
		elif palette == 'CubeHelix' :
			self.colormap = self.ColormapCubeHelix

	#
	# Convert an array of values to pseudo-colors
	#
	def ValueArrayToColor( self, values, normalize = True ) :

		# Normalize the values
		if normalize :
			values = ( values - values.min() ) / ( values.max() - values.min() )

		# Convert each value to a pseudo-color
		return np.array( [ self.colormap( i ) for i in values ] )

	#
	# Convert an array of vectors to pseudo-colors
	#
	def VectorArrayToColor( self, vectors ) :

		# Compute value vector lengths and convert them to colors
		return self.ValueArrayToColor( np.sqrt( (vectors**2).sum(axis=1) ) )

	#
	# Grayscale colormap
	#
	def ColormapGrayscale( self, value ) :

		return [ value, value, value ]

	#
	# ColdToHot colormap
	#
	def ColormapColdToHot( self, value ) :

		if value < 0.25 : return [ 0.0, value * 4.0, 1.0 ]
		elif value < 0.50 : return [ 0.0, 1.0, 1.0 - (value - 0.25) * 4.0 ]
		elif value < 0.75 : return [ (value - 0.5) * 4.0, 1.0, 0.0 ]
		else : return [ 1.0, 1.0 - (value - 0.75) * 4.0, 0.0 ]
		
	#
	# Jet colormap
	#
	def ColormapJet( self, value ) :

		if value < 0.125 : return [ 0.0, 0.0, 0.5 + 0.5 * value * 8.0 ]
		elif value < 0.375 : return [ 0.0, (value - 0.125) * 4.0, 1.0 ]
		elif value < 0.625 : return [ 4.0 * ( value - 0.375 ), 1.0, 1.0 - ( value - 0.375 ) * 4.0 ]
		elif value < 0.875 : return [ 1.0, 1.0 - 4.0 * ( value - 0.625 ), 0.0 ]
		else : return [ 1.0 - 4.0 * ( value - 0.875 ), 0.0, 0.0 ]

	#
	# Rainbow colormap
	#
	def ColormapRainbow( self, value ) :

		if value < 0.2  : return [ 1.0 - value * 5.0, 0.0 , 1.0 ]
		elif value < 0.4 : return [ 0.0, (value - 0.2) * 5.0, 1.0 ]
		elif value < 0.6 : return [ 0.0, 1.0, 1.0 - (value - 0.4) * 5.0 ]
		elif value < 0.8 : return [ (value - 0.6) * 5.0, 1.0, 0.0 ]
		else : return [ 1.0, 1.0 - (value - 0.8) * 5.0, 0.0 ]

	#
	# Cube helix colormap
	#
	# A colour scheme for the display of astronomical intensity images
	# Dave A. Green, Bulletin of the Astronomical Society of India, 39, 289, 2011
	# https://www.mrao.cam.ac.uk/~dag/CUBEHELIX
	#
	def ColormapCubeHelix( self, value, start = 0.5, rots = -1.5, hue = 1.3, gamma = 0.7 ) :
		
		angle = 2.0 * math.pi * ( start / 3.0 + 1.0 + rots * value )
		value = value ** gamma
		amp = hue * value * ( 1.0 - value ) / 2.0
		r = value + amp * ( -0.14861 * math.cos( angle ) + 1.78277 * math.sin( angle ) )
		g = value + amp * ( -0.29227 * math.cos( angle ) - 0.90649 * math.sin( angle ) )
		b = value + amp * ( +1.97249 * math.cos( angle ) )
		return np.clip( [ r, g, b ], 0.0, 1.0 )
