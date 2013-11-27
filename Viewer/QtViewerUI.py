# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Viewer/QtViewerUI.ui'
#
# Created: Wed Nov 27 11:15:11 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        self.central_widget = QtGui.QWidget(MainWindow)
        self.central_widget.setMouseTracking(True)
        self.central_widget.setObjectName("central_widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.central_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.opengl_widget = OpenGLWidget(self.central_widget)
        self.opengl_widget.setObjectName("opengl_widget")
        self.horizontalLayout.addWidget(self.opengl_widget)
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 30))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtGui.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_view = QtGui.QMenu(self.menubar)
        self.menu_view.setObjectName("menu_view")
        self.menu_help = QtGui.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_file_open = QtGui.QAction(MainWindow)
        self.action_file_open.setObjectName("action_file_open")
        self.action_file_save = QtGui.QAction(MainWindow)
        self.action_file_save.setObjectName("action_file_save")
        self.action_file_check = QtGui.QAction(MainWindow)
        self.action_file_check.setObjectName("action_file_check")
        self.action_file_close = QtGui.QAction(MainWindow)
        self.action_file_close.setObjectName("action_file_close")
        self.action_file_quit = QtGui.QAction(MainWindow)
        self.action_file_quit.setObjectName("action_file_quit")
        self.action_view_flat = QtGui.QAction(MainWindow)
        self.action_view_flat.setCheckable(True)
        self.action_view_flat.setChecked(False)
        self.action_view_flat.setObjectName("action_view_flat")
        self.action_view_smooth = QtGui.QAction(MainWindow)
        self.action_view_smooth.setCheckable(True)
        self.action_view_smooth.setChecked(True)
        self.action_view_smooth.setObjectName("action_view_smooth")
        self.action_view_wireframe = QtGui.QAction(MainWindow)
        self.action_view_wireframe.setCheckable(True)
        self.action_view_wireframe.setObjectName("action_view_wireframe")
        self.action_view_antialiasing = QtGui.QAction(MainWindow)
        self.action_view_antialiasing.setCheckable(True)
        self.action_view_antialiasing.setChecked(True)
        self.action_view_antialiasing.setObjectName("action_view_antialiasing")
        self.action_view_colorbar = QtGui.QAction(MainWindow)
        self.action_view_colorbar.setCheckable(True)
        self.action_view_colorbar.setObjectName("action_view_colorbar")
        self.action_view_reset = QtGui.QAction(MainWindow)
        self.action_view_reset.setObjectName("action_view_reset")
        self.action_help_about = QtGui.QAction(MainWindow)
        self.action_help_about.setObjectName("action_help_about")
        self.action_help_opengl = QtGui.QAction(MainWindow)
        self.action_help_opengl.setObjectName("action_help_opengl")
        self.action_help_qt = QtGui.QAction(MainWindow)
        self.action_help_qt.setObjectName("action_help_qt")
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
        self.menu_view.addAction(self.action_view_colorbar)
        self.menu_view.addAction(self.action_view_antialiasing)
        self.menu_view.addAction(self.action_view_wireframe)
        self.menu_view.addSeparator()
        self.menu_view.addAction(self.action_view_reset)
        self.menu_help.addAction(self.action_help_about)
        self.menu_help.addAction(self.action_help_qt)
        self.menu_help.addAction(self.action_help_opengl)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_file_open, QtCore.SIGNAL("triggered()"), MainWindow.FileOpen)
        QtCore.QObject.connect(self.action_file_save, QtCore.SIGNAL("triggered()"), MainWindow.FileSave)
        QtCore.QObject.connect(self.action_file_quit, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.action_file_check, QtCore.SIGNAL("triggered()"), MainWindow.FileCheck)
        QtCore.QObject.connect(self.action_file_close, QtCore.SIGNAL("triggered()"), MainWindow.FileClose)
        QtCore.QObject.connect(self.action_view_flat, QtCore.SIGNAL("triggered()"), MainWindow.ViewFlat)
        QtCore.QObject.connect(self.action_view_smooth, QtCore.SIGNAL("triggered()"), MainWindow.ViewSmooth)
        QtCore.QObject.connect(self.action_view_antialiasing, QtCore.SIGNAL("triggered()"), MainWindow.ViewAntialiasing)
        QtCore.QObject.connect(self.action_view_colorbar, QtCore.SIGNAL("triggered()"), MainWindow.ViewColorbar)
        QtCore.QObject.connect(self.action_view_wireframe, QtCore.SIGNAL("triggered()"), MainWindow.ViewWireframe)
        QtCore.QObject.connect(self.action_view_reset, QtCore.SIGNAL("triggered()"), MainWindow.ViewReset)
        QtCore.QObject.connect(self.action_help_about, QtCore.SIGNAL("triggered()"), MainWindow.HelpAbout)
        QtCore.QObject.connect(self.action_help_qt, QtCore.SIGNAL("triggered()"), MainWindow.HelpAboutQt)
        QtCore.QObject.connect(self.action_help_opengl, QtCore.SIGNAL("triggered()"), MainWindow.HelpAboutOpenGL)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "QtViewer", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_file.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_view.setTitle(QtGui.QApplication.translate("MainWindow", "&View", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_open.setText(QtGui.QApplication.translate("MainWindow", "&Open...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_open.setToolTip(QtGui.QApplication.translate("MainWindow", "Open a VRML file ...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_open.setShortcut(QtGui.QApplication.translate("MainWindow", "O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_save.setText(QtGui.QApplication.translate("MainWindow", "&Save...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_save.setToolTip(QtGui.QApplication.translate("MainWindow", "Save to a VRML file ...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_save.setShortcut(QtGui.QApplication.translate("MainWindow", "S", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_check.setText(QtGui.QApplication.translate("MainWindow", "&Check", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_check.setToolTip(QtGui.QApplication.translate("MainWindow", "Check different parameters of the current mesh", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_check.setShortcut(QtGui.QApplication.translate("MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_close.setText(QtGui.QApplication.translate("MainWindow", "C&lose", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_close.setToolTip(QtGui.QApplication.translate("MainWindow", "Close the current mesh", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_close.setShortcut(QtGui.QApplication.translate("MainWindow", "W", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_quit.setToolTip(QtGui.QApplication.translate("MainWindow", "Quit the application", None, QtGui.QApplication.UnicodeUTF8))
        self.action_file_quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Esc", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_flat.setText(QtGui.QApplication.translate("MainWindow", "&Flat Shading", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_flat.setToolTip(QtGui.QApplication.translate("MainWindow", "Enable flat shading", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_flat.setShortcut(QtGui.QApplication.translate("MainWindow", "F", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_smooth.setText(QtGui.QApplication.translate("MainWindow", "&Smooth shading", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_smooth.setToolTip(QtGui.QApplication.translate("MainWindow", "Enable smooth shading", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_smooth.setShortcut(QtGui.QApplication.translate("MainWindow", "G", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_wireframe.setText(QtGui.QApplication.translate("MainWindow", "&Wireframe", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_wireframe.setToolTip(QtGui.QApplication.translate("MainWindow", "Enable wireframe rendering", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_wireframe.setShortcut(QtGui.QApplication.translate("MainWindow", "D", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_antialiasing.setText(QtGui.QApplication.translate("MainWindow", "&Antialiasing", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_antialiasing.setToolTip(QtGui.QApplication.translate("MainWindow", "Enable antialiasing", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_antialiasing.setShortcut(QtGui.QApplication.translate("MainWindow", "A", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_colorbar.setText(QtGui.QApplication.translate("MainWindow", "&Color bar", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_colorbar.setToolTip(QtGui.QApplication.translate("MainWindow", "Display the color bar", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_colorbar.setShortcut(QtGui.QApplication.translate("MainWindow", "C", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_reset.setText(QtGui.QApplication.translate("MainWindow", "&Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_reset.setToolTip(QtGui.QApplication.translate("MainWindow", "Reset the current view", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_reset.setShortcut(QtGui.QApplication.translate("MainWindow", "R", None, QtGui.QApplication.UnicodeUTF8))
        self.action_help_about.setText(QtGui.QApplication.translate("MainWindow", "&About QtViewer...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_help_about.setToolTip(QtGui.QApplication.translate("MainWindow", "About this application", None, QtGui.QApplication.UnicodeUTF8))
        self.action_help_about.setShortcut(QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.action_help_opengl.setText(QtGui.QApplication.translate("MainWindow", "About &OpenGL...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_help_opengl.setToolTip(QtGui.QApplication.translate("MainWindow", "OpenGL informations", None, QtGui.QApplication.UnicodeUTF8))
        self.action_help_opengl.setShortcut(QtGui.QApplication.translate("MainWindow", "F3", None, QtGui.QApplication.UnicodeUTF8))
        self.action_help_qt.setText(QtGui.QApplication.translate("MainWindow", "About &Qt...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_help_qt.setShortcut(QtGui.QApplication.translate("MainWindow", "F2", None, QtGui.QApplication.UnicodeUTF8))

from OpenGLWidget import OpenGLWidget
