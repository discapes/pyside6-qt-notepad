import sys
from MainWindow import MainWindow

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QCommandLineParser
from PySide6.QtGui import QCloseEvent
from app import app

def parse(app):
    parser = QCommandLineParser()
    parser.addHelpOption()
    parser.addVersionOption()
    parser.process(app)

if __name__ == "__main__":
    app.setStyle("Fusion")

    app.setStyleSheet("""
                    QMainWindow, QDialog {
                        /*background-color: darkgray;*/
                        border: 1px solid black;
                    }
                    QMenuBar {
                        border: 0px;
                    }
                    QPlainTextEdit {
                        border: 0;
                    }
                    /*QWidget {
                        margin: 0;
                        padding: 0;
                        spacing: 0;                        
                    }*/
                    QPushButton {
                        padding: 3px 5px;
                    }
                      """)
    app.setApplicationName("My Application")
    app.setApplicationVersion("1.0")
    parse(app)

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
