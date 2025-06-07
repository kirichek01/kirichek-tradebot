# Fragment from MainWindow class in gui.py

    def build_settings_tab(self):
        from PySide6.QtWidgets import QFileDialog, QListWidget, QHBoxLayout, QComboBox
        layout = QVBoxLayout()

        # Session file selector
        session_btn = QPushButton("Browse Session File")
        self.session_path_input = QLineEdit()
        session_btn.clicked.connect(self.select_session)

        # Theme selector
        theme_selector = QComboBox()
        theme_selector.addItems(["Dark", "Light"])
        theme_selector.currentTextChanged.connect(self.set_theme)

        # Channels editor
        self.channel_list = QListWidget()
        add_btn = QPushButton("Add Channel")
        remove_btn = QPushButton("Remove Channel")
        add_btn.clicked.connect(self.add_channel)
        remove_btn.clicked.connect(self.remove_channel)

        layout.addWidget(QLabel("Session File"))
        layout.addWidget(self.session_path_input)
        layout.addWidget(session_btn)
        layout.addWidget(QLabel("Theme"))
        layout.addWidget(theme_selector)
        layout.addWidget(QLabel("Telegram Channels"))
        layout.addWidget(self.channel_list)
        layout.addWidget(add_btn)
        layout.addWidget(remove_btn)

        container = QWidget()
        container.setLayout(layout)
        return container

    def select_session(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select .session", "", "Session Files (*.session)")
        if path:
            self.session_path_input.setText(path)

    def set_theme(self, theme):
        if theme == "Dark":
            self.setStyleSheet(open("assets/dark.qss").read())
        else:
            self.setStyleSheet(open("assets/light.qss").read())

    def add_channel(self):
        from PySide6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, "Add Channel", "Enter channel URL:")
        if ok and text:
            self.channel_list.addItem(text)

    def remove_channel(self):
        item = self.channel_list.currentItem()
        if item:
            self.channel_list.takeItem(self.channel_list.row(item))