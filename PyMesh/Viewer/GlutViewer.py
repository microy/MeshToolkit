# -*- coding:utf-8 -*- 


#
# External dependencies
#
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from PyMesh.Viewer.MeshViewer import MeshViewer


#
# Create an OpenGL frame with GLUT
#
class GlutViewer( MeshViewer ) :


	#
	# Initialisation
	#
	def __init__( self, mesh=None, title="GlutViewer", width=1024, height=768 ) :

		# Initialise OpenGL / GLUT
		glutInit()
		glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE )
		glutInitWindowSize( width, height )
		glutInitWindowPosition( 100, 100 )
		glutCreateWindow( title )

		# GLUT function binding
		glutCloseFunc( self.Close )
		glutDisplayFunc( self.Display )
		glutIdleFunc( self.Idle )
		glutKeyboardFunc( self.Keyboard )
		glutMouseFunc( self.Mouse )
		glutMotionFunc( self.Motion )
		glutReshapeFunc( self.Reshape )

		# OpenGL initialization
		MeshViewer.Initialize( self, width, height )
		if mesh : MeshViewer.LoadMesh( self, mesh )


	#
	# Keyboard
	#
	def Keyboard( self, key, mouseX, mouseY ) :

		# Escape
		if key == '\x1b' :

			# Exit
			sys.exit()

		# R
		elif key in [ 'r', 'R' ] :

			# Reset model translation and rotation
			MeshViewer.Reset( self )


	#
	# Mouse
	#
	def Mouse( self, button, state, x, y ) :

		# Button down
		if state == GLUT_DOWN :

			# Left button
			if button == GLUT_LEFT_BUTTON :

				# Trackball rotation
				MeshViewer.MousePress( self, [ x, y ], 1 )

			# Right button
			elif button == GLUT_RIGHT_BUTTON :

				# Z translation
				MeshViewer.MousePress( self, [ x, y ], 2 )
		
		# Button up
		elif state == GLUT_UP :

			# Stop motion
			MeshViewer.MouseRelease( self )


	#
	# Motion
	#
	def Motion( self, x, y ) :

		# Update the trackball
		MeshViewer.Motion( self, [ x, y ] )


	#
	# Reshape
	#
	def Reshape( self, width, height ) :

		# Resize the mesh viewer
		MeshViewer.Resize( self, width, height )


	#
	# Display
	#
	def Display( self ) :

		# Display the mesh
		MeshViewer.Display( self )

		# Swap buffers
		glutSwapBuffers()
		glutPostRedisplay()

	#
	# Idle
	#
	def Idle( self ) :

		# Redraw
		glutPostRedisplay()


	#
	# Close
	#
	def Close( self ) :

		# Close the mesh
		MeshViewer.Close( self )
	

	#
	# Run
	#
	@staticmethod
	def Run() :

		# Start up the main loop
		glutMainLoop()


	#
	# PrintInfo
	#
	def PrintInfo( self ) :

		# Display OpenGL driver informations
		print( '~~~ OpenGL Informations ~~~' )
		print( '  Vendor :   ' + glGetString( GL_VENDOR ) )
		print( '  Renderer : ' + glGetString( GL_RENDERER ) )
		print( '  Version :  ' + glGetString( GL_VERSION ) )
		print( '  Shader :   ' + glGetString( GL_SHADING_LANGUAGE_VERSION ) )
