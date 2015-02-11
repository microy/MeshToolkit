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
		self.setupUi( self )

		# Initialise the mesh
		self.mesh = mesh
		self.opengl_widget.init_mesh = mesh
		
	#
	# Create the user interface
	#
	def setupUi(self, MainWindow) :
		
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1024, 768)
		self.central_widget = qtgui.QWidget(MainWindow)
		self.central_widget.setMouseTracking(True)
		self.central_widget.setObjectName("central_widget")
		self.horizontalLayout = qtgui.QHBoxLayout(self.central_widget)
		self.horizontalLayout.setSpacing(0)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.opengl_widget = OpenGLWidget(self.central_widget)
		self.opengl_widget.setObjectName("opengl_widget")
		self.horizontalLayout.addWidget(self.opengl_widget)
		MainWindow.setCentralWidget(self.central_widget)
		self.menubar = qtgui.QMenuBar(MainWindow)
		self.menubar.setGeometry(qtcore.QRect(0, 0, 1024, 30))
		self.menubar.setObjectName("menubar")
		self.menu_file = qtgui.QMenu(self.menubar)
		self.menu_file.setObjectName("menu_file")
		self.menu_view = qtgui.QMenu(self.menubar)
		self.menu_view.setObjectName("menu_view")
		self.menu_help = qtgui.QMenu(self.menubar)
		self.menu_help.setObjectName("menu_help")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = qtgui.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.action_file_open = qtgui.QAction(MainWindow)
		self.action_file_open.setObjectName("action_file_open")
		self.action_file_save = qtgui.QAction(MainWindow)
		self.action_file_save.setObjectName("action_file_save")
		self.action_file_check = qtgui.QAction(MainWindow)
		self.action_file_check.setObjectName("action_file_check")
		self.action_file_close = qtgui.QAction(MainWindow)
		self.action_file_close.setObjectName("action_file_close")
		self.action_file_quit = qtgui.QAction(MainWindow)
		self.action_file_quit.setObjectName("action_file_quit")
		self.action_view_flat = qtgui.QAction(MainWindow)
		self.action_view_flat.setCheckable(True)
		self.action_view_flat.setChecked(False)
		self.action_view_flat.setObjectName("action_view_flat")
		self.action_view_smooth = qtgui.QAction(MainWindow)
		self.action_view_smooth.setCheckable(True)
		self.action_view_smooth.setChecked(True)
		self.action_view_smooth.setObjectName("action_view_smooth")
		self.action_view_wireframe = qtgui.QAction(MainWindow)
		self.action_view_wireframe.setCheckable(True)
		self.action_view_wireframe.setObjectName("action_view_wireframe")
		self.action_view_antialiasing = qtgui.QAction(MainWindow)
		self.action_view_antialiasing.setCheckable(True)
		self.action_view_antialiasing.setChecked(True)
		self.action_view_antialiasing.setObjectName("action_view_antialiasing")
		self.action_view_reset = qtgui.QAction(MainWindow)
		self.action_view_reset.setObjectName("action_view_reset")
		self.action_help_about = qtgui.QAction(MainWindow)
		self.action_help_about.setObjectName("action_help_about")
		self.action_help_opengl = qtgui.QAction(MainWindow)
		self.action_help_opengl.setObjectName("action_help_opengl")
		self.action_help_qt = qtgui.QAction(MainWindow)
		self.action_help_qt.setObjectName("action_help_qt")
		self.action_view_hiddenlines = qtgui.QAction(MainWindow)
		self.action_view_hiddenlines.setCheckable(True)
		self.action_view_hiddenlines.setObjectName("action_view_hiddenlines")
		self.action_view_solid = qtgui.QAction(MainWindow)
		self.action_view_solid.setCheckable(True)
		self.action_view_solid.setChecked(True)
		self.action_view_solid.setObjectName("action_view_solid")
		self.menu_file.addAction(self.action_file_open)
		self.menu_file.addAction(self.action_file_save)
		self.menu_file.addSeparator()
		self.menu_file.addAction(self.action_file_check)
		self.menu_file.addSeparator()
		self.menu_file.addAction(self.action_file_close)
		self.menu_file.addAction(self.action_file_quit)
		self.menu_view.addAction(self.action_view_flat)
		self.menu_view.addAction(self.action_view_smooth)
		self.menu_view.addSeparator()
		self.menu_view.addAction(self.action_view_solid)
		self.menu_view.addAction(self.action_view_wireframe)
		self.menu_view.addAction(self.action_view_hiddenlines)
		self.menu_view.addSeparator()
		self.menu_view.addAction(self.action_view_antialiasing)
		self.menu_view.addSeparator()
		self.menu_view.addAction(self.action_view_reset)
		self.menu_help.addAction(self.action_help_about)
		self.menu_help.addAction(self.action_help_opengl)
		self.menu_help.addAction(self.action_help_qt)
		self.menubar.addAction(self.menu_file.menuAction())
		self.menubar.addAction(self.menu_view.menuAction())
		self.menubar.addAction(self.menu_help.menuAction())

		MainWindow.setWindowTitle(qtgui.QApplication.translate("MainWindow", "QtViewer", None, qtgui.QApplication.UnicodeUTF8))
		self.menu_file.setTitle(qtgui.QApplication.translate("MainWindow", "&File", None, qtgui.QApplication.UnicodeUTF8))
		self.menu_view.setTitle(qtgui.QApplication.translate("MainWindow", "&View", None, qtgui.QApplication.UnicodeUTF8))
		self.menu_help.setTitle(qtgui.QApplication.translate("MainWindow", "&Help", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_open.setText(qtgui.QApplication.translate("MainWindow", "&Open...", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_open.setToolTip(qtgui.QApplication.translate("MainWindow", "Open a VRML file ...", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_open.setShortcut(qtgui.QApplication.translate("MainWindow", "O", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_save.setText(qtgui.QApplication.translate("MainWindow", "&Save...", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_save.setToolTip(qtgui.QApplication.translate("MainWindow", "Save to a VRML file ...", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_save.setShortcut(qtgui.QApplication.translate("MainWindow", "S", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_check.setText(qtgui.QApplication.translate("MainWindow", "&Check", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_check.setToolTip(qtgui.QApplication.translate("MainWindow", "Check different parameters of the current mesh", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_check.setShortcut(qtgui.QApplication.translate("MainWindow", "X", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_close.setText(qtgui.QApplication.translate("MainWindow", "C&lose", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_close.setToolTip(qtgui.QApplication.translate("MainWindow", "Close the current mesh", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_close.setShortcut(qtgui.QApplication.translate("MainWindow", "W", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_quit.setText(qtgui.QApplication.translate("MainWindow", "&Quit", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_quit.setToolTip(qtgui.QApplication.translate("MainWindow", "Quit the application", None, qtgui.QApplication.UnicodeUTF8))
		self.action_file_quit.setShortcut(qtgui.QApplication.translate("MainWindow", "Esc", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_flat.setText(qtgui.QApplication.translate("MainWindow", "&Flat Shading", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_flat.setToolTip(qtgui.QApplication.translate("MainWindow", "Enable flat shading", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_flat.setShortcut(qtgui.QApplication.translate("MainWindow", "F", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_smooth.setText(qtgui.QApplication.translate("MainWindow", "&Smooth shading", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_smooth.setToolTip(qtgui.QApplication.translate("MainWindow", "Enable smooth shading", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_smooth.setShortcut(qtgui.QApplication.translate("MainWindow", "G", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_wireframe.setText(qtgui.QApplication.translate("MainWindow", "&Wireframe", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_wireframe.setToolTip(qtgui.QApplication.translate("MainWindow", "Enable wireframe rendering", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_wireframe.setShortcut(qtgui.QApplication.translate("MainWindow", "2", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_antialiasing.setText(qtgui.QApplication.translate("MainWindow", "&Antialiasing", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_antialiasing.setToolTip(qtgui.QApplication.translate("MainWindow", "Enable antialiasing", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_antialiasing.setShortcut(qtgui.QApplication.translate("MainWindow", "A", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_reset.setText(qtgui.QApplication.translate("MainWindow", "&Reset", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_reset.setToolTip(qtgui.QApplication.translate("MainWindow", "Reset the current view", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_reset.setShortcut(qtgui.QApplication.translate("MainWindow", "R", None, qtgui.QApplication.UnicodeUTF8))
		self.action_help_about.setText(qtgui.QApplication.translate("MainWindow", "&About QtViewer...", None, qtgui.QApplication.UnicodeUTF8))
		self.action_help_about.setToolTip(qtgui.QApplication.translate("MainWindow", "About this application", None, qtgui.QApplication.UnicodeUTF8))
		self.action_help_about.setShortcut(qtgui.QApplication.translate("MainWindow", "F1", None, qtgui.QApplication.UnicodeUTF8))
		self.action_help_opengl.setText(qtgui.QApplication.translate("MainWindow", "About &OpenGL...", None, qtgui.QApplication.UnicodeUTF8))
		self.action_help_opengl.setToolTip(qtgui.QApplication.translate("MainWindow", "OpenGL informations", None, qtgui.QApplication.UnicodeUTF8))
		self.action_help_opengl.setShortcut(qtgui.QApplication.translate("MainWindow", "F3", None, qtgui.QApplication.UnicodeUTF8))
		self.action_help_qt.setText(qtgui.QApplication.translate("MainWindow", "About &Qt...", None, qtgui.QApplication.UnicodeUTF8))
		self.action_help_qt.setShortcut(qtgui.QApplication.translate("MainWindow", "F2", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_hiddenlines.setText(qtgui.QApplication.translate("MainWindow", "&Hidden lines", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_hiddenlines.setToolTip(qtgui.QApplication.translate("MainWindow", "Enable wireframe rendering with hidden lines removal", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_hiddenlines.setShortcut(qtgui.QApplication.translate("MainWindow", "3", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_solid.setText(qtgui.QApplication.translate("MainWindow", "S&olid", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_solid.setToolTip(qtgui.QApplication.translate("MainWindow", "Enable solid rendering", None, qtgui.QApplication.UnicodeUTF8))
		self.action_view_solid.setShortcut(qtgui.QApplication.translate("MainWindow", "1", None, qtgui.QApplication.UnicodeUTF8))

		qtcore.QObject.connect(self.action_file_open, qtcore.SIGNAL("triggered()"), MainWindow.FileOpen)
		qtcore.QObject.connect(self.action_file_save, qtcore.SIGNAL("triggered()"), MainWindow.FileSave)
		qtcore.QObject.connect(self.action_file_quit, qtcore.SIGNAL("triggered()"), MainWindow.close)
		qtcore.QObject.connect(self.action_file_check, qtcore.SIGNAL("triggered()"), MainWindow.FileCheck)
		qtcore.QObject.connect(self.action_file_close, qtcore.SIGNAL("triggered()"), MainWindow.FileClose)
		qtcore.QObject.connect(self.action_view_flat, qtcore.SIGNAL("triggered()"), MainWindow.ViewFlat)
		qtcore.QObject.connect(self.action_view_smooth, qtcore.SIGNAL("triggered()"), MainWindow.ViewSmooth)
		qtcore.QObject.connect(self.action_view_antialiasing, qtcore.SIGNAL("triggered()"), MainWindow.ViewAntialiasing)
		qtcore.QObject.connect(self.action_view_wireframe, qtcore.SIGNAL("triggered()"), MainWindow.ViewWireframe)
		qtcore.QObject.connect(self.action_view_reset, qtcore.SIGNAL("triggered()"), MainWindow.ViewReset)
		qtcore.QObject.connect(self.action_help_about, qtcore.SIGNAL("triggered()"), MainWindow.HelpAbout)
		qtcore.QObject.connect(self.action_help_qt, qtcore.SIGNAL("triggered()"), MainWindow.HelpAboutQt)
		qtcore.QObject.connect(self.action_help_opengl, qtcore.SIGNAL("triggered()"), MainWindow.HelpAboutOpenGL)
		qtcore.QObject.connect(self.action_view_solid, qtcore.SIGNAL("triggered()"), MainWindow.ViewSolid)
		qtcore.QObject.connect(self.action_view_hiddenlines, qtcore.SIGNAL("triggered()"), MainWindow.ViewHiddenlines)
		qtcore.QMetaObject.connectSlotsByName(MainWindow)

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

