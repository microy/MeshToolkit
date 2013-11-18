#! /usr/bin/env python

from Viewer.QtViewer import *
import sys


if __name__ == "__main__":

	app = QtGui.QApplication( sys.argv )
	window = QtViewer()
	window.show()
	sys.exit( app.exec_() )

