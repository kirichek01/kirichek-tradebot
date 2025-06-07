from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from telethon import TelegramClient
from config import CONFIG

class AuthDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Login")
        self.setMinimumWidth(300)

        self.layout = QVBoxLayout()
        self.label = QLabel("Enter your phone number:")
        self.input = QLineEdit()
        self.button = QPushButton("Next")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.step = "phone"
        self.button.clicked.connect(self.handle_step)

    def handle_step(self):
        if self.step == "phone":
            self.phone = self.input.text()
            self.label.setText("Enter the code from Telegram:")
            self.input.setText("")
            self.step = "code"
        elif self.step == "code":
            self.code = self.input.text()
            self.label.setText("Enter 2FA password (if any), or leave blank:")
            self.input.setText("")
            self.step = "2fa"
        elif self.step == "2fa":
            self.password = self.input.text()
            self.accept()

    def get_auth_data(self):
        return self.phone, self.code, self.password