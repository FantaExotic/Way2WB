from model import Model
from view.mainview import Mainview
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QCheckBox
from PySide6.QtCore import Qt, QEvent, QObject

class Controller(QObject):
    def __init__(self, model: Model, view: Mainview, app) -> None:
        super().__init__()
        self.model = model
        self.view = view
        self.app = app

        # Install event filter for plainTextEdit
        self.view.plainTextEdit.installEventFilter(self)
        self.view.plainTextEdit_2.installEventFilter(self)
        self.view.plainTextEdit_3.installEventFilter(self)
        self.view.tableWidget.installEventFilter(self)
        self.view.tableWidget_2.installEventFilter(self)

    def run(self) -> None:
        self.view.show()
        self.app.exec()

    def eventFilter(self, source, event):
        #eventhandler for pressing enter in plainTextEdit to add symbol to watchlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.view.plainTextEdit:
                self.view.handle_enter_press_plainTextEdit()
                #TODO: call method for yfinance ticker/download object
                return True
        #eventhandler for pressing delete in tableWidget to remove symbol from watchlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.view.tableWidget:
                self.view.handle_delete_press_tableWidget()
                #TODO: call method for yfinance ticker/download object
                return True
        #eventhandler for entering data in plainTextEdit_2, to search stocks in watchlist
        if event.type() == QEvent.KeyRelease or (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return):
            if source == self.view.plainTextEdit_2:
                self.view.handle_search_input_plainTextEdit_2()
                return True
        #eventhandler for pressing enter in plainTextEdit_3 to add statistical method to methodlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.view.plainTextEdit_3:
                self.view.handle_enter_press_plainTextEdit_3()
                return True
        #eventhandler for pressing delete in tableWidget_2 to remove statMethod from methodlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.view.tableWidget_2:
                self.view.handle_delete_press_tableWidget_2()
                #TODO: call method for yfinance ticker/download object
                return True
        return super().eventFilter(source, event)
    

    