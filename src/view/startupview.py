from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QCheckBox, QTableWidget
from view.qt.mainframe import Ui_frame_main
from model.model import Model
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPlainTextEdit
from model.historymanager import Period_Tickerhistory_Longname
from enum import Enum

class Startupview(QMainWindow, Ui_frame_main):
    def __init__(self, model: Model):
        super().__init__()
        self.setupUi(self)
        self.model = model