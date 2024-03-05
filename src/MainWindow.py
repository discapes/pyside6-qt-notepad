from functools import reduce
from PySide6.QtWidgets import *
from PySide6.QtCore import QEvent, QObject, Qt, Slot
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QPixmap  
from PySide6 import QtCore, QtGui
from MainWidget import MainWidget
from app import app

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        app.installEventFilter(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Editor")
        app.setWindowIcon(QIcon(":pen"))

    
    def closeEvent(self, event: QCloseEvent):
        app.closeAllWindows()
        return super().closeEvent(event)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        #print(event)
        return super().resizeEvent(event)
    
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        def onMouseEvent(watched: QObject, e: QtGui.QMouseEvent):
            x = e.pos().x() / self.width()
            y = e.pos().y() / self.height()
            delta = 0.02
            
            if event.type() is QEvent.Type.MouseButtonPress:
                edges = []
                if x < delta and y > 0.1: edges.append(Qt.Edge.LeftEdge)
                if x > 1 - delta and y > 0.1: edges.append(Qt.Edge.RightEdge)
                if y > 1 - delta: edges.append(Qt.Edge.BottomEdge)
                if len(edges):
                    self.windowHandle().startSystemResize(reduce(lambda x, y: x | y, edges))
                    
            if event.type() is QEvent.Type.MouseMove:
                cursor = False
                if x < delta and y > 1 - delta: cursor = Qt.CursorShape.SizeBDiagCursor
                elif x > 1 - delta and y > 1 - delta: cursor = Qt.CursorShape.SizeFDiagCursor
                elif (x < delta or x > 1 - delta) and y > 0.1: cursor = Qt.CursorShape.SizeHorCursor
                elif y > 1 - delta:  cursor = Qt.CursorShape.SizeVerCursor
                
                if cursor: 
                    app.setOverrideCursor(cursor)
                else: 
                    app.restoreOverrideCursor() # needed twice for some reason
                    app.restoreOverrideCursor()
                
        if isinstance(event, QtGui.QMouseEvent) and isinstance(watched, QtGui.QWindow):
            onMouseEvent(watched, event)
        return super().eventFilter(watched, event)