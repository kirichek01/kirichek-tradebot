# Добавить блок в Settings или отдельную вкладку
    def build_learning_tab(self):
        layout = QVBoxLayout()
        self.channel_selector = QComboBox()
        self.channel_selector.addItems(CONFIG.telegram_channels)

        learn_btn = QPushButton("Прочитать стиль канала")
        self.learn_output = QTextEdit()
        self.learn_output.setReadOnly(True)

        learn_btn.clicked.connect(self.learn_channel_prompt)

        layout.addWidget(QLabel("Выберите канал"))
        layout.addWidget(self.channel_selector)
        layout.addWidget(learn_btn)
        layout.addWidget(QLabel("Результат GPT"))
        layout.addWidget(self.learn_output)

        container = QWidget()
        container.setLayout(layout)
        return container

    def learn_channel_prompt(self):
        from core.learning_prompt import analyze_channel_style
        chan = self.channel_selector.currentText()
        result = analyze_channel_style(chan)
        self.learn_output.setPlainText(result)