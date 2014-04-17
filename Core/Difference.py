# -*- coding:utf-8 -*- 


#--
#
# Copyright (C) 2013-2014 Michaël Roy
#
#--


#--
#
# External dependencies
#
#--
#
from numpy import array


#--
#
# Difference
#
#--
#
# Defines a class representing partial differences on triangular mesh
#
class Difference :


	#--
	#
	# Initialisation
	#
	#--
	#
	def __init__( self, mesh=None ) :
		
		# Base mesh
		self.mesh = mesh
		
	#--
	#
	# Gradient
	#
	#--
	#
	def Gradient( self ) :
		
		for u in range(len( self.vertices )) :
			for v in self.mesh.neighbor_vertices[ u ] :
				
	
