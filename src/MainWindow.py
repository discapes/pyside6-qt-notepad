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
            left = e.pos().x()
            top = e.pos().y()
            right = self.width() - left
            bottom = self.height() - top
            delta = 15
            delta2 = delta * 2 # so corner is a bit bigger
            
            isTop = top < 30
            isBL = bottom < delta2 and left < delta2 and not (bottom > delta and left > delta)
            isBR = bottom < delta2 and right < delta2 and not (bottom > delta and right > delta)
            isLeft = not isTop and not isBL and left < delta
            isRight = not isTop and not isBR and right < delta
            isBottom = not isBR and not isBL and bottom < delta
            
            if event.type() is QEvent.Type.MouseButtonPress:
                edge = False
                if isBL: edge = Qt.Edge.BottomEdge | Qt.Edge.LeftEdge
                elif isBR: edge = Qt.Edge.BottomEdge | Qt.Edge.RightEdge
                elif isLeft: edge = Qt.Edge.LeftEdge
                elif isRight: edge = Qt.Edge.RightEdge
                elif isBottom: edge = Qt.Edge.BottomEdge
                if edge:
                    self.windowHandle().startSystemResize(edge)
                    
            if event.type() is QEvent.Type.MouseMove:
                cursor = False
                if isBL: cursor = Qt.CursorShape.SizeBDiagCursor
                elif isBR: cursor = Qt.CursorShape.SizeFDiagCursor
                elif isLeft or isRight: cursor = Qt.CursorShape.SizeHorCursor
                elif isBottom:  cursor = Qt.CursorShape.SizeVerCursor
                
                if cursor: 
                    if app.overrideCursor():
                        app.changeOverrideCursor(cursor)
                    else:
                        app.setOverrideCursor(cursor)
                else: 
                    app.restoreOverrideCursor()
                
        if isinstance(event, QtGui.QMouseEvent) and isinstance(watched, QtGui.QWindow):
            onMouseEvent(watched, event)
        return super().eventFilter(watched, event)