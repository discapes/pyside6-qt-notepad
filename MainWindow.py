import sys
import random

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QIcon, QPixmap
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
        new_action.setStatusTip("Open new file")
        new_action.setToolTip("Open new file")
        new_action.triggered.connect(self.magic)
        icon_action = QAction("&Icons", self)
        icon_action.triggered.connect(self.open_icons)
        icon_action.setStatusTip("Open icon list")
        file_menu.addActions([icon_action, new_action])
        
    def view_menu(self):
        view_menu = self.menuBar().addMenu("&Edit")
        undo = QAction("&Undo", self)
        redo = QAction("&Redo", self)
        view_menu.addActions([undo, redo])
        

    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.statusBar()

        self.hello = ["Hello World", "Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.i = 0
        
        pref_action = QAction(self)
        pref_action.setIcon(QIcon(":gear"))
        self.menuBar().addAction(pref_action)
        
        self.file_menu()
        self.view_menu()

        self.button = QPushButton("Click me!")
        self.button2 = QPushButton("Click meeee!")
        self.button2.clicked.connect(self.open_file)
        self.text = QLabel(self.hello[self.i],
                                     alignment=Qt.AlignCenter)
        
        self.bbar = QHBoxLayout()
        self.bbar.addWidget(self.button)
        self.bbar.addWidget(self.button2)
        self.line = QLineEdit()
        self.line.setPlaceholderText("asd")
        self.bbar.addWidget(self.line)
        self.bbar.setSpacing(50)
        self.bbar.setAlignment(Qt.AlignmentFlag.AlignJustify | Qt.AlignmentFlag.AlignVCenter)


        self.setWindowTitle("Window title")
        self.setWindowIcon(QIcon())
        layout.addWidget(self.text)
        layout.addLayout(self.bbar)
        self.setCentralWidget(widget)
        self.l = layout
        #self.setWindowState(Qt.WindowState.WindowFullScreen)
        #self.setWindowState(Qt.WindowState.WindowMaximized)
        self.icons = getattr(self, "icons", IconWidget())
        self.l.addWidget(self.icons)
        self.icons.setVisible(False)

        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self):
        self.i = (self.i + 1) % len(self.hello)
        self.text.setText(self.hello[self.i])

    @Slot()
    def open_file(self):
        file = QFileDialog.getOpenFileName(self, "Open file")

    @Slot()
    def open_icons(self):
        self.icons.setVisible(not self.icons.isVisible())
        
    @Slot()
    def open_pref(self):
        self.icons.setVisible(not self.icons.isVisible())