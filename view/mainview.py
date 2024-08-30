from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox
from view.qt.mainframe import Ui_frame_main
from model.model import Model
from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QPlainTextEdit
import yfinance as yf
from model.tickerwrapper import TickerWrapper
from utils.helpfunctions import *
from enum import Enum

class TableRow(Enum):
    SHORTNAME = 0
    SYMBOLNAME = 1
    ISIN = 2
    CURRENTVALUE = 3
    DELTAVALUE = 4
    CHECKBOX = 5

class Mainview(QMainWindow, Ui_frame_main):
    def __init__(self, model: Model):
        super().__init__()
        self.setupUi(self)
        self.model = model
        self.init_statMethods()
        self.init_intervals()
        self.init_tableWidget()

    # add statistical methods to combobox, which contains all statistical methods
    def init_statMethods(self):
        self.comboBox_method.addItem("Moving Average")
    
    def init_intervals(self):
        for key,value in valid_periods.items():
            self.comboBox_period.addItem(value)

    # init tableWidget based on self.model.tickerlist, which contains downloaded tickers from watchlist
    def init_tableWidget(self):
        for tickerwrapper in self.model.tickerlist:
            # Adding the data to tableWidget
            row_position = self.table_watchlist.rowCount()
            self.table_watchlist.insertRow(row_position)

            period = get_keyFromDictValue(self.comboBox_period.currentText(), valid_periods)
            interval = setTickerArgs(period)
            #TODO: get data for period '1d' before doing this!
            lastDataframeIndex = tickerwrapper.tickerhistory[interval].shape[0]-1

            openprice = tickerwrapper.tickerhistory['1m']['Open'].values[lastDataframeIndex].item()  #TODO: Interval '1m' hardcoded, need to get this from view instead
            stockvalue = QTableWidgetItem() # very inefficient!!! Fix it!
            stockvalue.setData(Qt.EditRole, openprice)
            self.table_watchlist.setItem(row_position, TableRow.SHORTNAME.value, QTableWidgetItem(tickerwrapper.ticker.info["shortName"]))
            self.table_watchlist.setItem(row_position, TableRow.SYMBOLNAME.value, QTableWidgetItem(tickerwrapper.ticker.info["symbol"]))
            #self.table_watchlist.setItem(row_position, 2, QTableWidgetItem(each.isin))
            self.table_watchlist.setItem(row_position, TableRow.ISIN.value, QTableWidgetItem("default ISIN"))
            self.table_watchlist.setItem(row_position, TableRow.CURRENTVALUE.value, stockvalue)
            
            #index 0 because we want difference to start of interval (e.g. start of month instead end of month)
            stockdiff = QTableWidgetItem()
            delta_start = tickerwrapper.tickerhistory[interval]['Open'].values[0].item()
            delta_end = openprice
            delta = delta_end/delta_start * 100 - 100
            stockdiff.setData(Qt.EditRole, delta)
            self.table_watchlist.setItem(row_position, TableRow.DELTAVALUE.value, stockdiff)

            # checkbox for analysis
            analyze_checkbox = QCheckBox()
            analyze_checkbox.setChecked(True)
            self.table_watchlist.setCellWidget(row_position, TableRow.CHECKBOX.value, analyze_checkbox)

    def handle_updateTickervalue(self, period: str):
        interval = setTickerArgs(period)
        for row in range(self.table_watchlist.rowCount()):
            for tickerwrapper in self.model.tickerlist:
                if tickerwrapper.ticker.info["symbol"] == self.table_watchlist.item(row,1).text():
                    lastDataframeIndex = tickerwrapper.tickerhistory['1m'].shape[0]-1
                    openprice = tickerwrapper.tickerhistory['1m']['Open'].values[lastDataframeIndex].item()
                    stockvalue = QTableWidgetItem() # very inefficient!!! Fix it!
                    stockvalue.setData(Qt.EditRole, openprice)
                    self.table_watchlist.setItem(row, TableRow.CURRENTVALUE.value, stockvalue)

                    #index 0 because we want difference to start of interval (e.g. start of month instead end of month)
                    stockdiff = QTableWidgetItem()
                    try:
                        delta_start = tickerwrapper.tickerhistory[interval]['Open'].values[0].item()
                        delta_end = openprice
                        delta = delta_end/delta_start * 100 - 100
                        stockdiff.setData(Qt.EditRole, delta)
                        self.table_watchlist.setItem(row, TableRow.DELTAVALUE.value, stockdiff)
                    except:
                        print(f'Stockdata for {tickerwrapper.ticker.info["symbol"]} doesnt exist for this period! Select a shorted period!')
                        self.table_watchlist.setItem(row, TableRow.DELTAVALUE.value, None)
                    #TODO: get data for selected period and compare to current tickervalue!
                    #TODO: iterate through rows in tableWidget instead!

    # add statistical method to table_analysis (analysislist)
    def handle_enter_press_plainTextEdit_methodinput(self) -> list:
        input_text = self.get_plaintextedit_input(self.plainTextEdit_methodinput)
        if not input_text:
            print("no inputtext entered for adding statistical method!")
            return []
        
        try:
            input_text_filtered = int(input_text)
        except ValueError:
            print("input value for adding statistical method is not an integer!")
            return []

        # Adding the data to tableWidget
        row_position = self.table_analysis.rowCount()
        self.table_analysis.insertRow(row_position)
        statistical_method_value = QTableWidgetItem()
        statistical_method_value.setData(Qt.EditRole, input_text_filtered)
        self.table_analysis.setItem(row_position, 0, QTableWidgetItem("Moving Average"))
        self.table_analysis.setItem(row_position, 1, statistical_method_value)
        ret_statMethodName = self.table_analysis.item(row_position, 0).text()
        ret_statMethodArgs = self.table_analysis.item(row_position, 1).text()
        return [ret_statMethodName, ret_statMethodArgs]

    # removes selected method from table_analysis
    def handle_delete_press_table_analysis(self):
        # Get the selected rows
        selected_row = self.table_analysis.currentRow()
        #TODO: use also here predefined values to determine which row is for name, args etc.
        statMethodName = self.table_analysis.item(selected_row,0).text()
        statMethodArgs = self.table_analysis.item(selected_row,1).text()
        self.table_analysis.removeRow(selected_row)
        return [statMethodName,statMethodArgs]

    # adds stockdata to tablewidget (watchlist)
    def handle_enter_press_plainTextEdit_addTicker(self,tickerwrapper: TickerWrapper):
        input_text = self.get_plaintextedit_input(self.plainTextEdit_addTicker)
        if not input_text:
            print("no inputtext provided to add ticker")
            return
        
        #get info from ticker object
        short_name = tickerwrapper.ticker.info['shortName']
        symbol = tickerwrapper.ticker.info['symbol']
        isin = tickerwrapper.ticker.isin

        # Adding the data to tableWidget
        row_position = self.table_watchlist.rowCount()
        self.table_watchlist.insertRow(row_position)
        stockvalue = QTableWidgetItem()
        stockvalue.setData(Qt.EditRole, 1234)
        self.table_watchlist.setItem(row_position, 0, QTableWidgetItem(short_name))
        self.table_watchlist.setItem(row_position, 1, QTableWidgetItem(symbol))
        #self.table_watchlist.setItem(row_position, 2, QTableWidgetItem(isin))
        self.table_watchlist.setItem(row_position, 2, QTableWidgetItem("default ISIN"))
        self.table_watchlist.setItem(row_position, 3, stockvalue)
        analyze_checkbox = QCheckBox()
        analyze_checkbox.setChecked(True)
        self.table_watchlist.setCellWidget(row_position, 5, analyze_checkbox)

    # removes selected stock from tablewidget
    def handle_delete_press_tableWidget(self):
        # Get the selected row
        selected_row = self.table_watchlist.currentRow()
        # TODO: add variable for columnposition of symbol, shortname, isin, etc.
        removedSymbol = self.table_watchlist.item(selected_row,TableRow.SYMBOLNAME.value).text()
        self.table_watchlist.removeRow(selected_row)
        return removedSymbol

    # sorts list based on input in search stock plainTextEdit 
    def handle_search_input_plainTextEdit_searchTicker(self):
        search_text = self.get_plaintextedit_input(self.plainTextEdit_searchTicker)

        for row in range(self.table_watchlist.rowCount()):
            stockname_item = self.table_watchlist.item(row, TableRow.SHORTNAME.value)
            symbolname_item = self.table_watchlist.item(row, TableRow.SYMBOLNAME.value)

            if stockname_item is None or symbolname_item is None:
                print("stockname or symbolname == None!")
                continue

            stockname = stockname_item.text().lower()
            symbolname = symbolname_item.text().lower()
            if search_text in stockname or search_text in symbolname:
                self.table_watchlist.setRowHidden(row, False)
            else:
                self.table_watchlist.setRowHidden(row, True)
                    
    # function to get all selected checkboxes from watchlist, which shall be used for analysis and graph generation
    def get_selected_Checkboxes(self) -> list:
        ret = []
        for row in range(self.table_watchlist.rowCount()):
            #TODO: use variables here to determine which column
            symbol = self.table_watchlist.item(row, TableRow.SYMBOLNAME.value).text()
            checkbox = self.table_watchlist.cellWidget(row, TableRow.CHECKBOX.value)
            if checkbox.isChecked():
                ret.append(symbol)
        return ret
    
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