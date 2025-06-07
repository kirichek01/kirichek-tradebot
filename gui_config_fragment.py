# Вставить в build_settings_tab() в gui.py
    def build_settings_tab(self):
        ...
        import_btn = QPushButton("Import Config")
        export_btn = QPushButton("Export Config")
        import_btn.clicked.connect(self.import_config)
        export_btn.clicked.connect(self.export_config)
        layout.addWidget(import_btn)
        layout.addWidget(export_btn)
        ...

    def import_config(self):
        from PySide6.QtWidgets import QFileDialog
        from core.config_manager import import_config
        path, _ = QFileDialog.getOpenFileName(self, "Import Config", "", "JSON Files (*.json)")
        if path:
            import_config(path)
            QMessageBox.information(self, "Config Imported", "Settings have been applied. Restart may be required.")

    def export_config(self):
        from PySide6.QtWidgets import QFileDialog
        from core.config_manager import export_config
        path, _ = QFileDialog.getSaveFileName(self, "Export Config", "config.json", "JSON Files (*.json)")
        if path:
            export_config(path)
            QMessageBox.information(self, "Config Exported", f"Saved to {path}")