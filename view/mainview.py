from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QTableWidget
from view.qt.mainframe import Ui_frame_main
from model.model import Model
from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QPlainTextEdit
import yfinance as yf
from model.tickerwrapper import TickerWrapper
from utils.helpfunctions import *
from enum import Enum

class TableWatchlistRows(Enum):
    SHORTNAME = 0
    SYMBOLNAME = 1
    ISIN = 2
    CURRENTVALUE = 3
    DELTAVALUE = 4
    CHECKBOX = 5

class TableAnalysisRows(Enum):
    METHODNAME = 0
    METHODVALUE = 1

class Mainview(QMainWindow, Ui_frame_main):
    def __init__(self, model: Model):
        super().__init__()
        self.setupUi(self)
        self.model = model
        self.init_statMethods()
        self.init_intervals()
        self.init_table_analysis()

    # --------------------------------------------
    # new data
    def set_table_watchlist_row_staticItems(self, tickerwrapper: TickerWrapper, row: int): #TODO: change datatype for interval! create own datatype for available intervals
        """Updates static elements, which only need to be set once"""
        self.table_watchlist.setItem(row, TableWatchlistRows.SHORTNAME.value, QTableWidgetItem(tickerwrapper.ticker.info["shortName"]))
        self.table_watchlist.setItem(row, TableWatchlistRows.SYMBOLNAME.value, QTableWidgetItem(tickerwrapper.ticker.info["symbol"]))
        #self.table_watchlist.setItem(row_position, 2, QTableWidgetItem(each.isin))
        self.table_watchlist.setItem(row, TableWatchlistRows.ISIN.value, QTableWidgetItem("default ISIN"))
        analyze_checkbox = QCheckBox()
        analyze_checkbox.setChecked(False)
        self.table_watchlist.setCellWidget(row, TableWatchlistRows.CHECKBOX.value, analyze_checkbox)

    def set_table_watchlist_row_dynamicItems(self, tickerwrapper: TickerWrapper, row: int, interval: str): #TODO: change datatype for interval! create own datatype for available intervals
        """Updates dynamic elements in analysis table, which will be updated dynamically in tickerhistory"""
        lastDataframeIndex = tickerwrapper.tickerhistory['1m'].shape[0]-1
        #TODO: add try catch for accessing shape, doesnt seem to be consistent (e.g. LULU at 10:28 am)
        openprice = tickerwrapper.tickerhistory['1m']['Open'].values[lastDataframeIndex].item()
        stockvalue = QTableWidgetItem() # very inefficient!!! Fix it!
        stockvalue.setData(Qt.EditRole, openprice)
        self.table_watchlist.setItem(row, TableWatchlistRows.CURRENTVALUE.value, stockvalue)

        #index 0 because we want difference to start of interval (e.g. start of month instead end of month)
        stockdiff = QTableWidgetItem()
        delta_start = tickerwrapper.tickerhistory[interval]['Open'].values[0].item()
        delta_end = openprice
        delta = delta_end/delta_start * 100 - 100
        stockdiff.setData(Qt.EditRole, delta)
        self.table_watchlist.setItem(row, TableWatchlistRows.DELTAVALUE.value, stockdiff)

    # function to get all selected checkboxes from watchlist, which shall be used for analysis and graph generation
    def get_selected_Checkboxes(self) -> list:
        ret = list()
        for row in range(self.table_watchlist.rowCount()):
            symbol = self.table_watchlist.item(row, TableWatchlistRows.SYMBOLNAME.value).text()
            checkbox = self.table_watchlist.cellWidget(row, TableWatchlistRows.CHECKBOX.value)
            if checkbox.isChecked():
                ret.append(symbol)
        return ret

    def get_selected_symbol_from_table_watchlist(self) -> str:
        return self._get_selected_item_from_table(table=self.table_watchlist, column=TableWatchlistRows.SYMBOLNAME.value).text()

    def get_selected_methodpair_from_table_analysis(self) -> str:
        method = self._get_selected_item_from_table(table=self.table_analysis, column=TableAnalysisRows.METHODNAME.value).text()
        methodArg = self._get_selected_item_from_table(table=self.table_analysis, column=TableAnalysisRows.METHODVALUE.value).text()
        return [method, methodArg]
    
    def _get_selected_item_from_table(self, table: QTableWidget, column: TableWatchlistRows.SYMBOLNAME.value) -> QTableWidgetItem:
        row = table.currentRow()
        item = table.item(row, column)
        return item

    def remove_selected_row_from_table_watchlist(self) -> None:
        self._remove_selected_row_from_table(table=self.table_watchlist)

    def remove_selected_row_from_table_analysis(self) -> None:
        self._remove_selected_row_from_table(table=self.table_analysis)

    # removes selected stock from tablewidget
    def _remove_selected_row_from_table(self, table: QTableWidget) -> None:
        row = table.currentRow()
        table.removeRow(row)

    def add_table_watchlist_row(self, tickerwrapper: TickerWrapper, period: str):
        row = self.table_watchlist.rowCount() # needed to identify row to insert data
        self.table_watchlist.insertRow(row)
        interval = setTickerArgs(period)
        self.set_table_watchlist_row_staticItems(tickerwrapper=tickerwrapper,row=row)
        self.set_table_watchlist_row_dynamicItems(tickerwrapper=tickerwrapper,row=row,interval=interval)

    def init_table_analysis(self):
        period = get_keyFromDictValue(self.comboBox_period.currentText(), valid_periods)
        tickerwrapper: TickerWrapper
        for tickerwrapper in self.model.tickerlist.values():
            self.add_table_watchlist_row(tickerwrapper=tickerwrapper,period=period)

    def set_table_analysis_row_staticItems(self, methodArg: int, method: str, row: int):
        #TODO: get selected method from combobox!
        statistical_method_value = QTableWidgetItem()
        statistical_method_value.setData(Qt.EditRole, methodArg)
        self.table_analysis.setItem(row, TableAnalysisRows.METHODNAME.value, QTableWidgetItem(method))
        self.table_analysis.setItem(row, TableAnalysisRows.METHODVALUE.value, statistical_method_value)

    # add statistical method to table_analysis (analysislist)
    def add_table_analysis_row(self, methodArg: int, method: str) -> None:
        row = self.table_analysis.rowCount()
        self.table_analysis.insertRow(row)
        self.set_table_analysis_row_staticItems(methodArg=methodArg, method=method, row=row)

    # --------------------------------------------

    # add statistical methods to combobox, which contains all statistical methods
    def init_statMethods(self):
        self.comboBox_method.addItem("Moving Average")

    def init_intervals(self):
        for value in valid_periods.values():
            self.comboBox_period.addItem(value)

    def update_table_analysis(self, period: str):
        interval = setTickerArgs(period)
        for row in range(self.table_watchlist.rowCount()):
            tickersymbol = self.table_watchlist.item(row,TableWatchlistRows.SYMBOLNAME.value).text()
            self.set_table_watchlist_row_dynamicItems(tickerwrapper = self.model.tickerlist[tickersymbol], row = row, interval = interval)

    # sorts list based on input in search stock plainTextEdit 
    def handle_search_input_plainTextEdit_searchTicker(self):
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
    
################################################################################
## 
## helpfunction:
## get_plaintextedit_input
## 
## Description:
## returns value of plaintextedit_1_2_3 inputfield
################################################################################
    def get_plaintextedit_input(self, qPlainTextEdit: QPlainTextEdit):
        ret = qPlainTextEdit.toPlainText().strip()
        return ret

    def clear_input_field(self, qPlainTextEdit: QPlainTextEdit):
         qPlainTextEdit.clear()