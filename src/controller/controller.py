from model.model import Model
from view.mainview import Mainview
from view.graphicview import Graphicview
#from view.startupview import Startupview
from PySide6.QtCore import Qt, QEvent, QObject, QThread
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QCloseEvent
from PySide6 import QtAsyncio
from model.historymanager import *
from model.liveticker.ystreamer import YFStreamer
import warnings
import asyncio

class Controller(QObject):
    def __init__(self, model: Model, mainview: Mainview, app: QApplication, graphicview: Graphicview) -> None:
        super().__init__()
        self.model = model
        self.mainview = mainview
        self.app = app
        app.setStyle("Fusion")
        self.graphicview = graphicview
        #self.mainview.callbackfunction = self.callback_upperlayer
        self.yfstreamer = None
        self.yfstreamer : YFStreamer
        #self.startupview = startupview

        """Install event filter for plainTextEdit"""
        #startup page
        self.mainview.button_startAppliction.installEventFilter(self)
        self.mainview.button_selectWatchlist.installEventFilter(self)
        self.mainview.button_createWatchlist.installEventFilter(self)

        #mainpage
        self.mainview.button_genGraph.installEventFilter(self)

        #mainpage: Configure Watchlist
        self.mainview.table_watchlist.installEventFilter(self)        
        self.mainview.plainTextEdit_addTicker.installEventFilter(self)
        self.mainview.plainTextEdit_searchTicker.installEventFilter(self)
        # Connect comboBox_period to async handler via wrapper
        #self.mainview.comboBox_period.installEventFilter(self)

        #mainpage: Configure analysis
        self.mainview.table_analysis.installEventFilter(self)
        self.mainview.plainTextEdit_methodinput.installEventFilter(self)

        #mainpage: Notifier and rules
        self.mainview.table_rules.installEventFilter(self)
        #self.mainview.comboBox_period_addRule.installEventFilter(self)
        #self.mainview.comboBox_tickers_addRule.installEventFilter(self)
        self.mainview.plainTextEdit_threshold_addRule.installEventFilter(self)
        self.mainview.plainTextEdit_subscribetopicinput.installEventFilter(self)
        self.mainview.checkBox_activateNotifier.installEventFilter(self)
        self.mainview.checkBox_activateLiveticker.installEventFilter(self)

    #def callback_upperlayer(self):
    #    warnings.simplefilter("ignore")
    #    if self.yfstreamer:
    #        self.yfstreamer.stop()
    #    #self.app.quit()

    def run(self) -> None:
        self.mainview.show()
        QtAsyncio.run()
        #self.app.exec()

    def initYFStreamer(self, tickers) -> None:
        """Init YFStreamer, which creates new Thread to listen for incoming messages based on YFStreamer subscriptions"""
        self.yfstreamer = YFStreamer(tickers,self.eventHandler_liveticker_update, self.mainview.liveticker_enabled())
        self.yfstreamer.start_YFStreamer()

    def eventHandler_liveticker_update(self, msg) -> None:
        """Eventhandler, which is called if a message from liveticker is received"""
        self.model.update_liveticker(msg)
        self.mainview.update_table_watchlist()  # only update history for time interval '1m'

    def wrapper_eventHandler_comboBox_period_changed(self) -> None:
        """Wrapper for async eventHandler_comboBox_period_change. Schedules async task without blocking GUI."""
        asyncio.create_task(self.eventHandler_comboBox_period_change())

    async def eventHandler_comboBox_period_change(self) -> None:
        """Eventhandler, which is called if comboBox period value is changed"""
        period = get_shortname_from_longname(self.mainview.comboBox_period.currentText())
        self.mainview.progressBar_tickerhistory_periodChange.show() # show progressbar during tickerhistory download
        self.mainview.setEnabled(False) # Disable the main window during tickerhistories download to prevent unintended behavior
        # workaround: currentiter and totaliter needed to calculate overall progress during multiple calls of this function
        # e.g. first call: currentiter=0, totaliter=2 for period='5d'; second call: currentiter=1, totaliter=2 for period=selected period
        await self.model.update_tickerhistories(period='5d', verify_period=False, callbackfunction_progressbarupdate=self.mainview.update_progressBar_tickerhistory_periodChange, currentiter=0, totaliter=2)
        await self.model.update_tickerhistories(period=period, verify_period=True, callbackfunction_progressbarupdate=self.mainview.update_progressBar_tickerhistory_periodChange, currentiter=1, totaliter=2)
        self.model.wrapper_convert_currencies()
        self.mainview.update_table_watchlist()
        self.mainview.progressBar_tickerhistory_periodChange.hide( )# hide progressbar after tickerhistory download
        self.mainview.setEnabled(True) # enable the main window again after tickerhistories download

    async def eventHandler_plainTextEdit_addTicker_enterPressed(self) -> None:
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
        tickerwrapper = await self.model.get_tickerwrapper_yfinance_async(input)
        if not tickerwrapper.verify_ticker_valid():
            self.mainview.clear_input_field(self.mainview.plainTextEdit_addTicker)
            return
        if self.model.check_duplicates_in_watchlistfile(tickerwrapper):
            self.mainview.clear_input_field(self.mainview.plainTextEdit_addTicker)
            return
        await tickerwrapper.update_tickerhistory_async(period='5d', verify_period=False)
        if not tickerwrapper.verify_tickerhistory_valid(period="5d"):
            self.mainview.clear_input_field(self.mainview.plainTextEdit_addTicker)
            return
        period = get_shortname_from_longname(self.mainview.comboBox_period.currentText())
        await tickerwrapper.update_tickerhistory_async(period=period, verify_period=True)
        tickerwrapper.update_current_tickerhistory(period=period)
        tickerwrapper = self.model.wrapper_convert_currency(tickerwrapper=tickerwrapper)
        self.model.add_tickerinfo_to_watchlistfile(tickerwrapper)
        self.model.add_tickerwrapper_to_tickerwrappers(tickerwrapper)
        self.yfstreamer.add_liveticker(tickerwrapper.ticker.info_local["symbol"])
        self.mainview.add_table_watchlist_row(tickerwrapper=tickerwrapper)
        self.mainview.clear_input_field(self.mainview.plainTextEdit_addTicker)
        self.mainview.add_comboBox_tickers_addRule(tickerwrapper=tickerwrapper)
        
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
            self.yfstreamer.remove_liveticker(removedSymbol)
            self.model.remove_tickerwrapper_from_tickerwrappers(removedSymbol)
            self.mainview.removeItem_comboBox_tickers_addRule(removedSymbol)
            self.mainview.deactivate_rules_from_deleted_tickers(removedSymbol=removedSymbol)

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
        # alternativ below: create new object for each graphicview.
        #graphicview = Graphicview(self.model, self.mainview)
        #graphicview.initstaticGraph(selected_stocks)


    """Eventhandlers for statupview"""
    async def eventHandler_button_startAppliction(self):
        if self.model.watchlistfile.flag_watchlist_selected:
            await self.mainview.startApplication()
            self.mainview.comboBox_period.currentTextChanged.connect(self.wrapper_eventHandler_comboBox_period_changed) # workaround to prevent eventhandler trigger when adding periods to comboBox
            tickers = [tickerwrapper.ticker.info_local['symbol'] for tickerwrapper in self.model.tickerwrappers.values()]
            self.initYFStreamer(tickers)

    def eventHandler_button_selectWatchlist(self):
        file_path = self.mainview.select_watchlist()
        self.model.watchlistfile.set_watchlistfile(file_path)
        self.model.watchlistfile.flag_watchlist_selected = True
    
    def eventHandler_button_createWatchlist(self):
        file_path = self.mainview.create_watchlist()
        self.model.watchlistfile.set_watchlistfile(file_path)
        self.model.watchlistfile.flag_watchlist_selected = True
        
    def eventHandler_table_rules_delete_row(self) -> None:
        """Eventhandler, which is called if Delete button is pressed if a row is selected in table watchlist
            It does the following steps:
            1. gets selected symbol from table watchlist
            2. removes row in table watchlist
            3. removes tickerwrapper in Model (tickerlist, watchlistfile, liveticker)"""
        if self.mainview.table_watchlist.rowCount():
            [symbol, threshold, period] = self.mainview.get_selected_items_from_table_rules()
            for rule in self.model.rules:
                if rule.symbol == symbol and rule.threshold == threshold and rule.period == period:
                    self.model.rules.remove(rule)
                    self.mainview.remove_selected_row_from_table_rules()
                    return

    """Eventhandlers for notifier view"""
    def eventHandler_plainTextEdit_createNewRule(self):
        period = self.mainview.comboBox_period_addRule.currentText()
        symbol = self.mainview.comboBox_tickers_addRule.currentText()
        threshold = self.mainview.get_plaintextedit_input(self.mainview.plainTextEdit_threshold_addRule)
        self.model.add_rule(symbol=symbol, threshold=threshold, period=period)
        self.mainview.add_table_rules_row(symbol=symbol, threshold=threshold, period=period)
        self.mainview.clear_input_field(self.mainview.plainTextEdit_threshold_addRule)

    def eventFilter(self, source: QWidget, event: QEvent):
        """Eventfilter, which is the main eventloop for most eventhandlers, 
            expect eventhandlers related to Qwidgets (e.g. button_genGraph)"""
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.mainview.plainTextEdit_addTicker:
                asyncio.create_task(self.eventHandler_plainTextEdit_addTicker_enterPressed())
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
        """Eventfilters for startupview"""
        if event.type() == QEvent.MouseButtonPress:
            if source == self.mainview.button_startAppliction:
                asyncio.create_task(self.eventHandler_button_startAppliction())
                return True
        if event.type() == QEvent.MouseButtonPress:
            if source == self.mainview.button_selectWatchlist:
                self.eventHandler_button_selectWatchlist()
                return True
        if event.type() == QEvent.MouseButtonPress:
            if source == self.mainview.button_createWatchlist:
                self.eventHandler_button_createWatchlist()
                return True
            
        """Eventfilters for rules"""
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            if source == self.mainview.plainTextEdit_threshold_addRule:
                self.eventHandler_plainTextEdit_createNewRule()
                return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            if source == self.mainview.table_rules:
                self.eventHandler_table_rules_delete_row()
                return True

        return super().eventFilter(source, event)