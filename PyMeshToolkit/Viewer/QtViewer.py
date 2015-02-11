# -*- coding:utf-8 -*- 


#
# Create a Qt application to display a 3D mesh with OpenGL
#


#
# External dependencies
#
import platform
import OpenGL.GL as gl
import PySide as qt
import PySide.QtCore as qtcore
import PySide.QtGui as qtgui
import PySide.QtOpenGL as qtgl
from PyMeshToolkit.Core.Repair import Check
from PyMeshToolkit.File.Ply import ReadPly, WritePly
from PyMeshToolkit.Viewer.MeshViewer import MeshViewer



#
# Customize the Qt OpenGL widget
# to get our mesh viewer
#
class OpenGLWidget( MeshViewer, qtgl.QGLWidget ) :

	#
	# Initialisation
	#
	def __init__( self, parent=None ) :
		
		# Initialise QGLWidget with multisampling enabled and OpenGL 3 core only
		qtgl.QGLWidget.__init__( self, qtgl.QGLFormat( qtgl.QGL.SampleBuffers | qtgl.QGL.NoDeprecatedFunctions ), parent )

		# Track mouse events
		self.setMouseTracking( True )
		
		# Mesh loaded at the initialisation
		self.init_mesh = None

	#
	# initializeGL
	#
	def initializeGL( self ) :

		# OpenGL initialization
		MeshViewer.Initialise( self, self.width(), self.height() )
		
		# Load the initial mesh
		if self.init_mesh : MeshViewer.LoadMesh( self, self.init_mesh )

	#
	# paintGL
	#
	def paintGL( self ) :

		# Display the mesh
		MeshViewer.Display( self )

	#
	# resizeGL
	#
	def resizeGL( self, width, height ) :

		# Resize the mesh viewer
		MeshViewer.Resize( self, width, height )

	#
	# mousePressEvent
	#
	def mousePressEvent( self, mouseEvent ) :

		# Left button
		if int(mouseEvent.buttons()) & qt.QtCore.Qt.LeftButton : button = 1

		# Right button
		elif int(mouseEvent.buttons()) & qt.QtCore.Qt.RightButton : button = 2

		# Unmanaged
		else : return

		# Update the trackball
		MeshViewer.MousePress( self, [ mouseEvent.x(), mouseEvent.y() ], button )

	#
	# mouseReleaseEvent
	#
	def mouseReleaseEvent( self, mouseEvent ) :

		# Update the trackball
		MeshViewer.MouseRelease( self )

	#
	# mouseMoveEvent
	#
	def mouseMoveEvent( self, mouseEvent ) :

		# Update the trackball
		if MeshViewer.MouseMove( self, mouseEvent.x(), mouseEvent.y() ) :

			# Refresh display
			self.update()

	#
	# wheelEvent
	#
	def wheelEvent( self, event ) :

		# Get the mouse wheel delta for normalisation
		delta = event.delta()

		# Update the trackball
		MeshViewer.MouseWheel( self, delta and delta // abs(delta) )

		# Refresh display
		self.update()

	#
	# OpenGLInfo
	#
	def OpenGLInfo( self ) :

		# Return OpenGL driver informations
		gl_vendor = gl.glGetString( gl.GL_VENDOR ).decode( 'UTF-8' )
		gl_renderer = gl.glGetString( gl.GL_RENDERER ).decode( 'UTF-8' )
		gl_version = gl.glGetString( gl.GL_VERSION ).decode( 'UTF-8' )
		gl_shader = gl.glGetString( gl.GL_SHADING_LANGUAGE_VERSION ).decode( 'UTF-8' )
		return ( gl_vendor, gl_renderer, gl_version, gl_shader )



#
# Create a mesh viewer with Qt
#
class QtViewer( qtgui.QMainWindow ) :

	#
	# Initialisation
	#
	def __init__( self, parent = None, mesh = None ) :

		# Initialise the main window
		super( QtViewer, self ).__init__( parent ) 

		# Initialise the UI
		self.SetupUI()

		# Initialise the mesh
		self.mesh = mesh
		self.opengl_widget.init_mesh = mesh
		
	#
	# Create the user interface
	#
	def SetupUI( self ) :
		
		# Main window parameters
		self.setWindowTitle( 'QtViewer' )
		self.resize(1024, 768)
		
		# Central widget
		self.central_widget = qtgui.QWidget( self )
		self.central_widget.setMouseTracking( True )
		
		# OpenGL widget
		self.opengl_widget = OpenGLWidget( self.central_widget )

		# Layout
		self.horizontalLayout = qtgui.QHBoxLayout( self.central_widget )
		self.horizontalLayout.setSpacing( 0 )
		self.horizontalLayout.setContentsMargins( 0, 0, 0, 0 )
		self.horizontalLayout.addWidget( self.opengl_widget )

		# Set the central widget and layout
		self.setCentralWidget( self.central_widget )

		# Action File -> Open
		self.action_file_open = qtgui.QAction( self )
		self.action_file_open.setText( "&Open..." )
		self.action_file_open.setToolTip( "Open a Stanford PLY file ..." )
		self.action_file_open.setShortcut( "O" )
		qtcore.QObject.connect( self.action_file_open, qtcore.SIGNAL("triggered()"), self.FileOpen )

		# Action File -> Save
		self.action_file_save = qtgui.QAction( self )
		self.action_file_save.setText( "&Save..." )
		self.action_file_save.setToolTip( "Save to a Stanford PLY file ..." )
		self.action_file_save.setShortcut( "S" )
		qtcore.QObject.connect( self.action_file_save, qtcore.SIGNAL("triggered()"), self.FileSave )

		# Action File -> Check
		self.action_file_check = qtgui.QAction( self )
		self.action_file_check.setText( "&Check" )
		self.action_file_check.setToolTip( "Check different parameters of the current mesh" )
		self.action_file_check.setShortcut( "X" )
		qtcore.QObject.connect( self.action_file_check, qtcore.SIGNAL("triggered()"), self.FileCheck )
	
		# Action File -> Close
		self.action_file_close = qtgui.QAction( self )
		self.action_file_close.setText( "C&lose" )
		self.action_file_close.setToolTip( "Close the current mesh" )
		self.action_file_close.setShortcut( "W" )
		qtcore.QObject.connect( self.action_file_close, qtcore.SIGNAL("triggered()"), self.FileClose )
		
		# Action File -> Quit
		self.action_file_quit = qtgui.QAction( self )
		self.action_file_quit.setText( "&Quit" )
		self.action_file_quit.setToolTip( "Quit the application" )
		self.action_file_quit.setShortcut( "Esc" )
		qtcore.QObject.connect( self.action_file_quit, qtcore.SIGNAL("triggered()"), self.close )
		
		# Action View -> Flat
		self.action_view_flat = qtgui.QAction( self )
		self.action_view_flat.setCheckable( True )
		self.action_view_flat.setChecked( False )
		self.action_view_flat.setText( "&Flat Shading" )
		self.action_view_flat.setToolTip( "Enable flat shading" )
		self.action_view_flat.setShortcut( "F" )
		qtcore.QObject.connect( self.action_view_flat, qtcore.SIGNAL("triggered()"), self.ViewFlat )
	
		# Action View -> Smooth
		self.action_view_smooth = qtgui.QAction( self )
		self.action_view_smooth.setCheckable( True )
		self.action_view_smooth.setChecked( True )
		self.action_view_smooth.setText( "&Smooth shading" )
		self.action_view_smooth.setToolTip( "Enable smooth shading" )
		self.action_view_smooth.setShortcut( "G" )
		qtcore.QObject.connect( self.action_view_smooth, qtcore.SIGNAL("triggered()"), self.ViewSmooth )
	
		# Action View -> Solid
		self.action_view_solid = qtgui.QAction( self )
		self.action_view_solid.setCheckable( True )
		self.action_view_solid.setChecked( True )
		self.action_view_solid.setText( "S&olid" )
		self.action_view_solid.setToolTip( "Enable solid rendering" )
		self.action_view_solid.setShortcut( "1" )
		qtcore.QObject.connect( self.action_view_solid, qtcore.SIGNAL("triggered()"), self.ViewSolid )

		# Action View -> Wireframe
		self.action_view_wireframe = qtgui.QAction( self )
		self.action_view_wireframe.setCheckable( True )
		self.action_view_wireframe.setText( "&Wireframe" )
		self.action_view_wireframe.setToolTip( "Enable wireframe rendering" )
		self.action_view_wireframe.setShortcut( "2" )
		qtcore.QObject.connect( self.action_view_wireframe, qtcore.SIGNAL("triggered()"), self.ViewWireframe )
	
		# Action View -> Hidden lines
		self.action_view_hiddenlines = qtgui.QAction( self )
		self.action_view_hiddenlines.setCheckable( True )
		self.action_view_hiddenlines.setText( "&Hidden lines" )
		self.action_view_hiddenlines.setToolTip( "Enable wireframe rendering with hidden lines removal" )
		self.action_view_hiddenlines.setShortcut( "3" )
		qtcore.QObject.connect( self.action_view_hiddenlines, qtcore.SIGNAL("triggered()"), self.ViewHiddenlines )

		# Action View -> Antialiasing
		self.action_view_antialiasing = qtgui.QAction( self )
		self.action_view_antialiasing.setCheckable( True )
		self.action_view_antialiasing.setChecked( True )
		self.action_view_antialiasing.setText( "&Antialiasing" )
		self.action_view_antialiasing.setToolTip( "Enable antialiasing" )
		self.action_view_antialiasing.setShortcut( "A" )
		qtcore.QObject.connect( self.action_view_antialiasing, qtcore.SIGNAL("triggered()"), self.ViewAntialiasing )
	
		# Action View -> Reset
		self.action_view_reset = qtgui.QAction( self )
		self.action_view_reset.setText( "&Reset" )
		self.action_view_reset.setToolTip( "Reset the current view" )
		self.action_view_reset.setShortcut( "R" )
		qtcore.QObject.connect( self.action_view_reset, qtcore.SIGNAL("triggered()"), self.ViewReset )
	
		# Action Help -> About
		self.action_help_about = qtgui.QAction( self )
		self.action_help_about.setText( "&About QtViewer..." )
		self.action_help_about.setToolTip( "About this application" )
		self.action_help_about.setShortcut( "F1" )
		qtcore.QObject.connect( self.action_help_about, qtcore.SIGNAL("triggered()"), self.HelpAbout )

		# Action Help -> About Qt
		self.action_help_qt = qtgui.QAction( self )
		self.action_help_qt.setText( "About &Qt..." )
		self.action_help_qt.setShortcut( "F2" )
		qtcore.QObject.connect( self.action_help_qt, qtcore.SIGNAL("triggered()"), self.HelpAboutQt )

		# Action Help -> About OpenGL
		self.action_help_opengl = qtgui.QAction( self )
		self.action_help_opengl.setText( "About &OpenGL..." )
		self.action_help_opengl.setToolTip( "OpenGL informations" )
		self.action_help_opengl.setShortcut( "F3" )
		qtcore.QObject.connect( self.action_help_opengl, qtcore.SIGNAL("triggered()"), self.HelpAboutOpenGL )
	
		# Create the menu bar
		self.menubar = qtgui.QMenuBar( self )

		# Setup the file menu
		self.menu_file = qtgui.QMenu( self.menubar )
		self.menu_file.setTitle( "&File" )
		self.menu_file.addAction( self.action_file_open )
		self.menu_file.addAction( self.action_file_save )
		self.menu_file.addSeparator()
		self.menu_file.addAction( self.action_file_check )
		self.menu_file.addSeparator()
		self.menu_file.addAction( self.action_file_close )
		self.menu_file.addAction( self.action_file_quit )
		
		# Setup the view menu
		self.menu_view = qtgui.QMenu( self.menubar )
		self.menu_view.setTitle( "&View" )
		self.menu_view.addAction( self.action_view_flat )
		self.menu_view.addAction( self.action_view_smooth )
		self.menu_view.addSeparator()
		self.menu_view.addAction( self.action_view_solid )
		self.menu_view.addAction( self.action_view_wireframe )
		self.menu_view.addAction( self.action_view_hiddenlines )
		self.menu_view.addSeparator()
		self.menu_view.addAction( self.action_view_antialiasing )
		self.menu_view.addSeparator()
		self.menu_view.addAction( self.action_view_reset )
		
		# Setup the help menu
		self.menu_help = qtgui.QMenu( self.menubar )
		self.menu_help.setTitle( "&Help" )
		self.menu_help.addAction( self.action_help_about )
		self.menu_help.addAction( self.action_help_qt )
		self.menu_help.addAction( self.action_help_opengl )
		
		# Setup the menu bar
		self.menubar.addAction( self.menu_file.menuAction() )
		self.menubar.addAction( self.menu_view.menuAction() )
		self.menubar.addAction( self.menu_help.menuAction() )

		# Set the menu bar to the main window
		self.setMenuBar( self.menubar )

	#
	# File -> Open
	#
	def FileOpen( self ) :

		# Open file dialog
		( filename, selected_filter ) = qtgui.QFileDialog.getOpenFileName( self, 'Open a Stanford PLY file...', '',
			'Stanford PLY files (*.ply);;All files (*.*)' )

		# Check filename
		if not filename : return

		# Read PLY file
		self.mesh = ReadPly( filename )

		# Send the mesh to the OpenGL viewer
		self.opengl_widget.LoadMesh( self.mesh )

	#
	# File -> Save
	#
	def FileSave( self ) :

		# Nothing to save
		if not self.mesh : return

		# Open file dialog
		( filename, selected_filter ) = qtgui.QFileDialog.getSaveFileName( self, 'Save to a Stanford PLY file...', '',
			'Stanford PLY files (*.ply);;All files (*.*)' )

		# Check filename
		if not filename : return

		# Save PLY file
		WritePly( self.mesh, filename )

	#
	# File -> Check
	#
	def FileCheck( self ) :

		# Nothing to check
		if not self.mesh : return

		# Check different parameters of the mesh
		Check( self.mesh )

	#
	# File -> Close
	#
	def FileClose( self ) :

		# Close the mesh
		self.opengl_widget.Close()
		self.mesh = None
		self.opengl_widget.update()

	#
	# View -> Flat
	#
	def ViewFlat( self ) :

		# Set flat shading
		self.action_view_flat.setChecked( True )
		self.action_view_smooth.setChecked( False )
		self.opengl_widget.SetShader( 'FlatShading' )
		self.opengl_widget.update()

	#
	# View -> Smooth
	#
	def ViewSmooth( self ) :

		# Set smooth shading
		self.action_view_flat.setChecked( False )
		self.action_view_smooth.setChecked( True )
		self.opengl_widget.SetShader( 'SmoothShading' )
		self.opengl_widget.update()

	#
	# View -> Solid
	#
	def ViewSolid( self ) :

		# Enable / Disable solid rendering
		self.action_view_solid.setChecked( True )
		self.action_view_wireframe.setChecked( False )
		self.action_view_hiddenlines.setChecked( False )
		self.opengl_widget.wireframe_mode = 0
		self.opengl_widget.update()

	#
	# View -> Wireframe
	#
	def ViewWireframe( self ) :

		# Enable / Disable wireframe rendering
		self.action_view_solid.setChecked( False )
		self.action_view_wireframe.setChecked( True )
		self.action_view_hiddenlines.setChecked( False )
		self.opengl_widget.wireframe_mode = 1
		self.opengl_widget.update()

	#
	# View -> Hidden lines
	#
	def ViewHiddenlines( self ) :

		# Enable / Disable hideen lines rendering
		self.action_view_solid.setChecked( False )
		self.action_view_wireframe.setChecked( False )
		self.action_view_hiddenlines.setChecked( True )
		self.opengl_widget.wireframe_mode = 2
		self.opengl_widget.update()

	#
	# View -> Antialiasing
	#
	def ViewAntialiasing( self ) :

		# Enable / Disable antialiasing
		self.action_view_antialiasing.setChecked( self.action_view_antialiasing.isChecked() )
		self.opengl_widget.SetAntialiasing( self.action_view_antialiasing.isChecked() )
		self.opengl_widget.update()

	#
	# View -> Reset
	#
	def ViewReset( self ) :

		# Reset model transformation
		self.opengl_widget.Reset()
		self.opengl_widget.update()

	#
	# Help -> About
	#
	def HelpAbout( self ) :

		qtgui.QMessageBox.about( self, 'About QtViewer',
		'''<b>PyMeshToolkit QtViewer</b>
        <p>Copyright (c) 2013-2015 Michael Roy.</p>
        <p>All rights reserved in accordance with the MIT License.</p>
        <i><p>Python {}</p><p>PySide version {}</p><p>Qt version {} on {}</p></i>'''.format(
        platform.python_version(), qt.__version__, qt.QtCore.__version__,
        platform.system()))

	#
	# Help -> About Qt
	#
	def HelpAboutQt( self ) :
		
		qtgui.QMessageBox.aboutQt( self, 'About Qt' )
		
	#
	# Help -> About OpenGL
	#
	def HelpAboutOpenGL( self ) :
		
		( gl_vendor, gl_renderer, gl_version, gl_shader ) = self.opengl_widget.OpenGLInfo()
		
		qtgui.QMessageBox.about( self, 'About OpenGL', '''<p><b>Vendor :</b> {}</p>
			<p><b>Renderer :</b> {}</p>
			<p><b>Version :</b> {}</p>
			<p><b>Shader :</b> {}</p>'''.format( gl_vendor, gl_renderer, gl_version, gl_shader ) )

