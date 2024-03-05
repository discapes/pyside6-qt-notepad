import sys
import random

from PySide6.QtWidgets import *
from PySide6.QtCore import QEvent, QObject, Qt, Slot
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QPixmap  
from Preferences import Preferences
from PySide6 import QtCore, QtGui
from app import app
import rc_icons

def icon(icon):
    return app.style().standardIcon(getattr(QStyle, icon))

    

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
        
class TopBar(QWidget):
    def __init__(self, window: QMainWindow):
        super().__init__()
        self._window = window
        
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.window().windowHandle().startSystemMove()
        return super().mousePressEvent(event)

class MainWindow(QMainWindow):
    def closeEvent(self, event: QCloseEvent):
        app.closeAllWindows()
        return super().closeEvent(event)
    
    def file_menu(self):
        file_menu = self.menu_bar.addMenu("&File")
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
        edit = self.menu_bar.addMenu("&Edit")
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
        view = self.menu_bar.addMenu("&View")
        undo = QAction("&Undo", self)
        redo = QAction("&Redo", self)
        view.addActions([undo, redo])

    def help_menu(self):
        help = self.menu_bar.addMenu("&Help")
        undo = QAction("&Undo", self)
        redo = QAction("&Redo", self)
        help.addActions([undo, redo])

    def setup_menubar(self):
        pref_action = QAction(self)
        pref_action.setIcon(QIcon(":gear"))
        pref_action.triggered.connect(self.open_pref)
        self.menu_bar.addAction(pref_action)
        
        self.file_menu()
        self.edit_menu()
        self.view_menu()
        self.help_menu()


    def __init__(self):
        super().__init__()
        self.menu_bar = QMenuBar()
        widget = QWidget()
        layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        widget.setLayout(layout)
        topbar = TopBar(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        
        self.menu_bar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        
        self.icons = IconWidget()
        self.editor = QPlainTextEdit()
        self.prefs = Preferences(self)
        self.statusMessage = QLabel("Untitled")
        self.statusMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.setup_menubar()


        self.setWindowTitle("Editor")
        app.setWindowIcon(QIcon(":pen"))
        self.csd = QHBoxLayout()
        topbar.setLayout(self.top_layout)
        layout.addWidget(topbar)
        mblayout = QHBoxLayout()
        mblayout.addWidget(self.menu_bar)
        self.top_layout.setSpacing(5)
        self.top_layout.setContentsMargins(0,0,0,0)
        
        
        mblayout.setContentsMargins(0, 3, 0, 0)
        self.top_layout.addLayout(mblayout)
        self.top_layout.addWidget(self.statusMessage)
        self.top_layout.addLayout(self.csd)
        
        closebutton = QPushButton(icon("SP_DialogCloseButton"), "")
        closebutton.setStyleSheet("""
                                QPushButton {
                                    border-radius: 0;
                                    border-left: 1px solid black;
                                    border-right: 0;
                                    border-top: 0;
                                } 
                                QPushButton:pressed {
                                    background-color: rgb(224, 0, 0);
                                }
                                  """)
        closebutton.clicked.connect(self.close)
        closebutton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.top_layout.addWidget(closebutton)
        layout.addWidget(self.editor)
        layout.setSpacing(0)
        layout.setContentsMargins(1,1,1,1)
        self.setCentralWidget(widget)
        
        #self.statusBar().addWidget(self.statusMessage)
        app.installEventFilter(self)
        
        self.icons.setVisible(False)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
      #  print(event)
        def onMouseEvent(watched: QObject, e: QtGui.QMouseEvent):
            print(e.isEndEvent())
            print(watched)
        if isinstance(event, QtGui.QMouseEvent) and event.type() is QEvent.Type.MouseButtonPress:
            onMouseEvent(watched, event)
        return super().eventFilter(watched, event)


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