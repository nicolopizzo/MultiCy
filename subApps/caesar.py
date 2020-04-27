import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from functools import partial

class caesarFrame(QWidget):
    def __init__(self):
        super().__init__()

        # Declaring layouts and widgets
        grid = QGridLayout()
        centralGrid = QGridLayout()

        inLabel = QLabel()
        inText = QTextEdit()

        rotBox = QSpinBox()
        encryptButton = QPushButton()
        decryptButton = QPushButton()

        outLabel = QLabel()
        outText = QTextBrowser()

        # Grid settings
        grid.setSpacing(10)
        centralGrid.setSpacing(0)

        # Setting input
        inLabel.setText("Input text")
        inLabel.setAlignment(Qt.AlignCenter)

        # Setting the central interactive part
        rotBox.setRange(1, 25)

        encryptButton.setText("Encrypt")
        encryptButton.clicked.connect(partial(self.onClickEncrypt, rotBox, inText, outText))
        encryptButton.setObjectName("cipher")

        decryptButton.setText("Decrypt")
        decryptButton.clicked.connect(partial(self.onClickDecrypt, rotBox, inText, outText))
        decryptButton.setObjectName("cipher")

        # Setting Output
        outLabel.setText("Output text")
        outLabel.setAlignment(Qt.AlignCenter)

        # Add the widgets and layout to grid
        grid.addWidget(inLabel, 0, 0)
        grid.addWidget(inText, 1, 0)

        grid.addWidget(rotBox, 0, 1)
        
        centralGrid.addWidget(encryptButton, 0, 0)
        centralGrid.addWidget(decryptButton, 1, 0)
        grid.addLayout(centralGrid, 1, 1)

        grid.addWidget(outLabel, 0, 2)
        grid.addWidget(outText, 1, 2)

        # Set layout in the widget
        self.setLayout(grid)
        self.loadStyle("../style/dark.qss")
        self.setFixedSize(1000, 400)
        
        self.center()

    def onClickEncrypt(self, rotBox: QSpinBox, inW: QTextEdit, outW: QTextBrowser):
        rot = int(rotBox.text())
        text = inW.toPlainText()
        text = self.caesarEncrypt(text, rot)
        outW.setText(text)

    def onClickDecrypt(self, rotBox: QSpinBox,  inW: QTextEdit, outW: QTextBrowser):
        rot = int(rotBox.text())
        text = inW.toPlainText()
        text = self.caesarEncrypt(text, -rot)
        outW.setText(text)

    def caesarEncrypt(self, s: str, rot: int):
        res = ""

        for ch in s:
            if ch.isupper():
                tmp = ord('A') + (ord(ch) - ord('A') + rot)%26
                tmp = chr(tmp)
                res += tmp

            elif ch.islower():
                tmp = ord('a') + (ord(ch) - ord('a') + rot)%26
                tmp = chr(tmp)
                res += tmp
            
            else:
                res += ch

        return res

    def center(self):
        qr = self.frameGeometry()

        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadStyle(self, path="../style/default.qss"):
        curDir = os.path.dirname(__file__)
        path = os.path.join(curDir, path)
        with open(path, "r") as styleSheet:
            style = styleSheet.read()
            self.setStyleSheet(style)