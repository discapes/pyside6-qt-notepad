from functools import reduce
import sys
import random
from IconWidget import IconWidget

from Preferences import Preferences
from app import app
from enum import Flag
import rc_icons
from PySide6.QtWidgets import *
from PySide6.QtCore import QEvent, QObject, Qt, Slot
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QPixmap  
from PySide6 import QtCore, QtGui
from Header import Header

def icon(icon):
    return app.style().standardIcon(getattr(QStyle, icon))

class MainWidget(QWidget):
    def setup_header(self):
        header = Header()
        header.menubar.new_action.triggered.connect(self.new_file)
        header.menubar.open_action.triggered.connect(self.open_file)
        header.menubar.save_action.triggered.connect(self.save_file)
        header.menubar.pref_action.triggered.connect(self.open_pref)
        header.menubar.icon_action.triggered.connect(self.open_icons)
        return header

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(1,1,1,1)

        self.icons = IconWidget()
        self.editor = QPlainTextEdit()
        self.prefs = Preferences(self)
        
        self.layout().addWidget(self.setup_header())
        self.layout().addWidget(self.editor)
        
    @Slot()
    def open_file(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "Open file")
            if len(file_name):
                with open(file_name) as file:
                    self.file_name = file_name
                    self.editor.setPlainText(file.read())
                    self.statusMessage.setText(self.file_name)
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setText(str(e))
            msg_box.exec()

    @Slot()
    def new_file(self):
        try:
            file_name, _ = QFileDialog.getSaveFileName(self, "Open file")
            if len(file_name):
                with open(file_name, "x") as file:
                    self.file_name = file_name
                    self.statusMessage.setText(self.file_name)
                    self.editor.setPlainText("")
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setText(str(e))
            msg_box.exec()
        
    @Slot()
    def save_file(self):
        try:
            with open(self.file_name, "w") as file:
                file.write(self.editor.toPlainText())
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setText(str(e))
            msg_box.exec()


    @Slot()
    def open_icons(self):
        self.icons.setVisible(not self.icons.isVisible())
        
    @Slot()
    def open_pref(self):
        print("Opening")
        self.prefs.exec()