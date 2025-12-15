from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QCheckBox, QTableWidget, QFileDialog, QProgressBar
from view.qt.mainframe import Ui_frame_main
from model.model import Model
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPlainTextEdit, QComboBox
from PySide6.QtGui import QCloseEvent
from model.tickerwrapper import TickerWrapper
from model.historymanager import Period_Tickerhistory_Longname
from enum import Enum
from config.configmanager import YAxisSetting

class TableWatchlistRows(Enum):
    """Config for columns in table watchlist"""
    SHORTNAME = 0
    SYMBOLNAME = 1
    ISIN = 2
    CURRENTVALUE = 3
    DELTAVALUE = 4
    CHECKBOX = 5

class TableAnalysisRows(Enum):
    """Config for columns in table watchlist"""
    METHODNAME = 0
    METHODVALUE = 1

class TableRulesRows(Enum):
    """Config for columns in table rules"""
    PERIOD = 0
    THRESHOLD = 1
    SYMBOL = 2
    ACTIVATED = 3

class Mainview(QMainWindow, Ui_frame_main):
    def __init__(self, model: Model):
        super().__init__()
        self.setupUi(self)
        self.model = model
        self.stackedWidget.setCurrentIndex(0) # set stacked widget to startup view
        self.progressBar_tickerhistory_periodChange.hide() # workaround to hide progressbar in tab_watchlist
        self.progressBar_tickers.hide() # workaround to hide progressbar in startup view

        self.widgets_with_eventhandler = [
        #startup page
        self.button_startAppliction,
        self.button_selectWatchlist,
        self.button_createWatchlist,
        self.checkBox_activateLiveticker,

        #tab watchlist
        self.table_watchlist,
        self.plainTextEdit_addTicker,
        self.plainTextEdit_searchTicker,
        self.button_genGraph,

        #tab analysis
        self.table_analysis,
        self.plainTextEdit_methodinput,

        #tab Notifier and rules
        self.table_rules,
        #self.comboBox_period_addRule
        #self.comboBox_tickers_addRule
        self.plainTextEdit_threshold_addRule,
        self.plainTextEdit_subscribetopicinput,
        self.checkBox_activateNotifier
        ]

    def init_mainview(self) -> None:
        self._init_statMethods()
        self._init_yaxisSettings()
        self._init_intervals(comboBox=self.comboBox_period)
        self._init_table_watchlist()
        self.init_notifier_and_rules()

    def checkbox_liveticker_enabled(self) -> bool:
        """returns if liveticker is enabled from checkbox in mainview"""
        return self.checkBox_activateLiveticker.isChecked()

    def get_selected_Checkboxes(self) -> list:
        """function to get all selected checkboxes from watchlist, which shall be used for analysis and graph generation"""
        ret = list()
        for row in range(self.table_watchlist.rowCount()):
            symbol = self.table_watchlist.item(row, TableWatchlistRows.SYMBOLNAME.value).text()
            checkbox = self.table_watchlist.cellWidget(row, TableWatchlistRows.CHECKBOX.value)
            if checkbox.isChecked():
                ret.append(symbol)
        return ret

    def get_selected_symbol_from_table_watchlist(self) -> str:
        """Get symbol of the selected row in table watchlist"""
        return self._get_selected_item_from_table(table=self.table_watchlist, column=TableWatchlistRows.SYMBOLNAME.value).text()

    def get_selected_methodpair_from_table_analysis(self) -> str:
        """Get method and methodArg of the selected row in table analysis"""
        method = self._get_selected_item_from_table(table=self.table_analysis, column=TableAnalysisRows.METHODNAME.value).text()
        methodArg = self._get_selected_item_from_table(table=self.table_analysis, column=TableAnalysisRows.METHODVALUE.value).text()
        return [method, methodArg]

    def remove_selected_row_from_table_watchlist(self) -> None:
        """Remove selected row from table watchlist"""
        self._remove_selected_row_from_table(table=self.table_watchlist)

    def remove_selected_row_from_table_analysis(self) -> None:
        """Remove selected row from table analysis"""
        self._remove_selected_row_from_table(table=self.table_analysis)

    def add_table_watchlist_row(self, tickerwrapper: TickerWrapper):
        """ adds new row to table watchlist and sets the according values to all columns in the added row"""
        row = self.table_watchlist.rowCount()
        self.table_watchlist.insertRow(row)
        self._set_table_watchlist_row_staticItems(tickerwrapper=tickerwrapper,row=row)
        self._set_table_watchlist_row_dynamicItems(tickerwrapper=tickerwrapper,row=row)

    def add_table_analysis_row(self, methodArg: int, method: str) -> None:
        """adds new row to table analysis and sets the according values to all columns in the added row"""
        row = self.table_analysis.rowCount()
        self.table_analysis.insertRow(row)
        self._set_table_analysis_row_staticItems(methodArg=methodArg, method=method, row=row)

    def update_table_watchlist(self):
        """updates dynamic items in each row. Dynamic items are items, which will be update during runtime
            by the liveticker (e.g.: currentValue and deltavalue)"""
        for row in range(self.table_watchlist.rowCount()):
            tickersymbol = self.table_watchlist.item(row,TableWatchlistRows.SYMBOLNAME.value).text()
            self._set_table_watchlist_row_dynamicItems(tickerwrapper = self.model.tickerwrappers[tickersymbol], row = row)

    def handle_search_input_plainTextEdit_searchTicker(self):
        """filteres each row in table watchlist, if plainTextEdit searchTicker is no substring of symbol or shortName"""
        search_text = self.get_plaintextedit_input(self.plainTextEdit_searchTicker)
        for row in range(self.table_watchlist.rowCount()):
            stockname_item = self.table_watchlist.item(row, TableWatchlistRows.SHORTNAME.value)
            symbolname_item = self.table_watchlist.item(row, TableWatchlistRows.SYMBOLNAME.value)
            if stockname_item is None or symbolname_item is None:
                print("stockname or symbolname == None!")
                continue
            stockname = stockname_item.text().lower()
            symbolname = symbolname_item.text().lower()
            if search_text in stockname or search_text in symbolname:
                self.table_watchlist.setRowHidden(row, False)
            else:
                self.table_watchlist.setRowHidden(row, True)

    def get_plaintextedit_input(self, qPlainTextEdit: QPlainTextEdit):
        """returns text from qPlainTextEdit"""
        ret = qPlainTextEdit.toPlainText().strip()
        return ret

    def clear_input_field(self, qPlainTextEdit: QPlainTextEdit):
         """Clears text in qPlainTextEdit"""
         qPlainTextEdit.clear()

    """functions for startup view"""

    #TODO: move this function to controller
    async def startApplication(self):
        if self.model.watchlistfile.flag_watchlist_selected:
            self.progressBar_tickers.show() # set format for loading progress
            self.setEnabled(False) # Disable the main window during loading tickers
            await self.model.init_model_async(callbackfunction=self.update_progressbar_tickers)
            self.progressBar_tickers.hide()
            self.setEnabled(True) # Enable the main window after loading tickers
            self.init_mainview()
            self.stackedWidget.setCurrentIndex(1)

    def select_watchlist(self):
                # Open a file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Json file (*.json)")
        if file_path:
            self.label_watchlistpath_startup.setText(file_path)  # Update the label with the selected file path
            #self.stackedWidget.setCurrentIndex(1)  # Switch to the main application page
        else:
            self.label_watchlistpath_startup.setText("No Watchlist imported. Application cannot be started before loading watchlist")
        return file_path
    
    def create_watchlist(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Json file (*.json)")

        with open(file_path, 'w') as file:
            pass  # Do nothing, just create the empty file
        #print(file_path)
        return file_path
    
    """functions for notifier and rules"""
    
    def init_notifier_and_rules(self):
        self.init_comboBox_tickers_addRule()
        self._init_intervals(comboBox=self.comboBox_period_addRule)

    def init_comboBox_tickers_addRule(self):
        """Init comboBox period for addRule with all periods from yfinance"""
        tickerwrapper: TickerWrapper
        for tickerwrapper in self.model.tickerwrappers.values():
            self.add_comboBox_tickers_addRule(tickerwrapper)
        #self.comboBox_tickers_addRule.setCurrentText(tickerwrapper.ticker.info_local["shortName"])

    def add_comboBox_tickers_addRule(self, tickerwrapper: TickerWrapper):
        """adds new ticker to comboBox tickers_addRule"""
        self.comboBox_tickers_addRule.addItem(tickerwrapper.ticker.info_local["symbol"])

    def add_table_rules_row(self, symbol: str, threshold: int, period: str):
        """ adds new row to table watchlist and sets the according values to all columns in the added row"""
        row = self.table_rules.rowCount()
        self.table_rules.insertRow(row)
        self._set_table_rules_row_staticItems(symbol=symbol, threshold=threshold, period=period, row=row)

    def remove_selected_row_from_table_rules(self) -> None:
        """Remove selected row from table analysis"""
        self._remove_selected_row_from_table(table=self.table_rules)

    def get_selected_items_from_table_rules(self) -> str:
        """Get symbol of the selected row in table rules"""
        symbol = self._get_selected_item_from_table(table=self.table_rules, column=TableRulesRows.SYMBOL.value).text()
        threshold = self._get_selected_item_from_table(table=self.table_rules, column=TableRulesRows.THRESHOLD.value).text()
        period = self._get_selected_item_from_table(table=self.table_rules, column=TableRulesRows.PERIOD.value).text()
        return [symbol, threshold, period]
    
    def deactivate_rules_from_deleted_tickers(self, removedSymbol: str):
        for row in range(self.table_rules.rowCount()):
            item = self.table_rules.item(row, TableRulesRows.SYMBOL.value).text()
            if item == removedSymbol:
                checkboxItem = self.table_rules.cellWidget(row, TableRulesRows.ACTIVATED.value)
                checkboxItem.setChecked(False)
                #TODO: add feature to grey out checkbox with setEnabled(False),
                # but needs be enabled again if ticker will be readded to watchlist

    def removeItem_comboBox_tickers_addRule(self, symbol: str):
        index = self.comboBox_tickers_addRule.findText(symbol)
        if index >= 0:
            self.comboBox_tickers_addRule.removeItem(index)

    def update_progressbar_tickers(self, currentTickerwrapperIndex: int, totalTickerwrappers) -> None:
        """updates progressbar from startup view for ticker download"""
        self.progressBar_tickers.setValue(currentTickerwrapperIndex/totalTickerwrappers*100)

    def update_progressBar_tickerhistory_periodChange(self, currentTickerwrapperIndex: int, totalTickerwrappers) -> None:
        """updates progressbar from analysis view for tickerhistory download during period change"""
        self.progressBar_tickerhistory_periodChange.setValue(currentTickerwrapperIndex/totalTickerwrappers*100)

    """private functions"""

    def _set_table_watchlist_row_staticItems(self, tickerwrapper: TickerWrapper, row: int): #TODO: change datatype for interval! create own datatype for available intervals
        """Updates static items in table watchlist, which only need to be set once"""
        self.table_watchlist.setItem(row, TableWatchlistRows.SHORTNAME.value, QTableWidgetItem(tickerwrapper.ticker.info_local["shortName"]))
        self.table_watchlist.setItem(row, TableWatchlistRows.SYMBOLNAME.value, QTableWidgetItem(tickerwrapper.ticker.info_local["symbol"]))
        self.table_watchlist.setItem(row, TableWatchlistRows.ISIN.value, QTableWidgetItem(tickerwrapper.ticker.isin_local))
        analyze_checkbox = QCheckBox()
        analyze_checkbox.setChecked(False)
        self.table_watchlist.setCellWidget(row, TableWatchlistRows.CHECKBOX.value, analyze_checkbox)

    def _set_table_watchlist_row_dynamicItems(self, tickerwrapper: TickerWrapper, row: int): #TODO: change datatype for interval! create own datatype for available intervals
        """Updates dynamic items in table watchlist, which will be updated dynamically based on data from liveticker"""
        openprice = tickerwrapper.tickerhistory['1m']['Open'].values[-1].item()
        stockvalue = QTableWidgetItem() # very inefficient!
        stockvalue.setData(Qt.EditRole, openprice)
        self.table_watchlist.setItem(row, TableWatchlistRows.CURRENTVALUE.value, stockvalue)
        stockdiff = QTableWidgetItem()
        delta_start = tickerwrapper.tickerhistory["current"]['Open'].values[0].item() #index 0 because we want difference to start of interval
        delta_end = openprice
        if delta_start == 0:
            delta_start = tickerwrapper.tickerhistory["current"]['Close'].values[0].item() # workaround if Open value == 0
        delta = delta_end/delta_start * 100 - 100
        stockdiff.setData(Qt.EditRole, delta)
        self.table_watchlist.setItem(row, TableWatchlistRows.DELTAVALUE.value, stockdiff)

    def _init_statMethods(self):
        """Add methods to comboBox method"""
        self.comboBox_method.addItem("Moving Average")

    def _init_yaxisSettings(self):
        """Init comboBox yaxis settings with all available settings"""
        for setting in YAxisSetting:
            self.comboBox_analysis_yaxisSetting.addItem(setting.value)
        self.comboBox_analysis_yaxisSetting.setCurrentText(YAxisSetting.ABSOLUTE.value) 

    def _init_intervals(self, comboBox: QComboBox):
        """Init comboBox period with all periods from yfinance"""
        for period in Period_Tickerhistory_Longname:
            comboBox.addItem(period.value)
        comboBox.setCurrentText(Period_Tickerhistory_Longname.DAYS_5.value)

    def _get_selected_item_from_table(self, table: QTableWidget, column: TableWatchlistRows.SYMBOLNAME.value) -> QTableWidgetItem:
        """return item in selected row and column, table in arg"""
        row = table.currentRow()
        item = table.item(row, column)
        return item

    def _remove_selected_row_from_table(self, table: QTableWidget) -> None:
        """removes selected rows from table in arg"""
        row = table.currentRow()
        table.removeRow(row)

    def _init_table_watchlist(self):
        """Init table watchlist"""
        tickerwrapper: TickerWrapper
        for tickerwrapper in self.model.tickerwrappers.values():
            self.add_table_watchlist_row(tickerwrapper=tickerwrapper)

    def _set_table_analysis_row_staticItems(self, methodArg: int, method: str, row: int):
        """Set method and methodArg for corresponding row in table analysis"""
        statistical_method_value = QTableWidgetItem()
        statistical_method_value.setData(Qt.EditRole, methodArg)
        self.table_analysis.setItem(row, TableAnalysisRows.METHODNAME.value, QTableWidgetItem(method))
        self.table_analysis.setItem(row, TableAnalysisRows.METHODVALUE.value, statistical_method_value)

    def _set_table_rules_row_staticItems(self, symbol: str, threshold: int, period: str, row: int):
        """Set rule for corresponding row in table rules"""
        item_symbol = QTableWidgetItem(symbol)
        item_threshold = QTableWidgetItem()
        item_period = QTableWidgetItem(period)
        item_threshold.setData(Qt.EditRole, threshold)
        self.table_rules.setItem(row, TableRulesRows.SYMBOL.value, item_symbol)
        self.table_rules.setItem(row, TableRulesRows.THRESHOLD.value, item_threshold)
        self.table_rules.setItem(row, TableRulesRows.PERIOD.value, item_period)
        item_activated = QCheckBox()
        item_activated.setChecked(False)
        self.table_rules.setCellWidget(row, TableRulesRows.ACTIVATED.value, item_activated)