from model.model import Model
from view.mainview import Mainview
from view.graphicview import Graphicview
#from view.startupview import Startupview
from PySide6.QtCore import Qt, QEvent, QObject
from PySide6.QtWidgets import QApplication, QWidget
from model.historymanager import *
from model.liveticker.ystreamer import YahooStreamer

class Controller(QObject):
    def __init__(self, model: Model, mainview: Mainview, app: QApplication, graphicview: Graphicview) -> None:
        super().__init__()
        self.model = model
        self.mainview = mainview
        self.app = app
        app.setStyle("Fusion")
        self.graphicview = graphicview
        #self.startupview = startupview
        self.initLiveticker()

        """Install event filter for plainTextEdit"""
        self.mainview.plainTextEdit_addTicker.installEventFilter(self)
        self.mainview.plainTextEdit_searchTicker.installEventFilter(self)
        self.mainview.plainTextEdit_methodinput.installEventFilter(self)
        self.mainview.table_watchlist.installEventFilter(self)
        self.mainview.table_analysis.installEventFilter(self)
        self.mainview.button_genGraph.installEventFilter(self)
        self.mainview.comboBox_period.currentTextChanged.connect(self.eventHandler_comboBox_period_change)
        self.mainview.button_startAppliction.installEventFilter(self)
        self.mainview.button_selectWatchlist.installEventFilter(self)
        self.mainview.button_createWatchlist.installEventFilter(self)

    def run(self) -> None:
        self.mainview.show()
        self.app.exec()

    def initLiveticker(self) -> None:
        """Init liveticker and connects eventhandler to liveticker"""
        # Initialize the YahooStreamer with the tickers and the event handler
        tickers = [tickerwrapper.ticker.info['symbol'] for tickerwrapper in self.model.tickerwrappers.values()]
        self.yahoostreamer = YahooStreamer(tickers, self.eventHandler_liveticker_update)
        # Start the YahooStreamer
        self.yahoostreamer.start(reconnect=5)

    def eventHandler_liveticker_update(self, msg) -> None:
        """Eventhandler, which is called if a message from liveticker is received"""
        self.model.update_liveticker(msg)
        self.mainview.update_table_watchlist()  # only update history for time interval '1m'

    def eventHandler_comboBox_period_change(self) -> None:
        """Eventhandler, which is called if comboBox period value is changed"""
        period = get_shortname_from_longname(self.mainview.comboBox_period.currentText())
        self.model.update_tickerhistories(period='5d', verify_period=False)
        self.model.update_tickerhistories(period=period, verify_period=True)
        self.model.wrapper_convert_currencies()
        self.mainview.update_table_watchlist()

    def eventHandler_plainTextEdit_searchTicker_enterPressed(self) -> None:
        """Eventhandler, which is called if Enter button is pressed in plainTextEdit addTicker
            It does the following steps:
            1. Check if ticker is valid
            2. Check if ticker already exists in watchlistfile
            3. Check if tickerhistory is valid
            4. Update Model (liveticker, watchlistfile, tickerhistory in tickerlist, currencywrapper)
            5. update view (adds row in table watchlist and fills data)
            6. clears inputfield of plainTextEdit addTicker"""
        input = self.mainview.get_plaintextedit_input(self.mainview.plainTextEdit_addTicker)
        if not input:
            self.mainview.clear_input_field(self.mainview.plainTextEdit_addTicker)
            return
        tickerwrapper = self.model.get_tickerwrapper_yfinance(input)
        if not tickerwrapper.verify_ticker_valid():
            self.mainview.clear_input_field(self.mainview.plainTextEdit_addTicker)
            return
        if self.model.check_duplicates_in_watchlistfile(tickerwrapper):
            self.mainview.clear_input_field(self.mainview.plainTextEdit_addTicker)
            return
        tickerwrapper.update_tickerhistory(period='5d', verify_period=False)
        if not tickerwrapper.verify_tickerhistory_valid(period="5d"):
            self.mainview.clear_input_field(self.mainview.plainTextEdit_addTicker)
            return
        period = get_shortname_from_longname(self.mainview.comboBox_period.currentText())
        tickerwrapper.update_tickerhistory(period=period, verify_period=True)
        tickerwrapper.update_current_tickerhistory(period=period)
        tickerwrapper = self.model.wrapper_convert_currency(tickerwrapper=tickerwrapper)
        self.model.add_tickerinfo_to_watchlistfile(tickerwrapper)
        self.model.add_tickerwrapper_to_tickerwrappers(tickerwrapper)
        self.yahoostreamer.add_liveticker(tickerwrapper.ticker.info["symbol"])
        self.mainview.add_table_watchlist_row(tickerwrapper=tickerwrapper)
        self.mainview.clear_input_field(self.mainview.plainTextEdit_addTicker)

    def eventHandler_plainTextEdit_methodinput(self) -> None:
        """Eventhandler, which is called if Enter button is pressed in plainTextEdit methodinput"""
        methodArg = self.mainview.get_plaintextedit_input(self.mainview.plainTextEdit_methodinput)
        method = self.mainview.comboBox_method.currentText()
        if not methodArg:
            self.mainview.clear_input_field(self.mainview.plainTextEdit_methodinput)
            return
        self.mainview.add_table_analysis_row(methodArg = methodArg, method=method)
        self.model.add_method(methodArg=methodArg, method=method)
        self.mainview.clear_input_field(self.mainview.plainTextEdit_methodinput)

    def eventHandler_table_watchlist_delete_row(self) -> None:
        """Eventhandler, which is called if Delete button is pressed if a row is selected in table watchlist
            It does the following steps:
            1. gets selected symbol from table watchlist
            2. removes row in table watchlist
            3. removes tickerwrapper in Model (tickerlist, watchlistfile, liveticker)"""
        if self.mainview.table_watchlist.rowCount():
            removedSymbol = self.mainview.get_selected_symbol_from_table_watchlist()
            self.mainview.remove_selected_row_from_table_watchlist()
            self.model.watchlistfile.remove_ticker_from_watchlistfile(removedSymbol)
            self.model.remove_tickerwrapper_from_tickerwrappers(removedSymbol)
            self.yahoostreamer.remove_liveticker(removedSymbol)

    def eventHandler_table_analysis_delete_row(self):
        """Eventhandler, which is called if Delete button is pressed if a row is selected in table analysis"""
        [method, methodArg] = self.mainview.get_selected_methodpair_from_table_analysis()
        if not method:
            return
        self.mainview.remove_selected_row_from_table_analysis()
        self.model.remove_method(methodArg, method)

    def eventHandler_button_genGraph_pressed(self):
        """Eventhandler, which is called if button genGraph is clicked. 
            Generates plot for the tickerhistories of all selected checkboxes in table watchlist"""
        selected_stocks = self.mainview.get_selected_Checkboxes()
        self.graphicview.initstaticGraph(selected_stocks)


    """Eventhandlers for statupview"""
    def eventHandler_button_startAppliction(self):
        self.mainview.startApplication()

    def eventHandler_button_selectWatchlist(self):
        file_path = self.mainview.select_watchlist()
        self.model.watchlistfile.set_watchlistfile(file_path)
        self.model.watchlistfile.flag_watchlist_selected = True
    
    def eventHandler_button_createWatchlist(self):
        file_path = self.mainview.create_watchlist()
        self.model.watchlistfile.set_watchlistfile(file_path)
        self.model.watchlistfile.flag_watchlist_selected = True


    def eventFilter(self, source: QWidget, event: QEvent):
        """Eventfilter, which is the main eventloop for most eventhandlers, 
            expect eventhandlers related to Qwidgets (e.g. button_genGraph)"""
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.mainview.plainTextEdit_addTicker:
                self.eventHandler_plainTextEdit_searchTicker_enterPressed()
                return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.mainview.table_watchlist:
                self.eventHandler_table_watchlist_delete_row()
                return True
        if event.type() == QEvent.KeyRelease or (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return):
            if source == self.mainview.plainTextEdit_searchTicker:
                self.mainview.handle_search_input_plainTextEdit_searchTicker()
                return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.mainview.plainTextEdit_methodinput:
                self.eventHandler_plainTextEdit_methodinput()
                return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.mainview.table_analysis:
                self.eventHandler_table_analysis_delete_row()
                return True
        if event.type() == QEvent.MouseButtonPress:
            if source == self.mainview.button_genGraph:
                self.eventHandler_button_genGraph_pressed()
                return True
            
        #TODO: shift eventhandler for startupview to startup controller and create startupview file
        """Eventfilters for statupview"""
        if event.type() == QEvent.MouseButtonPress:
            if source == self.mainview.button_startAppliction:
                self.eventHandler_button_startAppliction()
                return True
        if event.type() == QEvent.MouseButtonPress:
            if source == self.mainview.button_selectWatchlist:
                self.eventHandler_button_selectWatchlist()
                return True
        if event.type() == QEvent.MouseButtonPress:
            if source == self.mainview.button_createWatchlist:
                self.eventHandler_button_createWatchlist()
                return True

        return super().eventFilter(source, event)