from model import Model
from view.mainview import Mainview
from view.graphicview import Graphicview
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QCheckBox
from PySide6.QtCore import Qt, QEvent, QObject
from helpfunctions import *

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
        self.view.button_genGraph.installEventFilter(self)

    def run(self) -> None:
        self.view.show()
        self.app.exec()

    def eventFilter(self, source, event):
        #eventhandler for pressing enter in plainTextEdit to add symbol to watchlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.view.plainTextEdit:
                try: # try block need to ensure ticker is valid, to prevent typo errors
                    ticker = self.model.findTicker(self.view.get_plaintextedit_input(self.view.plainTextEdit))
                    if ticker:
                        bool_addToWatchlist = self.model.add_stockticker_to_watchlist(ticker) # bool_addToWatchlist 1 if symbol shall be added, else 0
                        if bool_addToWatchlist:
                            self.view.handle_enter_press_plainTextEdit(ticker)
                    else:
                        print("symbol not found")
                        #TODO: highlight symbol not found error in view, in case it happens!
                except:
                    print("ticker doesnt contain valid data. Recheck entered stocksymbol")
                finally:
                    return True

        #eventhandler for pressing delete in tableWidget to remove symbol from watchlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.view.tableWidget:
                removedSymbol = self.view.handle_delete_press_tableWidget()
                self.model.remove_stockticker_from_watchlist(removedSymbol)
                return True
        #eventhandler for entering data in plainTextEdit_2, to search stocks in watchlist
        if event.type() == QEvent.KeyRelease or (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return):
            if source == self.view.plainTextEdit_2:
                self.view.handle_search_input_plainTextEdit_2()
                return True
        #eventhandler for pressing enter in plainTextEdit_3 to add statistical method to methodlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.view.plainTextEdit_3:
                method = self.view.handle_enter_press_plainTextEdit_3()
                if method:
                    self.model.methods.append(method)
                return True
        #eventhandler for pressing delete in tableWidget_2 to remove statMethod from methodlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.view.tableWidget_2:
                method = self.view.handle_delete_press_tableWidget_2()
                if method:
                    self.model.methods.remove(method)
                return True
        if event.type() == QEvent.MouseButtonPress:
            if source == self.view.button_genGraph:
                #TODO: integrate graphicview to mainview!
                selected_stocks = self.view.get_selected_Checkboxes()
                # get optimal period/interval pairing to get maximum data based on selected period
                period = get_keyFromDictValue(self.view.comboBox_2.currentText(), self.model.valid_periods) # helpfunction needed to get key from value and dict
                interval = self.model.setTickerArgs(period) 
                graphicview = Graphicview(self.model, self.view, selected_stocks, period, interval)
                return True

        return super().eventFilter(source, event)