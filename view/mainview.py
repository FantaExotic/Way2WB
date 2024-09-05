from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QCheckBox, QTableWidget
from view.qt.mainframe import Ui_frame_main
from model.model import Model
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPlainTextEdit
from model.tickerwrapper import TickerWrapper
from utils.helpfunctions import *
from enum import Enum

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

class Mainview(QMainWindow, Ui_frame_main):
    def __init__(self, model: Model):
        super().__init__()
        self.setupUi(self)
        self.model = model
        self._init_statMethods()
        self._init_intervals()
        self._init_table_watchlist()

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

    def add_table_watchlist_row(self, tickerwrapper: TickerWrapper, period: str):
        """ adds new row to table watchlist and sets the according values to all columns in the added row"""
        row = self.table_watchlist.rowCount()
        self.table_watchlist.insertRow(row)
        interval = setTickerArgs(period)
        self._set_table_watchlist_row_staticItems(tickerwrapper=tickerwrapper,row=row)
        self._set_table_watchlist_row_dynamicItems(tickerwrapper=tickerwrapper,row=row,interval=interval)

    def add_table_analysis_row(self, methodArg: int, method: str) -> None:
        """adds new row to table analysis and sets the according values to all columns in the added row"""
        row = self.table_analysis.rowCount()
        self.table_analysis.insertRow(row)
        self._set_table_analysis_row_staticItems(methodArg=methodArg, method=method, row=row)

    def update_table_analysis(self, period: str):
        """updates dynamic items in each row. Dynamic items are items, which will be update during runtime
            by the liveticker (e.g.: currentValue and deltavalue)"""
        interval = setTickerArgs(period)
        for row in range(self.table_watchlist.rowCount()):
            tickersymbol = self.table_watchlist.item(row,TableWatchlistRows.SYMBOLNAME.value).text()
            self._set_table_watchlist_row_dynamicItems(tickerwrapper = self.model.tickerlist[tickersymbol], row = row, interval = interval)

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

    """private functions"""

    def _set_table_watchlist_row_staticItems(self, tickerwrapper: TickerWrapper, row: int): #TODO: change datatype for interval! create own datatype for available intervals
        """Updates static items in table watchlist, which only need to be set once"""
        self.table_watchlist.setItem(row, TableWatchlistRows.SHORTNAME.value, QTableWidgetItem(tickerwrapper.ticker.info["shortName"]))
        self.table_watchlist.setItem(row, TableWatchlistRows.SYMBOLNAME.value, QTableWidgetItem(tickerwrapper.ticker.info["symbol"]))
        self.table_watchlist.setItem(row, TableWatchlistRows.ISIN.value, QTableWidgetItem(tickerwrapper.ticker.isin))
        analyze_checkbox = QCheckBox()
        analyze_checkbox.setChecked(False)
        self.table_watchlist.setCellWidget(row, TableWatchlistRows.CHECKBOX.value, analyze_checkbox)

    def _set_table_watchlist_row_dynamicItems(self, tickerwrapper: TickerWrapper, row: int, interval: str): #TODO: change datatype for interval! create own datatype for available intervals
        """Updates dynamic items in table watchlist, which will be updated dynamically based on data from liveticker"""
        lastDataframeIndex = tickerwrapper.tickerhistory['1m'].shape[0]-1
        openprice = tickerwrapper.tickerhistory['1m']['Open'].values[lastDataframeIndex].item()
        stockvalue = QTableWidgetItem() # very inefficient!
        stockvalue.setData(Qt.EditRole, openprice)
        self.table_watchlist.setItem(row, TableWatchlistRows.CURRENTVALUE.value, stockvalue)
        stockdiff = QTableWidgetItem()
        delta_start = tickerwrapper.tickerhistory[interval]['Open'].values[0].item() #index 0 because we want difference to start of interval
        delta_end = openprice
        delta = delta_end/delta_start * 100 - 100
        stockdiff.setData(Qt.EditRole, delta)
        self.table_watchlist.setItem(row, TableWatchlistRows.DELTAVALUE.value, stockdiff)

    def _init_statMethods(self):
        """Add methods to comboBox method"""
        self.comboBox_method.addItem("Moving Average")

    def _init_intervals(self):
        """Init comboBox period with all periods from yfinance"""
        for value in valid_periods.values():
            self.comboBox_period.addItem(value)

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
        period = get_keyFromDictValue(self.comboBox_period.currentText(), valid_periods)
        tickerwrapper: TickerWrapper
        for tickerwrapper in self.model.tickerlist.values():
            self.add_table_watchlist_row(tickerwrapper=tickerwrapper,period=period)

    def _set_table_analysis_row_staticItems(self, methodArg: int, method: str, row: int):
        """Set method and methodArg for corresponding row in table analysis"""
        statistical_method_value = QTableWidgetItem()
        statistical_method_value.setData(Qt.EditRole, methodArg)
        self.table_analysis.setItem(row, TableAnalysisRows.METHODNAME.value, QTableWidgetItem(method))
        self.table_analysis.setItem(row, TableAnalysisRows.METHODVALUE.value, statistical_method_value)