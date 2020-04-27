import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Crypto.Cipher import AES
from functools import partial

class aesFrame(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        vBox = QVBoxLayout()

        plainLabel = QLabel()
        plainText = QTextEdit()

        keyForm = QLineEdit()
        ivForm = QLineEdit()
        encryptButton = QPushButton()
        decryptButton = QPushButton()

        grid.setColumnStretch(0, 1)

        plainLabel.setText("Plain text")
        plainLabel.setAlignment(Qt.AlignCenter)

        keyForm.setPlaceholderText("Key")

        ivForm.setPlaceholderText("IV")

        encryptButton.setText("Encrypt")
        encryptButton.clicked.connect(partial(self.onClickEncrypt, keyForm, ivForm, plainText))
        encryptButton.setObjectName("cipher")

        decryptButton.setText("Decrypt")
        decryptButton.clicked.connect(partial(self.onClickDecrypt, keyForm, ivForm, plainText))
        decryptButton.setObjectName("cipher")

        grid.addWidget(plainLabel, 0, 0)
        grid.addWidget(plainText, 1, 0)

        vBox.addWidget(keyForm)
        vBox.addWidget(ivForm)
        vBox.addWidget(encryptButton)
        vBox.addWidget(decryptButton)
        grid.addLayout(vBox, 1, 1)

        self.setLayout(grid)
        self.loadStyle("../style/dark.qss")
        self.setFixedSize(1000, 400)

        self.center()

    def onClickEncrypt(self, kW: QLineEdit, ivW: QLineEdit, inW: QTextEdit):
        path = QFileDialog.getSaveFileName()[0]

        try:
            key = kW.text().encode()
            iv = ivW.text().encode()
            aes = AES.new(key, AES.MODE_CBC, iv)

            text = inW.toPlainText().encode()
            pad = 16 - len(text) % 16
            text = bytearray(pad) + text
            text = aes.encrypt(text)

            with open(path, "wb") as f:
                f.write(text)

            self.openDialog("Message encrypted successfully")
        
        except FileNotFoundError:
            self.openDialog("File not found. Please retry")
        
        except ValueError:
            self.openDialog("Key must hace length 16*n, n > 0 and iv must have length 16")

    def onClickDecrypt(self, kW: QLineEdit, ivW: QLineEdit, inW: QTextEdit):
        path = QFileDialog.getOpenFileName()[0]

        try:
            with open(path, "rb") as f:
                key = kW.text().encode()
                iv = ivW.text().encode()
                aes = AES.new(key, AES.MODE_CBC, iv)

                text = f.read()
                text = aes.decrypt(text).decode()

                inW.setText(text)

                self.openDialog("Message decrypted")
        
        except FileNotFoundError:
            self.openDialog("File not found. Please retry")

        except ValueError:
            self.openDialog("Key must hace length 16*n, n > 0 and iv must have length 16")

    def openDialog(self, msg):
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

    def center(self):
        qr = self.frameGeometry()

        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())