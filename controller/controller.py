from model.model import Model
from view.mainview import Mainview
from view.graphicview import Graphicview
from PySide6.QtCore import Qt, QEvent, QObject
from utils.helpfunctions import *
from ystreamer import YahooStreamer

class Controller(QObject):
    def __init__(self, model: Model, view: Mainview, app, graphicview: Graphicview) -> None:
        super().__init__()
        self.model = model
        self.view = view
        self.app = app
        self.graphicview = graphicview
        self.initLiveticker()

        """Install event filter for plainTextEdit"""
        self.view.plainTextEdit_addTicker.installEventFilter(self)
        self.view.plainTextEdit_searchTicker.installEventFilter(self)
        self.view.plainTextEdit_methodinput.installEventFilter(self)
        self.view.table_watchlist.installEventFilter(self)
        self.view.table_analysis.installEventFilter(self)
        self.view.button_genGraph.installEventFilter(self)
        self.view.comboBox_period.currentTextChanged.connect(self.eventHandler_comboBox_period_change)

    def run(self) -> None:
        self.view.show()
        self.app.exec()

    def initLiveticker(self) -> None:
        """Init liveticker and connects eventhandler to liveticker"""
        self.yahoostreamer = YahooStreamer([tickerwrapper.ticker.info['symbol'] for tickerwrapper in self.model.tickerlist.values()], self.eventHandler_liveticker_update)
        self.yahoostreamer.start(reconnect=5)

    def eventHandler_liveticker_update(self, msg) -> None:
        """Eventhandler, which is called if a message from liveticker is received"""
        period = get_keyFromDictValue(self.view.comboBox_period.currentText(), valid_periods)
        self.model.update_liveticker(msg)
        self.view.update_table_analysis(period) # only update history for timeinterval '1m'

    def eventHandler_comboBox_period_change(self) -> None:
        """Eventhandler, which is called if comboBox period value is changed"""
        period = get_keyFromDictValue(self.view.comboBox_period.currentText(), valid_periods)
        self.model.update_tickerhistories(period='1d', verify_period=False)
        self.model.update_tickerhistories(period=period, verify_period=True)
        self.view.update_table_analysis(period)

    def eventHandler_plainTextEdit_searchTicker_enterPressed(self) -> None:
        """Eventhandler, which is called if Enter button is pressed in plainTextEdit addTicker
            It does the following steps:
            1. Check if ticker is valid
            2. Check if ticker already exists in watchlistfile
            3. Check if tickerhistory is valid
            4. Update Model (liveticker, watchlistfile, tickerhistory in tickerlist)
            5. update view (adds row in table watchlist and fills data)
            6. clears inputfield of plainTextEdit addTicker"""
        input = self.view.get_plaintextedit_input(self.view.plainTextEdit_addTicker)
        if not input:
            self.view.clear_input_field(self.view.plainTextEdit_addTicker)
            return
        tickerwrapper = self.model.get_tickerwrapper(input)
        if not tickerwrapper.verify_ticker_valid():
            self.view.clear_input_field(self.view.plainTextEdit_addTicker)
            return
        if self.model.check_duplicates_in_watchlistfile(tickerwrapper):
            self.view.clear_input_field(self.view.plainTextEdit_addTicker)
            return
        self.model.update_tickerhistory(period='1d', verify_period=False, tickerwrapper=tickerwrapper)
        if not tickerwrapper.verify_tickerhistory_valid(period="1d"):
            self.view.clear_input_field(self.view.plainTextEdit_addTicker)
            return
        period = get_keyFromDictValue(self.view.comboBox_period.currentText(), valid_periods)
        self.model.update_tickerhistory(period=period, verify_period=True, tickerwrapper=tickerwrapper)
        self.model.add_tickerinfo_to_watchlistfile(tickerwrapper)
        self.model.add_tickerwrapper_to_tickerwrapperlist(tickerwrapper)
        self.yahoostreamer.add_liveticker(tickerwrapper.ticker.info["symbol"])
        self.view.add_table_watchlist_row(tickerwrapper=tickerwrapper, period=period)
        self.view.clear_input_field(self.view.plainTextEdit_addTicker)

    def eventHandler_plainTextEdit_methodinput(self) -> None:
        """Eventhandler, which is called if Enter button is pressed in plainTextEdit methodinput"""
        methodArg = self.view.get_plaintextedit_input(self.view.plainTextEdit_methodinput)
        method = self.view.comboBox_method.currentText()
        if not methodArg:
            self.view.clear_input_field(self.view.plainTextEdit_methodinput)
            return
        self.view.add_table_analysis_row(methodArg = methodArg, method=method)
        self.model.add_method(methodArg=methodArg, method=method)
        self.view.clear_input_field(self.view.plainTextEdit_methodinput)

    def eventHandler_table_watchlist_delete_row(self) -> None:
        """Eventhandler, which is called if Delete button is pressed if a row is selected in table watchlist
            It does the following steps:
            1. gets selected symbol from table watchlist
            2. removes row in table watchlist
            3. removes tickerwrapper in Model (tickerlist, watchlistfile, liveticker)"""
        removedSymbol = self.view.get_selected_symbol_from_table_watchlist()
        self.view.remove_selected_row_from_table_watchlist()
        self.model.watchlistfile.remove_ticker_from_watchlistfile(removedSymbol)
        self.model.remove_tickerwrapper_from_tickerwrapperlist(removedSymbol)
        self.yahoostreamer.remove_liveticker(removedSymbol)

    def eventHandler_table_analysis_delete_row(self):
        """Eventhandler, which is called if Delete button is pressed if a row is selected in table analysis"""
        [method, methodArg] = self.view.get_selected_methodpair_from_table_analysis()
        if not method:
            return
        self.view.remove_selected_row_from_table_analysis()
        self.model.remove_method(methodArg, method)
    
    def eventHandler_button_genGraph_pressed(self):
        """Eventhandler, which is called if button genGraph is clicked. 
            Generates plot for the tickerhistories of all selected checkboxes in table watchlist"""
        selected_stocks = self.view.get_selected_Checkboxes()
        period = get_keyFromDictValue(self.view.comboBox_period.currentText(), valid_periods) # helpfunction needed to get key from value and dict
        self.graphicview.initstaticGraph(selected_stocks, period)

    def eventFilter(self, source, event):
        """Eventfilter, which is the main eventloop for most eventhandlers, 
            expect eventhandlers related to Qwidgets (e.g. button_genGraph)"""
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.view.plainTextEdit_addTicker:
                self.eventHandler_plainTextEdit_searchTicker_enterPressed()
                return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.view.table_watchlist:
                self.eventHandler_table_watchlist_delete_row()
                return True
        if event.type() == QEvent.KeyRelease or (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return):
            if source == self.view.plainTextEdit_searchTicker:
                self.view.handle_search_input_plainTextEdit_searchTicker()
                return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.view.plainTextEdit_methodinput:
                self.eventHandler_plainTextEdit_methodinput()
                return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.view.table_analysis:
                self.eventHandler_table_analysis_delete_row()
                return True
        if event.type() == QEvent.MouseButtonPress:
            if source == self.view.button_genGraph:
                self.eventHandler_button_genGraph_pressed()
                return True
        return super().eventFilter(source, event)