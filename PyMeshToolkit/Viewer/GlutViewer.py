# -*- coding:utf-8 -*- 


#
# Create an OpenGL window with GLUT to display a 3D mesh
#


#
# External dependencies
#
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from PyMeshToolkit.Viewer.MeshViewer import MeshViewer


#
# Create an OpenGL frame with GLUT
#
class GlutViewer( MeshViewer ) :


	#
	# Initialisation
	#
	def __init__( self, mesh, title="GlutViewer", width=1024, height=768 ) :

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
		glutMotionFunc( self.MouseMove )
		glutReshapeFunc( self.Resize )

		# OpenGL initialization
		MeshViewer.Initialise( self, width, height )
		MeshViewer.LoadMesh( self, mesh )
		self.antialiasing = True


	#
	# Keyboard
	#
	def Keyboard( self, key, mouseX, mouseY ) :

		# Escape
		if key == '\x1b' :

			# Exit
			sys.exit()

		# A
		elif key in [ 'a', 'A' ] :

			# Antialiasing
			self.antialiasing = not self.antialiasing
			MeshViewer.SetAntialiasing( self, self.antialiasing )

		# F
		elif key in [ 'f', 'F' ] :

			# Flat shading
			MeshViewer.SetShader( self, 'FlatShading' )

		# G
		elif key in [ 'g', 'G' ] :

			# Smooth shading
			MeshViewer.SetShader( self, 'SmoothShading' )

		# I
		elif key in [ 'i', 'I' ] :

			# Print OpenGL informations
			self.PrintInfo()

		# R
		elif key in [ 'r', 'R' ] :

			# Reset model translation and rotation
			MeshViewer.Reset( self )

		# 1
		elif key == '1' :

			# Display the mesh with solid rendering
			self.wireframe_mode = 0

		# 2
		elif key == '2' :

			# Display the mesh with wireframe rendering
			self.wireframe_mode = 1

		# 3
		elif key == '3' :

			# Display the mesh with hidden line removal rendering
			self.wireframe_mode = 2
			

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

				# Trackball XY translation
				MeshViewer.MousePress( self, [ x, y ], 2 )
		
		# Button up
		elif state == GLUT_UP :

			# Wheel up
			if button == 3 :

				# Trackball Z translation 
				MeshViewer.MouseWheel( self, 1 )

			# Wheel down
			elif button == 4 :
				
				# Trackball Z translation 
				MeshViewer.MouseWheel( self, -1 )
				
			# Mouse button released
			else :
				
				# Stop motion
				MeshViewer.MouseRelease( self )


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
		print( 'OpenGL Informations...' )
		print( '  Vendor :     ' + glGetString( GL_VENDOR ) )
		print( '  Renderer :   ' + glGetString( GL_RENDERER ) )
		print( '  Version :    ' + glGetString( GL_VERSION ) )
		print( '  Shader :     ' + glGetString( GL_SHADING_LANGUAGE_VERSION ) )
