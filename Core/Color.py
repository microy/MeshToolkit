# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                   Color.py
#                             -------------------
#    update               : 2013-11-21
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
from numpy import empty
from numpy.linalg import norm


#--
#
# Double2Color
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
# Array2Color
#
#--
#
# Convert an array to a pseudo-color
#
def Array2Color( values ) :

	# Initialize variables
	colors = empty( (len(values), 3) )
	value_lengths = empty( (len(values), 1) )

	# Compute value vector length
	for i in range( len(values) ) :
		value_lengths[i] = norm( values[i] )

	# Compute minimum and maximum value
	min_value = value_lengths.min()
	max_value = value_lengths.max()

	# Compute the range of the values
	value_range = max_value - min_value

	# Convert each value to a pseudo-color
	for i in range( len(values) ) :
		colors[i] = Value2Color( (value_lengths[i] - min_value) / value_range )

	# Return result
	return colors

