# Добавить в MainWindow.__init__
from PySide6.QtGui import QIcon, QSystemTrayIcon, QMenu, QAction

        self.tray = QSystemTrayIcon(QIcon("assets/icon.png"), self)
        tray_menu = QMenu()

        show_action = QAction("Show")
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        quit_action = QAction("Exit")
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)

        self.tray.setContextMenu(tray_menu)
        self.tray.setToolTip("Combine Trade Bot by Kirichek")
        self.tray.show()

# Переопределить closeEvent
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray.showMessage("Combine Bot", "Свёрнуто в трей", QSystemTrayIcon.Information)