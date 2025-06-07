from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTabWidget,
    QTextEdit, QPushButton, QLineEdit, QListWidget, QHBoxLayout, QFileDialog,
    QComboBox, QCheckBox, QInputDialog, QMessageBox
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtCore import Qt

from core.database import get_all_signals
from core.exporter import export_signals_to_json, export_signals_to_csv
from core.test_gpt import parse_text_with_gpt
from core.config_manager import import_config, export_config
from core.learning_prompt import analyze_channel_style
from config import CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combine Trade Bot by Kirichek")
        self.setGeometry(100, 100, 1000, 700)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.build_main_tab(), "Main")
        self.tabs.addTab(self.build_history_tab(), "History")
        self.tabs.addTab(self.build_settings_tab(), "Settings")
        self.tabs.addTab(self.build_test_tab(), "Test GPT")
        self.tabs.addTab(self.build_learning_tab(), "Learning")

        self.setCentralWidget(self.tabs)
        self.set_theme("Dark")

        self.tray = QSystemTrayIcon(QIcon("assets/icon.png"), self)
        tray_menu = self.build_tray_menu()
        self.tray.setContextMenu(tray_menu)
        self.tray.show()

    def build_main_tab(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Main Settings / Status"))
        container = QWidget()
        container.setLayout(layout)
        return container

    def build_history_tab(self):
        self.table = QListWidget()
        self.load_history()

        export_json = QPushButton("Export JSON")
        export_json.clicked.connect(lambda: export_config("export.json"))

        export_csv = QPushButton("Export CSV")
        export_csv.clicked.connect(lambda: export_signals_to_csv("signals.csv"))

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(export_json)
        layout.addWidget(export_csv)

        container = QWidget()
        container.setLayout(layout)
        return container

    def load_history(self):
        self.table.clear()
        for s in get_all_signals():
            self.table.addItem(f"{s.timestamp} | {s.channel} | {s.parsed}")

    def build_settings_tab(self):
        layout = QVBoxLayout()

        self.session_input = QLineEdit()
        browse_btn = QPushButton("Select session file")
        browse_btn.clicked.connect(self.select_session)

        self.openai_key_input = QLineEdit()
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark", "Light"])
        self.theme_selector.currentTextChanged.connect(self.set_theme)

        self.channel_list = QListWidget()
        for ch in CONFIG.telegram_channels:
            self.channel_list.addItem(ch)
        add_channel = QPushButton("Add Channel")
        remove_channel = QPushButton("Remove Channel")
        add_channel.clicked.connect(self.add_channel)
        remove_channel.clicked.connect(self.remove_channel)

        self.bot_enabled = QCheckBox("Send via Telegram Bot")
        self.bot_token = QLineEdit()
        self.bot_chat = QLineEdit()

        test_gpt_btn = QPushButton("TEST GPT Key")
        test_gpt_btn.clicked.connect(self.test_gpt_key)

        import_btn = QPushButton("Import Config")
        export_btn = QPushButton("Export Config")
        import_btn.clicked.connect(self.import_cfg)
        export_btn.clicked.connect(self.export_cfg)

        for w in [
            QLabel("Session"), self.session_input, browse_btn,
            QLabel("OpenAI Key"), self.openai_key_input,
            QLabel("Theme"), self.theme_selector,
            QLabel("Channels"), self.channel_list, add_channel, remove_channel,
            QLabel("Bot Token"), self.bot_token,
            QLabel("Chat ID"), self.bot_chat,
            self.bot_enabled, test_gpt_btn, import_btn, export_btn
        ]:
            layout.addWidget(w)

        container = QWidget()
        container.setLayout(layout)
        return container

    def build_test_tab(self):
        layout = QVBoxLayout()
        self.test_input = QTextEdit()
        self.test_output = QTextEdit()
        self.test_output.setReadOnly(True)

        test_btn = QPushButton("Run GPT Test")
        test_btn.clicked.connect(self.run_gpt_test)

        layout.addWidget(QLabel("Input Message"))
        layout.addWidget(self.test_input)
        layout.addWidget(test_btn)
        layout.addWidget(QLabel("Parsed Output"))
        layout.addWidget(self.test_output)

        container = QWidget()
        container.setLayout(layout)
        return container

    def build_learning_tab(self):
        layout = QVBoxLayout()
        self.channel_selector = QComboBox()
        self.channel_selector.addItems(CONFIG.telegram_channels)

        learn_btn = QPushButton("Прочитать стиль канала")
        self.learn_output = QTextEdit()
        self.learn_output.setReadOnly(True)

        learn_btn.clicked.connect(self.learn_channel_prompt)

        layout.addWidget(QLabel("Канал"))
        layout.addWidget(self.channel_selector)
        layout.addWidget(learn_btn)
        layout.addWidget(QLabel("GPT результат"))
        layout.addWidget(self.learn_output)

        container = QWidget()
        container.setLayout(layout)
        return container

    def run_gpt_test(self):
        text = self.test_input.toPlainText()
        result = parse_text_with_gpt(text)
        self.test_output.setPlainText(result)

    def select_session(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose .session file", "", "Session Files (*.session)")
        if path:
            self.session_input.setText(path)

    def add_channel(self):
        text, ok = QInputDialog.getText(self, "Add Channel", "Enter channel:")
        if ok:
            self.channel_list.addItem(text)

    def remove_channel(self):
        row = self.channel_list.currentRow()
        self.channel_list.takeItem(row)

    def set_theme(self, theme):
        path = f"assets/{theme.lower()}.qss"
        try:
            self.setStyleSheet(open(path).read())
        except:
            self.setStyleSheet("")

    def test_gpt_key(self):
        import openai
        openai.api_key = self.openai_key_input.text()
        try:
            res = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "ping"}]
            )
            content = res.choices[0].message.content
            QMessageBox.information(self, "GPT OK", content)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def import_cfg(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import config", "", "JSON Files (*.json)")
        if path:
            import_config(path)

    def export_cfg(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export config", "config.json", "JSON Files (*.json)")
        if path:
            export_config(path)

    def learn_channel_prompt(self):
        chan = self.channel_selector.currentText()
        result = analyze_channel_style(chan)
        self.learn_output.setPlainText(result)

    def build_tray_menu(self):
        tray_menu = self.tray.contextMenu() or QMenu()
        show_action = QAction("Показать")
        show_action.triggered.connect(self.show)
        exit_action = QAction("Выход")
        exit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(show_action)
        tray_menu.addAction(exit_action)
        return tray_menu

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray.showMessage("Combine Trade Bot", "Свернуто в трей", QSystemTrayIcon.Information)