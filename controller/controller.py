from model import Model
from view.mainview import Mainview
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QEvent

class Controller:
    def __init__(self, model: Model, view: Mainview, app) -> None:
        self.model = model
        self.view = view
        self.app = app

    def run(self) -> None:
        self.view.show()
        self.app.exec()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.view.plainTextEdit:
                self.view.handle_enter_press()
                return True
        return super().eventFilter(source, event)