import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from functools import partial

class rsaFrame(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        centralGrid = QGridLayout()

        inLabel = QLabel()
        inText = QTextEdit()

        debugLabel = QLabel()
        loadPemButton = QPushButton()
        savePemButton = QPushButton()
        generateKeyButton = QPushButton()
        encryptButton = QPushButton()
        decryptButton = QPushButton()

        outLabel = QLabel()
        outText = QTextBrowser()

        grid.setSpacing(10)
        grid.setColumnStretch(0, 100)
        
        centralGrid.setSpacing(10)

        inLabel.setText("Plain text")
        inLabel.setAlignment(Qt.AlignCenter)

        debugLabel.setText("You have no PEM key")
        debugLabel.setAlignment(Qt.AlignCenter)
        debugLabel.setStyleSheet("color: red")

        loadPemButton.setText("Load PEM key")
        loadPemButton.clicked.connect(partial(self.onClickLoad, debugLabel))
        loadPemButton.setObjectName("little")

        savePemButton.setText("Save PEM key")
        savePemButton.clicked.connect(self.onClickSave)
        savePemButton.setObjectName("little")

        generateKeyButton.setText("Generate PEM key")
        generateKeyButton.clicked.connect(partial(self.onClickGenerate, debugLabel))
        generateKeyButton.setObjectName("little")

        encryptButton.setText("Encrypt")
        encryptButton.clicked.connect(partial(self.onClickEncrypt, inText))
        encryptButton.setObjectName("little")

        decryptButton.setText("Decrypt")
        decryptButton.clicked.connect(partial(self.onClickDecrypt, inText))
        decryptButton.setObjectName("little")

        grid.addWidget(inLabel, 0, 0)
        grid.addWidget(inText, 1, 0)

        centralGrid.addWidget(loadPemButton, 0, 0)
        centralGrid.addWidget(savePemButton, 0, 1)
        centralGrid.addWidget(generateKeyButton, 1, 0, 1, -1)
        centralGrid.addWidget(encryptButton, 2, 0, 2, -1)
        centralGrid.addWidget(decryptButton, 4, 0, 4, -1)

        grid.addWidget(debugLabel, 0, 1)
        grid.addLayout(centralGrid, 1, 1)

        self.setLayout(grid)
        self.loadStyle("../style/dark.qss")
        self.setFixedSize(1000, 400)

        self.center()

    def onClickLoad(self, debugLabel: QLabel):
        path = QFileDialog.getOpenFileName()[0]
        filename = path.split("/")[-1]

        try:
            with open(path, "r") as f:
                try:
                    self.keyPair = RSA.importKey(f.read())  
                    debugLabel.setText("PEM key is loaded ("+filename+")")
                    debugLabel.setStyleSheet("color: green")
                except ValueError:
                    self.openDialog("The file selected is not supported.")

        except FileNotFoundError:
            self.openDialog("File not found. Retry")

    def onClickSave(self):
        path = QFileDialog.getSaveFileName()[0]
        if not path.endswith(".pem"):
            path += ".pem"

        with open(path, "w") as f:
            try:
                k = self.keyPair.exportKey()
                f.write(k.decode())
                self.openDialog("Key saved successfully")
            except AttributeError:
                self.openDialog("You have no key loaded")

    def onClickGenerate(self, label: QLabel):
        self.keyPair = RSA.generate(2048)

        label.setText("You have generated a key")
        label.setStyleSheet("color: green")

    def onClickEncrypt(self, inW: QTextEdit):
        text = inW.toPlainText()

        try:
            encrypter = PKCS1_OAEP.new(self.keyPair)
            text = encrypter.encrypt(text.encode())
            path = QFileDialog.getSaveFileName()[0]
            with open(path, "wb") as f:
                f.write(text)
            self.openDialog("Text encrypted correctly in " + path)

        except AttributeError:
            self.openDialog("You have no PEM key")


    def onClickDecrypt(self, inW: QTextEdit):
        try:
            path = QFileDialog.getOpenFileName()[0]
            decrypter = PKCS1_OAEP.new(self.keyPair)
            with open(path, "rb") as f:
                text = decrypter.decrypt(f.read())
                inW.setText(text.decode())
            self.openDialog("File decrypted correctly.")

        except AttributeError:
            self.openDialog("You have no PEM key")
            
        except ValueError:
            self.openDialog("The key you loaded is not correct for the file chosen. Choose the correct key")


    def openDialog(self, msg):
        dialog = QMessageBox()
        dialog.setText(msg)

        dialog.show()
        dialog.exec_()

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