from PySide6.QtWidgets import *
from PySide6.QtCore import QEvent, QObject, Qt, Slot
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QPixmap  
from PySide6 import QtCore, QtGui

from MenuBar import MenuBar


class Header(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setLayout(QHBoxLayout())
        self.layout().setSpacing(5)
        self.layout().setContentsMargins(0,0,0,0)
        
        self.statusMessage = QLabel("Untitled")
        self.statusMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menubar = MenuBar()
        
        self.layout().addWidget(self.menubar)
        self.layout().addWidget(self.statusMessage)
        self.layout().addWidget(self.createCSD())
        
    def createCSD(self):
        minbutton = QPushButton(QIcon(":minus"), "")
        fsbutton = QPushButton(QIcon(":square"), "")
        closebutton = QPushButton(QIcon(":xmark"), "") # icon("SP_DialogCloseButton")
        
        minbutton.clicked.connect(lambda: self.window().setWindowState(Qt.WindowState.WindowMinimized))
        fsbutton.clicked.connect(lambda: self.window().setWindowState(self.window().windowState() ^ Qt.WindowState.WindowMaximized))
        closebutton.clicked.connect(lambda: self.window().close())
        
        minbutton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum))
        fsbutton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum))
        closebutton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        
        csd = QWidget()
        csd.setStyleSheet("""
                        QPushButton {
                            border-radius: 0;
                            border-left: 1px solid black;
                            padding: 3;
                            border-right: 0;
                            border-top: 0;
                        } 
                        QPushButton:pressed {
                            background-color: rgb(200, 200, 200);
                        }
                            """)
        csd.setLayout(QHBoxLayout())
        csd.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        csd.layout().setContentsMargins(0,0,0,0)
        csd.layout().setSpacing(0)
    
        csd.layout().addWidget(minbutton)
        csd.layout().addWidget(fsbutton)
        csd.layout().addWidget(closebutton)
        return csd
        
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.window().windowHandle().startSystemMove()
        return super().mousePressEvent(event)
    