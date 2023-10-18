#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import global_vars.vars as g
from login.window import LoginWindow
from app.window import MainWindow

# Opting out of high DPI support as it messes with my OCD when it is not perfect

# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)
# app.setAttribute(Qt.AA_UseHighDpiPixmaps)

# This is necessary since PyQT stomps over the locale settings needed by libmpv.
# This needs to happen after importing PyQT before creating the first mpv.MPV
# instance.

import locale
locale.setlocale(locale.LC_NUMERIC, 'C')

g.init()

# Assume the height of the first screen is our height
screen = app.screens()[0]
g.setScaleFactor(screen.virtualSize().height())

if g.cr_config.cookies == None:
	loginW = LoginWindow()
	loginW.show()

	print("Starting login")
	result = app.exec_()
	print("Done with login window")

	if g.crunchyroll.logged_in == False:
		print("Not logged in, exiting")
		sys.exit(result)

mainW = MainWindow()
mainW.show()

print("Starting Main window")
result = app.exec_()
print("Done with main window")

sys.exit(result)
