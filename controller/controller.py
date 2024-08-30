from model.model import Model
from view.mainview import Mainview
from view.graphicview import Graphicview
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QCheckBox
from PySide6.QtCore import Qt, QEvent, QObject, QThread, Signal
from utils.helpfunctions import *
from model.tickerwrapper import TickerWrapper
from ystreamer import YahooStreamer

class Controller(QObject):
    def __init__(self, model: Model, view: Mainview, app, graphicview: Graphicview) -> None:
        super().__init__()
        self.model = model
        self.view = view
        self.app = app
        self.graphicview = graphicview

        # init thread for yliveticker
        self.initLiveticker()

        # Install event filter for plainTextEdit
        self.view.plainTextEdit_addTicker.installEventFilter(self)
        self.view.plainTextEdit_searchTicker.installEventFilter(self)
        self.view.plainTextEdit_methodinput.installEventFilter(self)
        self.view.table_watchlist.installEventFilter(self)
        self.view.table_analysis.installEventFilter(self)
        self.view.button_genGraph.installEventFilter(self)
        self.view.comboBox_period.currentTextChanged.connect(self.eventHandler_comboBox_period)

    def run(self) -> None:
        self.view.show()
        self.app.exec()

    def initLiveticker(self) -> None:
        # Create a QThread for the live ticker
        self.yahoostreamer = YahooStreamer([tickerwrapper.ticker.info['symbol'] for tickerwrapper in self.model.tickerlist], self.eventHandler_liveticker_update)
        self.yahoostreamer.start()

    def eventHandler_liveticker_update(self, msg):
        period = get_keyFromDictValue(self.view.comboBox_period.currentText(), valid_periods)
        self.model.update_liveticker(msg)
        self.view.handle_updateTickervalue(period) # only update history for timeinterval '1m'

    # different apporach needed than eventFilter, because multiple clicks are required to change value of comboBox_period
    def eventHandler_comboBox_period(self):
        period = get_keyFromDictValue(self.view.comboBox_period.currentText(), valid_periods)
        self.model.update_tickerhistory(period='1d', verify_period=False)
        # second tickerhistory update needed after history for period '1d' was downloaded.
        # because we need access to valid_periods dict in ticker, which only gets initialized 
        # after downloading a ticker history
        self.model.update_tickerhistory(period=period, verify_period=True)
        self.view.handle_updateTickervalue(period)

    def eventFilter(self, source, event):
        #eventhandler for pressing enter in plainTextEdit to add symbol to watchlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.view.plainTextEdit_addTicker:
                input = self.view.get_plaintextedit_input(self.view.plainTextEdit_addTicker)
                if not input:
                    self.view.clear_input_field(self.view.plainTextEdit_addTicker)
                    return True
                tickerwrapper = self.model.get_tickerwrapper(input)
                if not tickerwrapper.verify_ticker_valid():
                    self.view.clear_input_field(self.view.plainTextEdit_addTicker)
                    return True
                if self.model.check_duplicates_in_watchlistfile(tickerwrapper):
                    self.view.clear_input_field(self.view.plainTextEdit_addTicker)
                    return True
                self.model.add_ticker_to_watchlistfile(tickerwrapper) # bool_addToWatchlist 1 if symbol shall be added, else 0
                self.model.add_tickerwrapper_to_tickerwrapperlist(tickerwrapper)
                self.yahoostreamer.add_ticker(tickerwrapper.ticker.info["symbol"])
                self.eventHandler_comboBox_period()
                self.view.handle_enter_press_plainTextEdit_addTicker(tickerwrapper)
                self.view.clear_input_field(self.view.plainTextEdit_addTicker)
                #TODO: add thread handling
                return True

        #eventhandler for pressing delete in table_watchlist to remove symbol from watchlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.view.table_watchlist:
                removedSymbol = self.view.handle_delete_press_tableWidget()
                self.model.remove_ticker_from_watchlistfile(removedSymbol)
                self.model.remove_tickerwrapper_from_tickerwrapperlist(removedSymbol)
                self.yahoostreamer.remove_ticker(removedSymbol)
                return True
        #eventhandler for entering data in plainTextEdit_2, to search stocks in watchlist
        if event.type() == QEvent.KeyRelease or (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return):
            if source == self.view.plainTextEdit_searchTicker:
                self.view.handle_search_input_plainTextEdit_searchTicker()
                return True
        #eventhandler for pressing enter in plainTextEdit_3 to add statistical method to methodlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.view.plainTextEdit_methodinput:
                method = self.view.handle_enter_press_plainTextEdit_methodinput()
                if method:
                    self.model.methods.append(method)
                self.view.clear_input_field(self.view.plainTextEdit_methodinput)
                return True
        #eventhandler for pressing delete in table_analysis to remove statMethod from methodlist
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.view.table_analysis:
                method = self.view.handle_delete_press_table_analysis()
                if method:
                    self.model.methods.remove(method)
                return True
        if event.type() == QEvent.MouseButtonPress:
            if source == self.view.button_genGraph:
                #TODO: integrate graphicview to mainview!
                selected_stocks = self.view.get_selected_Checkboxes()
                # get optimal period/interval pairing to get maximum data based on selected period
                period = get_keyFromDictValue(self.view.comboBox_period.currentText(), valid_periods) # helpfunction needed to get key from value and dict
                self.graphicview.initstaticGraph(selected_stocks, period)
                return True
        return super().eventFilter(source, event)