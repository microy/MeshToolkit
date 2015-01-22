# -*- coding:utf-8 -*-


#
# Provide utility functions to convert values to pseudo-colors
#


#
# External dependencies
#
import numpy as np


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


