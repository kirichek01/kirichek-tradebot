from core.database import init_db
init_db()
import asyncio
from gui import MainWindow
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())