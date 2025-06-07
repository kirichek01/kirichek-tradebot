# Добавить в build_settings_tab() в gui.py
    def build_settings_tab(self):
        ...
        test_gpt_btn = QPushButton("TEST GPT Key")
        test_gpt_btn.clicked.connect(self.test_gpt_key)
        layout.addWidget(test_gpt_btn)
        ...

    def test_gpt_key(self):
        from openai import OpenAI
        import openai
        openai.api_key = self.openai_key_input.text()

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Test GPT connectivity"}],
                temperature=0
            )
            content = response.choices[0].message.content
            QMessageBox.information(self, "GPT Key OK", content)
        except Exception as e:
            QMessageBox.critical(self, "GPT Test Failed", str(e))