#! /usr/bin/env python
# -*- coding:utf-8 -*- 


from Viewer.QtViewer import QtViewer
from PyQt4 import QtGui
import sys



if __name__ == "__main__" :

	app = QtGui.QApplication( sys.argv )
	window = QtViewer()
	window.show()
	sys.exit( app.exec_() )

