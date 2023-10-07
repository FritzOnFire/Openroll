from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import global_vars.vars as g

class WatchList:
	def __init__(self, layout: QBoxLayout):
		layout.addWidget(self.createTitleWidget())
		layout.addStretch(1)

		self.list_widget = QWidget()
		self.list_layout = QVBoxLayout(self.list_widget)

		layout.addWidget(self.list_widget)
		layout.addStretch(1)

	def createTitleWidget(self):
		title_widget = QWidget()
		title_layout = QHBoxLayout(title_widget)

		# Add list.svg in front of the title
		title_icon = QLabel(title_widget)
		title_icon.setPixmap(QPixmap('assets/list.svg'))
		title_icon.setScaledContents(True)
		title_icon.setMaximumSize(32, 32)
		title_layout.addWidget(title_icon)

		self.title_label = QLabel('My List')
		self.title_label.setStyleSheet("""
			QLabel {
				color: #ffffff;
				font-size: 34px;
				font-weight: 500;
				max-height: 62px;
				min-height: 62px;
			}
		""")
		title_layout.addWidget(self.title_label)
		title_layout.addStretch(1)
		return title_widget

	def createListWidget(self):
		try:
			watchList = g.crunchyroll.retriveWatchList()
		except Exception as e:
			print(e)
			return
		print(watchList)
