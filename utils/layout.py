from PyQt5.QtWidgets import *

def cleanLayout(layout: QBoxLayout):
	for i in reversed(range(layout.count())):
		layout.itemAt(i).widget().setParent(None)
