import sys
from MainWindow import MainWindow

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QCommandLineParser
from app import app

def parse(app):
    parser = QCommandLineParser()
    parser.addHelpOption()
    parser.addVersionOption()
    parser.process(app)

if __name__ == "__main__":
    app.setStyle("Fusion")
    app.setApplicationName("My Application")
    app.setApplicationVersion("1.0")
    parse(app)

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
