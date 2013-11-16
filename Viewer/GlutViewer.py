# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                GlutViewer.py
#                             -------------------
#    update               : 2013-11-16
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


#
# External dependencies
#
import OpenGL
OpenGL.FORWARD_COMPATIBLE_ONLY = True
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLUT import *

from MeshViewer import *







#--
#
# GlutViewer
#
#--
#
# Create an OpenGL frame with GLUT
#
class GlutViewer( MeshViewer ) :


	#
	# Initialisation
	#
	def __init__( self, mesh="None", title="Untitled Window", width=1024, height=768 ) :

		# Initialise member variables
		self.title = title
		self.width  = width
		self.height = height
		self.frame_count = 0

		# Initialise OpenGL / GLUT
		glutInit()
		glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH )
		glutInitWindowSize( width, height )
		glutInitWindowPosition( 100, 100 )
		glutCreateWindow( title )

		# GLUT function binding
		glutCloseFunc( self.Close )
		glutDisplayFunc( self.Display )
		glutIdleFunc( self.Idle )
		glutKeyboardFunc( self.Keyboard )
		glutMouseFunc( self.Mouse )
		glutReshapeFunc( self.Reshape )
		glutTimerFunc( 0, self.Timer, 0 )

		# OpenGL configuration
		glClearColor( 1, 1, 1, 1 )
		glEnable( GL_DEPTH_TEST )
		glDepthFunc( GL_LESS )
		glEnable( GL_CULL_FACE )

		# MeshViewer initialisation
		MeshViewer.__init__( self, mesh, width, height )



	#
	# PrintInfo
	#
	def PrintInfo( self ) :

		# Display OpenGL driver informations
		print '~~~ OpenGL Informations ~~~'
		print '  Vendor :   ' + glGetString( GL_VENDOR )
		print '  Renderer : ' + glGetString( GL_RENDERER )
		print '  Version :  ' + glGetString( GL_VERSION )
		print '  Shader :   ' + glGetString( GL_SHADING_LANGUAGE_VERSION )


	#
	# Keyboard
	#
	def Keyboard( self, key, mouseX, mouseY ) :

		glutPostRedisplay()


	#
	# Mouse
	#
	def Mouse( self, button, state, x, y ) :

#               case FL_PUSH :
#                       Mouse(Fl::event_button(), Fl::event_x(), Fl::event_y());
#                        break;

 #               // Mouse up event
#                case FL_RELEASE :
#                        motion_state = MOTION_NONE;
#                        cursor(FL_CURSOR_DEFAULT);
#                        break;

#                // Mouse moved while down event
#                case FL_DRAG :
#                        Motion(Fl::event_x(), Fl::event_y());
#                        break;

#                // Keyboard event
#                // Return 1 if you understand/use the keyboard event, 0 otherwise...
#                case FL_KEYBOARD :
#                case FL_SHORTCUT :
#                        if( Keyboard( Fl::event_key() ) ) break;
#                        return 0;



		if button == GLUT_LEFT_BUTTON:
			self.MouseLeftClick(x, y)
		elif button == GLUT_MIDDLE_BUTTON:
			self.MouseMiddleClick(x, y)
		elif button == GLUT_RIGHT_BUTTON:
			self.MouseRightClick(x, y)
		else:
			raise ValueError(button)
		glutPostRedisplay()


	#
	# MouseLeftClick
	#
	def MouseLeftClick( self, x, y ) :
#                motion_state = MOTION_ROTATION;
#                // Trackball Rotation
#                previous_trackball_position = TrackballMapping( x, y );
#                // Change window cursor
#                cursor(FL_CURSOR_HAND);
		pass


	#
	# MouseMiddleClick
	#
	def MouseMiddleClick( self, x, y ) :
#                        motion_state = MOTION_TRANSLATION_XY;
#                        previous_mouse_position = Vector2i( x, y );
#                        cursor(FL_CURSOR_MOVE);
		pass


	#
	# MouseRightClick
	#
	def MouseRightClick( self, x, y ) :
#                        motion_state = MOTION_TRANSLATION_Z;
#                        previous_mouse_position = Vector2i( x, y );
#                        cursor(FL_CURSOR_NS);
		pass


	#
	# Reshape
	#
	def Reshape( self, width, height ) :

		# Resize the viewport
		self.width  = width
		self.height = height
		glViewport( 0, 0, width, height )

		# Recompute the perspective matrix
		MeshViewer.SetPerspectiveMatrix( self, width, height )



	#
	# Display
	#
	def Display( self ) :

		# Framerate counter
		self.frame_count += 1

		# Display the mesh
		MeshViewer.Display( self )

		# Swap buffers
		glutSwapBuffers()
		glutPostRedisplay()


	#
	# Idle
	#
	def Idle( self ) :

		# Redraw
		glutPostRedisplay()


	#
	# Close
	#
	def Close( self ) :

		# Close the mesh
		MeshViewer.Close( self )

		# Initialise member variables


	#
	# Timer
	#
	def Timer( self, value ) :

		# Framerate counter
		if value :
			title = self.title + ' - {} FPS @ {} x {}'.format( self.frame_count * 4, self.width, self.height )
			glutSetWindowTitle( title )     
		self.frame_count = 0
		glutTimerFunc( 250, self.Timer, 1 )
	

	#
	# Run
	#
	@staticmethod
	def Run() :

		# Start up the main loop
		glutMainLoop()




