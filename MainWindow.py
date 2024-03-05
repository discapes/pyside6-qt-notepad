import sys
import random

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QIcon, QPixmap
from Preferences import Preferences
from app import app
import rc_icons

def icon(icon):
    return app.style().standardIcon(getattr(QStyle, icon))

    

class IconWidget(QScrollArea):
    def __init__(self):
        super().__init__()

        icons = sorted(
            [attr for attr in dir(QStyle.StandardPixmap) if attr.startswith("SP_")]
        )
        layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(layout)

        for n, name in enumerate(icons):
            btn = QPushButton(name)

            pixmapi = getattr(QStyle, name)
            icon = self.style().standardIcon(pixmapi)
            btn.setIcon(icon)
            layout.addWidget(btn, n / 4, n % 4)

        self.setWidget(widget)

class MainWindow(QMainWindow):
    def file_menu(self):
        file_menu = self.menuBar().addMenu("&File")
        file_menu.setToolTipsVisible(True)
        
        new_action = QAction("&New", self)
        new_action.triggered.connect(self.new_file)
        open_action = QAction("&Open", self)
        open_action.triggered.connect(self.open_file)
        save_action = QAction("&Save", self)
        save_action.triggered.connect(self.save_file)
       
       
        icon_action = QAction("&Icons", self)
        icon_action.triggered.connect(self.open_icons)
        icon_action.setStatusTip("Open icon list")
        
        file_menu.addActions([icon_action, new_action, open_action, save_action])
        
    def edit_menu(self):
        edit = self.menuBar().addMenu("&Edit")
        undo = QAction("&Undo", self)
        self.editor.undoAvailable.connect(print)
        def undo_fn():
            print("Undo")
            self.editor.undo()
        undo.triggered.connect(undo_fn)
        redo = QAction("&Redo", self)
        undo.triggered.connect(self.editor.redo)
        preferences = QAction(QIcon(":gear"),"&Preferences", self)
        preferences.triggered.connect(self.open_pref)
        edit.addActions([undo, redo, preferences])
        
    def view_menu(self):
        view = self.menuBar().addMenu("&View")
        undo = QAction("&Undo", self)
        redo = QAction("&Redo", self)
        view.addActions([undo, redo])

    def help_menu(self):
        help = self.menuBar().addMenu("&Help")
        undo = QAction("&Undo", self)
        redo = QAction("&Redo", self)
        help.addActions([undo, redo])

    def setup_menubar(self):
        pref_action = QAction(self)
        pref_action.setIcon(QIcon(":gear"))
        pref_action.triggered.connect(self.open_pref)
        self.menuBar().addAction(pref_action)
        
        self.file_menu()
        self.edit_menu()
        self.view_menu()
        self.help_menu()


    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        self.icons = IconWidget()
        self.editor = QPlainTextEdit()
        self.prefs = Preferences(self)
        self.statusMessage = QLabel()
        
        self.setup_menubar()


        self.setWindowTitle("Editor")
        app.setWindowIcon(QIcon(":pen"))
        layout.addWidget(self.editor)
        self.setCentralWidget(widget)
        
        self.statusBar().addWidget(self.statusMessage)
        
        self.icons.setVisible(False)


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