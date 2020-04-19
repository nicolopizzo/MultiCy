#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from functools import partial
from subApps.caesar import caesarFrame
from subApps.vigenere import vigenereFrame

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Declaring all of the widgets used
        basicBox = QVBoxLayout()
        caesarButton = QPushButton("Caesar")
        vigenereButton = QPushButton("Vigenere")

        basicBox.setSpacing(10)

        caesarButton.clicked.connect(self.launchCaesar)
        vigenereButton.clicked.connect(self.launchVigenere)

        basicBox.addWidget(caesarButton)
        basicBox.addWidget(vigenereButton)

        self.setLayout(basicBox)
        self.loadStyle()
        self.center()
        self.show()

    def launchCaesar(self):
        self.c = caesarFrame()
        self.c.setWindowTitle("Caesar")
        self.c.show()

        self.hide()

    def launchVigenere(self):
        self.v = vigenereFrame()
        self.v.show()

        self.hide()

    def center(self):
        qr = self.frameGeometry()

        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadStyle(self, path="style/default.qss"):
        with open(path, "r") as styleSheet:
            style = styleSheet.read()
            self.setStyleSheet(style)


def main():
    app = QApplication(sys.argv)

    window = mainWindow()
    window.setWindowTitle("MultiCy")
    window.resize(400, 200)

    app.exec_()

if __name__ == "__main__":
    main()