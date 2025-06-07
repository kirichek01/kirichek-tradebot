# Добавить в Settings вкладку GUI
    def build_bot_settings(self):
        layout = QVBoxLayout()

        self.bot_enabled = QCheckBox("Send Signals via Telegram Bot")
        self.bot_token_input = QLineEdit()
        self.bot_chat_id_input = QLineEdit()

        layout.addWidget(self.bot_enabled)
        layout.addWidget(QLabel("Bot Token"))
        layout.addWidget(self.bot_token_input)
        layout.addWidget(QLabel("Target Chat ID"))
        layout.addWidget(self.bot_chat_id_input)

        container = QWidget()
        container.setLayout(layout)
        return container

    def get_bot_settings(self):
        return {
            "enabled": self.bot_enabled.isChecked(),
            "token": self.bot_token_input.text(),
            "chat_id": self.bot_chat_id_input.text()
        }