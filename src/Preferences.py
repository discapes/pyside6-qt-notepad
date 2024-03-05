
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QIcon, QPixmap

from Header import Header

class Preferences(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        contentLayout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Preferences")
        layout.setContentsMargins(0,0,0,0)
        contentLayout.setContentsMargins(10,10,10,10)
        header = Header(False)
        header.statusMessage.setText("Preferences")

        self.button = QPushButton("Click me!")
        self.button2 = QPushButton("Click meeee!")
       # self.button2.clicked.connect(self.open_file)
       # self.text = QLabel(self.hello[self.i],
       #                              alignment=Qt.AlignCenter)
        
        self.bbar = QHBoxLayout()
        self.bbar.addWidget(self.button)
        self.bbar.addWidget(self.button2)
        self.line = QLineEdit()
        self.line.setPlaceholderText("asd")
        self.bbar.addWidget(self.line)
        self.bbar.setSpacing(50)
        self.bbar.setAlignment(Qt.AlignmentFlag.AlignJustify | Qt.AlignmentFlag.AlignVCenter)
        
        layout.addWidget(header)
        layout.addLayout(contentLayout)
        contentLayout.addWidget(self.line)
        contentLayout.addLayout(self.bbar)
        