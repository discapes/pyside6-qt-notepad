from PySide6.QtWidgets import *
from PySide6.QtCore import QEvent, QObject, Qt, Slot
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QPixmap  
from PySide6 import QtCore, QtGui

class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.pref_action = QAction(self)
        self.pref_action.setIcon(QIcon(":gear"))
#        self.addAction(self.pref_action)
        
        self.file_menu()
        self.edit_menu()
        self.view_menu()
        self.help_menu()

    def file_menu(self):
        file_menu = self.addMenu("&File")
        self.new_action = QAction("&New", self)
        self.open_action = QAction("&Open", self)
        self.save_action = QAction("&Save", self)
        self.icon_action = QAction("&Icons", self)
        file_menu.addActions([self.icon_action, self.new_action, self.open_action, self.save_action])
        
    def edit_menu(self):
        edit = self.addMenu("&Edit")
        pref_action = QAction(QIcon(":gear"),"&Preferences", self)
        pref_action.triggered.connect(self.pref_action.trigger)
        edit.addActions([pref_action])
        
    def view_menu(self):
        view = self.addMenu("&View")

    def help_menu(self):
        help = self.addMenu("&Help")
        self.about_action = QAction("&About", self)
        help.addActions([self.about_action])