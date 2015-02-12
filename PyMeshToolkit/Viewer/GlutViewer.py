# -*- coding:utf-8 -*- 


#
# Create an OpenGL window with GLUT to display a 3D mesh
#


#
# External dependencies
#
import platform
import sys
import OpenGL
import OpenGL.GL as gl
import OpenGL.GLUT as glut
from PyMeshToolkit.Viewer.MeshViewer import MeshViewer


#
# Create an OpenGL frame with GLUT
#
class GlutViewer( MeshViewer ) :

	#
	# Initialisation
	#
	def __init__( self, mesh, title='GlutViewer', width=1024, height=768 ) :

		# Initialise OpenGL / GLUT
		glut.glutInit()
		glut.glutInitDisplayMode( glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH | glut.GLUT_MULTISAMPLE )
		glut.glutInitWindowSize( width, height )
		glut.glutInitWindowPosition( 100, 100 )
		glut.glutCreateWindow( title )

		# GLUT function binding
		glut.glutCloseFunc( self.Close )
		glut.glutDisplayFunc( self.Display )
		glut.glutIdleFunc( self.Idle )
		glut.glutKeyboardFunc( self.Keyboard )
		glut.glutMouseFunc( self.Mouse )
		glut.glutMotionFunc( self.MouseMove )
		glut.glutReshapeFunc( self.Resize )

		# OpenGL initialization
		self.InitialiseOpenGL( width, height )
		self.LoadMesh( mesh )
		self.antialiasing = True

	#
	# Keyboard
	#
	def Keyboard( self, key, mouseX, mouseY ) :

		# Escape
		if key == b'\x1b' :

			# Exit
			sys.exit()

		# A
		elif key in [ b'a', b'A' ] :

			# Antialiasing
			self.antialiasing = not self.antialiasing
			self.SetAntialiasing( self.antialiasing )

		# F
		elif key in [ b'f', b'F' ] :

			# Flat shading
			self.SetShader( 'FlatShading' )

		# G
		elif key in [ b'g', b'G' ] :

			# Smooth shading
			self.SetShader( 'SmoothShading' )

		# I
		elif key in [ b'i', b'I' ] :

			# Print system informations
			print( 'System Informations...' )
			print( '  Python :    {}'.format( platform.python_version() ) )
			print( '  PyOpenGL :  {}'.format( OpenGL.__version__ ) )

			# Print OpenGL informations
			self.PrintOpenGLInfo()

		# R
		elif key in [ b'r', b'R' ] :

			# Reset model translation and rotation
			self.Reset()

		# 1
		elif key == b'1' :

			# Display the mesh with solid rendering
			self.wireframe_mode = 0

		# 2
		elif key == b'2' :

			# Display the mesh with wireframe rendering
			self.wireframe_mode = 1

		# 3
		elif key == b'3' :

			# Display the mesh with hidden line removal rendering
			self.wireframe_mode = 2

	#
	# Mouse
	#
	def Mouse( self, button, state, x, y ) :

		# Button down
		if state == glut.GLUT_DOWN :

			# Left button
			if button == glut.GLUT_LEFT_BUTTON :

				# Trackball rotation
				self.MousePress( [ x, y ], 1 )

			# Right button
			elif button == glut.GLUT_RIGHT_BUTTON :

				# Trackball XY translation
				self.MousePress( [ x, y ], 2 )
		
		# Button up
		elif state == glut.GLUT_UP :

			# Wheel up
			if button == 3 :

				# Trackball Z translation 
				self.MouseWheel( 1 )

			# Wheel down
			elif button == 4 :
				
				# Trackball Z translation 
				self.MouseWheel( -1 )
				
			# Mouse button released
			else :
				
				# Stop motion
				self.MouseRelease()

	#
	# Display
	#
	def Display( self ) :

		# Display the mesh
		super( GlutViewer, self ).Display()

		# Swap buffers
		glut.glutSwapBuffers()
		glut.glutPostRedisplay()

	#
	# Idle
	#
	def Idle( self ) :

		# Redraw
		glut.glutPostRedisplay()

	#
	# Run
	#
	@staticmethod
	def Run() :

		# Start up the main loop
		glut.glutMainLoop()
