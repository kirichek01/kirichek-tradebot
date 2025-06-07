# Вставить в MainWindow в gui.py
    def build_test_tab(self):
        from PySide6.QtWidgets import QTextEdit
        layout = QVBoxLayout()
        self.test_input = QTextEdit()
        self.test_output = QTextEdit()
        self.test_output.setReadOnly(True)

        test_btn = QPushButton("Test GPT")
        test_btn.clicked.connect(self.run_gpt_test)

        layout.addWidget(QLabel("Input Message"))
        layout.addWidget(self.test_input)
        layout.addWidget(test_btn)
        layout.addWidget(QLabel("Parsed Output"))
        layout.addWidget(self.test_output)

        container = QWidget()
        container.setLayout(layout)
        return container

    def run_gpt_test(self):
        from core.test_gpt import parse_text_with_gpt
        text = self.test_input.toPlainText()
        result = parse_text_with_gpt(text)
        self.test_output.setPlainText(result)