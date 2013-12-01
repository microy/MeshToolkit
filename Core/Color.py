# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Color.py
#                             -------------------
#    update               : 2013-12-01
#    copyright            : (C) 2013 by Michaël Roy
#    email                : microygh@gmail.com
# ***************************************************************************

# ***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************


#-
#
# External dependencies
#
#-
#
from numpy import array, copy, zeros, sqrt


#--
#
# Value2Color
#
#--
#
# Convert a value in range [ 0.0, 1.0 ] to a pseudo-color
#
def Value2Color( value ) :

	if( value < 0.0  ) : return [ 0.0, 0.0 , 1.0 ]
	if( value < 0.25 ) : return [ 0.0, value * 4.0, 1.0 ]
	if( value < 0.50 ) : return [ 0.0, 1.0, 1.0 - (value - 0.25) * 4.0 ]
	if( value < 0.75 ) : return [ (value - 0.5) * 4.0, 1.0, 0.0 ]
	if( value < 1.0  ) : return [ 1.0, 1.0 - (value - 0.75) * 4.0, 0.0 ]
	return [ 1.0, 0.0, 0.0 ]



#--
#
# Value2ColorAlternate
#
#--
#
# Convert a value in range [ 0.0, 1.0 ] to a pseudo-color
#
def Value2ColorAlternate( value ) :

	if( value < 0.0  ) : return [ 1.0, 0.0 , 1.0 ]
	if( value < 0.2  ) : return [ 1.0 - value * 5.0, 0.0 , 1.0 ]
	if( value < 0.4  ) : return [ 0.0, (value - 0.2) * 5.0, 1.0 ]
	if( value < 0.6  ) : return [ 0.0, 1.0, 1.0 - (value - 0.4) * 5.0 ]
	if( value < 0.8  ) : return [ (value - 0.6) * 5.0, 1.0, 0.0 ]
	if( value < 1.0  ) : return [ 1.0, 1.0 - (value - 0.8) * 5.0, 0.0 ]
	return [ 1.0, 0.0, 0.0 ]



#--
#
# Array2Colors
#
#--
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
	colors = [ Value2Color( i ) for i in norm_values ]

	# Return result
	return array( colors )


#--
#
# VectorArray2Colors
#
#--
#
# Convert an array of vectors to pseudo-colors
#
def VectorArray2Colors( values ) :

	# Compute value vector lengths and convert them to colors
	return Array2Colors( sqrt((values**2).sum(axis=1)) )


