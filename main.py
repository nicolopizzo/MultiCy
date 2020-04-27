#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from functools import partial
from subApps.caesar import caesarFrame
from subApps.vigenere import vigenereFrame
from subApps.rsa import rsaFrame
from subApps.aes import aesFrame

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Declaring all of the widgets used
        grid = QGridLayout()

        caesarButton = QPushButton("Caesar")
        vigenereButton = QPushButton("Vigenere")
        rsaButton = QPushButton("RSA")
        aesButton = QPushButton("AES")

        grid.setSpacing(0)
        grid.setContentsMargins(0,0,0,0)

        caesarButton.clicked.connect(self.launchCaesar)
        vigenereButton.clicked.connect(self.launchVigenere)
        rsaButton.clicked.connect(self.launchRSA)
        aesButton.clicked.connect(self.launchAES)

        grid.addWidget(caesarButton, 0, 0)
        grid.addWidget(vigenereButton, 1, 0)
        grid.addWidget(rsaButton, 0, 1)
        grid.addWidget(aesButton, 1, 1)

        self.setLayout(grid)
        self.loadStyle("style/dark.qss")
        self.setFixedSize(600, 200)
        self.center()

        self.show()


    def launchCaesar(self):
        self.c = caesarFrame()
        self.c.setWindowTitle("Caesar")
        self.c.show()
        self.c.closeEvent = lambda _: self.show()

        self.hide()

    def launchVigenere(self):
        self.v = vigenereFrame()
        self.v.setWindowTitle("Vigenere")
        self.v.show()
        self.v.closeEvent = lambda _: self.show()

        self.hide()

    def launchRSA(self):
        self.r = rsaFrame()
        self.r.setWindowTitle("RSA")
        self.r.show()
        self.r.closeEvent = lambda _: self.show()

        self.hide()

    def launchAES(self):
        self.a = aesFrame()
        self.a.setWindowTitle("AES")
        self.a.show()
        self.a.closeEvent = lambda _: self.show()

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