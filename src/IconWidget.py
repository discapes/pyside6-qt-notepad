from PySide6.QtWidgets import *
from PySide6.QtCore import QEvent, QObject, Qt, Slot
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QPixmap  
from PySide6 import QtCore, QtGui
from app import app


class IconWidget(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
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
            btn.clicked.connect((lambda name: lambda: app.clipboard().setText(name))(name))
            layout.addWidget(btn, n / 4, n % 4)

        self.setWidget(widget)