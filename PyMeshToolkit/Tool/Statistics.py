# -*- coding:utf-8 -*-


#
# Provide functions to compute different statistics on an array of values
#


#
# External dependencies
#
import numpy as np


#
# Print statictics of the given values
#
def Statistics( values ) :
	
	# Compute the statistics of the given values
	stats = list()
	stats.append( ('Minimum', np.amin( values ) ) )
	stats.append( ('Maximum', np.amax( values ) ) )
	stats.append( ('Mean', np.mean( values ) ) )
	stats.append( ('Median', np.median( values ) ) )
	stats.append( ('Deviation', np.std( values ) ) )
	stats.append( ('Variance', np.var( values ) ) )
	
	# Print the stats
	print( 'Statistics...' )
	for s in stats :
		print( '{:>14} : {:>15.5f}'.format( *s ) )
	

#
# Print a histogram of the given values
#
def Histogram( values, bins = 20 ) :
	
	# Compute histogram
    hist, bin_edges = np.histogram( values, bins )
    
    # Get the contribution percentage of each bin
    total = hist.astype( np.float ) / hist.sum()
    
    # Print the histogram in the console
    print( 'Histogram...' )
    for i in range( bins ) :
		print( '{:>14.2f} | {:60} |'.format( bin_edges[i], '_' * int(total[i] * 60) ) )
    print( '{:>14.2f} | {:60} |'.format( bin_edges[bins], '' ) )


