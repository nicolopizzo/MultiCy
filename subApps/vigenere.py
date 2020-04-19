import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from functools import partial

class vigenereFrame(QWidget):
    def __init__(self):
        super().__init__()

        # Declaring layouts and widgets
        grid = QGridLayout()
        centralVbox = QVBoxLayout()

        inLabel = QLabel()
        inText = QTextEdit()

        inKey = QLineEdit()
        encryptButton = QPushButton()
        decryptButton = QPushButton()

        outLabel = QLabel()
        outText = QTextBrowser()

        # Setting input
        inLabel.setText("Input text")
        inLabel.setAlignment(Qt.AlignCenter)

        # Setting central interactive part
        inKey.setText("Enter the key...")

        encryptButton.setText("Encrypt")
        encryptButton.clicked.connect(partial(self.onClickEncrypt, inKey, inText, outText))

        decryptButton.setText("Decrypt")
        decryptButton.clicked.connect(partial(self.onClickDecrypt, inKey, inText, outText))

        # Setting output
        outLabel.setText("Outpute text")
        outLabel.setAlignment(Qt.AlignCenter)

        # Setting grid
        grid.addWidget(inLabel, 0, 0)
        grid.addWidget(inText, 1, 0)

        centralVbox.addWidget(inKey)
        centralVbox.addWidget(encryptButton)
        centralVbox.addWidget(decryptButton)
        grid.addLayout(centralVbox, 1, 1)

        grid.addWidget(outLabel, 0, 2)
        grid.addWidget(outText, 1, 2)

        # Final setting to self
        self.setLayout(grid)
        self.loadStyle()
        self.center()

    def center(self):
        qr = self.frameGeometry()

        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openErrorDialog(self, msg):
        dialog = QMessageBox()
        dialog.setText(msg)

        dialog.show()
        dialog.exec_()

    def loadStyle(self, path="../style/default.qss"):
        curDir = os.path.dirname(__file__)
        path = os.path.join(curDir, path)
        with open(path, "r") as styleSheet:
            style = styleSheet.read()
            self.setStyleSheet(style)

    def onClickEncrypt(self, keyW: QLineEdit, inW: QTextEdit, outW: QTextBrowser):
        text = inW.toPlainText()
        key = keyW.text()
        if not text.isupper() or not key.isupper():
            self.openErrorDialog("Text and key must be in uppercase. Please retry")
        else:
            text = self.vigenereEncrypt(text, key)
            outW.setText(text)

    def onClickDecrypt(self, keyW: QLineEdit, inW: QTextEdit, outW: QTextBrowser):
        text = inW.toPlainText()
        key = keyW.text()

        if not text.isupper() or not key.isupper():
            self.openErrorDialog("Text and key must be in uppercase. Please retry")

        else:
            text = self.vigenereEncrypt(text, key, lambda a, b: b - a + 26)
            outW.setText(text)

    def vigenereEncrypt(self, s, k, f=lambda a, b: a + b):
        res = ""
        s = ''.join(s.split())
        for i in range(len(s)):
            if s[i].isupper():
                a = ord(k[i % len(k)]) - ord('A')
                b = ord(s[i]) - ord('A')

                n = f(a, b)
                r = n//26

                offset = n - (26*r)
                res += chr(ord('A') + offset)

            else:
                res += s[i]

        return res