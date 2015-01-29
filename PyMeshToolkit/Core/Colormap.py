# -*- coding:utf-8 -*-


#
# Provide utility functions to convert values to pseudo-colors
#


#
# External dependencies
#
import numpy as np




#
# Class to map values to RGB colors
#
class Colormap( object ) :
	
	#
	# Initialization
	#
	def __init__ ( self, palette='Jet' ) :
		
		self.colormap = self.ColormapJet
	
	#
	# Jet colormap
	#
	def ColormapJet( self, value ) :
		
		color = [ 1.0, 1.0, 1.0 ]

		if value < 0.25 :
			
			color[0] = 0.0
			color[1] = 4.0 * value
			
		elif value < 0.5 :
			
			color[0] = 0.0
			color[2] = 1.0 + 4.0 * ( 0.25 - value )
			
		elif value < 0.75 :
			
			color[0] = 4.0 * ( value - 0.5 )
			color[2] = 0
			
		else :
			color[1] = 1.0 + 4.0 * ( 0.75 - value )
			color[2] = 0

		return color


	#
	# Jet colormap 2
	#
	def ColormapJet2( self, value ) :
		
		color = [ 1.0, 1.0, 1.0 ]

		if value < 0.25 :
			
			color[0] = 0.0
			color[1] = 4.0 * value
			
		elif value < 0.5 :
			
			color[0] = 0.0
			color[2] = 1.0 + 4.0 * ( 0.25 - value )
			
		elif value < 0.75 :
			
			color[0] = 4.0 * ( value - 0.5 )
			color[2] = 0
			
		else :
			color[1] = 1.0 + 4.0 * ( 0.75 - value )
			color[2] = 0

		return color




def interpolate( val, y0, x0, y1, x1 ) :
    return ( val - x0 ) * ( y1 - y0 ) / ( x1 - x0 ) + y0

def base( val ) :
    if ( val <= -0.75 ) return 0.0
    else if ( val <= -0.25 ) return interpolate( val, 0.0, -0.75, 1.0, -0.25 )
    else if ( val <= 0.25 ) return 1.0
    else if ( val <= 0.75 ) return interpolate( val, 1.0, 0.25, 0.0, 0.75 )
    else return 0.0

def red( gray ) :
    return base( gray - 0.5 )

def green( gray ) :
    return base( gray )

def blue( gray ) :
    return base( gray + 0.5 )










#
# Jet colormap
#
def ColormapJet( value ) :

	if( value < 0.0  ) : return [ 0.0, 0.0 , 1.0 ]
	if( value < 0.25 ) : return [ 0.0, value * 4.0, 1.0 ]
	if( value < 0.50 ) : return [ 0.0, 1.0, 1.0 - (value - 0.25) * 4.0 ]
	if( value < 0.75 ) : return [ (value - 0.5) * 4.0, 1.0, 0.0 ]
	if( value < 1.0  ) : return [ 1.0, 1.0 - (value - 0.75) * 4.0, 0.0 ]
	return [ 1.0, 0.0, 0.0 ]


#
# Rainbow colormap
#
def ColormapRainbow( value ) :

	if( value < 0.0  ) : return [ 1.0, 0.0 , 1.0 ]
	if( value < 0.2  ) : return [ 1.0 - value * 5.0, 0.0 , 1.0 ]
	if( value < 0.4  ) : return [ 0.0, (value - 0.2) * 5.0, 1.0 ]
	if( value < 0.6  ) : return [ 0.0, 1.0, 1.0 - (value - 0.4) * 5.0 ]
	if( value < 0.8  ) : return [ (value - 0.6) * 5.0, 1.0, 0.0 ]
	if( value < 1.0  ) : return [ 1.0, 1.0 - (value - 0.8) * 5.0, 0.0 ]
	return [ 1.0, 0.0, 0.0 ]


#
# Convert an array of values to pseudo-colors
#
def Array2Colors( values ) :

	# Compute minimum value
	min_value = values.min()

	# Compute the range of the values
	value_range = values.max() - min_value

	# Normalize the values
	norm_values = (values - min_value) / value_range

	# Convert each value to a pseudo-color
	return np.array( [ ColormapJet( i ) for i in norm_values ] )


#
# Convert an array of vectors to pseudo-colors
#
def VectorArray2Colors( values ) :

	# Compute value vector lengths and convert them to colors
	return Array2Colors( np.sqrt((values**2).sum(axis=1)) )


