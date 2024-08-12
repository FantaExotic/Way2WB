from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox
from view.qt.mainframe import Ui_frame_main
from model import Model
from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QPlainTextEdit
import yfinance as yf

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
        self.comboBox.addItem("Moving Average")
    
    def init_intervals(self):
        for key,value in self.model.valid_periods.items():
            self.comboBox_2.addItem(value)

    # init tableWidget based on self.model.tickerlist, which contains downloaded tickers from watchlist
    def init_tableWidget(self):
        for each in self.model.tickerlist:
            # Adding the data to tableWidget
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

            stockvalue = QTableWidgetItem() # very inefficient!!! Fix it!
            stockvalue.setData(Qt.EditRole, 1234)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(each.info["shortName"]))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(each.info["symbol"]))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(each.isin))
            self.tableWidget.setItem(row_position, 3, stockvalue)
            
            # checkbox for analysis
            analyze_checkbox = QCheckBox()
            analyze_checkbox.setChecked(True)
            self.tableWidget.setCellWidget(row_position, 4, analyze_checkbox)

    # add statistical method to tableWidget_2 (analysislist)
    def handle_enter_press_plainTextEdit_3(self) -> list:
        input_text = self.get_plaintextedit_input(self.plainTextEdit_3)
        if not input_text:
            print("no inputtext entered for adding statistical method!")
            return []
        
        try:
            input_text_filtered = int(input_text)
        except ValueError:
            print("input value for adding statistical method is not an integer!")
            return []

        self.plainTextEdit_3.clear()
        # Adding the data to tableWidget
        row_position = self.tableWidget_2.rowCount()
        self.tableWidget_2.insertRow(row_position)
        statistical_method_value = QTableWidgetItem()
        statistical_method_value.setData(Qt.EditRole, input_text_filtered)
        self.tableWidget_2.setItem(row_position, 0, QTableWidgetItem("Moving Average"))
        self.tableWidget_2.setItem(row_position, 1, statistical_method_value)
        ret_statMethodName = self.tableWidget_2.item(row_position, 0).text()
        ret_statMethodArgs = self.tableWidget_2.item(row_position, 1).text()
        return [ret_statMethodName, ret_statMethodArgs]

    # removes selected method from tablewidget_2
    def handle_delete_press_tableWidget_2(self):
        # Get the selected rows
        selected_row = self.tableWidget_2.currentRow()
        #TODO: use also here predefined values to determine which row is for name, args etc.
        statMethodName = self.tableWidget_2.item(selected_row,0).text()
        statMethodArgs = self.tableWidget_2.item(selected_row,1).text()
        self.tableWidget_2.removeRow(selected_row)
        return [statMethodName,statMethodArgs]

    # adds stockdata to tablewidget (watchlist)
    def handle_enter_press_plainTextEdit(self,ticker: yf.Ticker):
        input_text = self.get_plaintextedit_input(self.plainTextEdit)
        if not input_text:
            print("no inputtext provided to add ticker")
            return
        
        #get info from ticker object
        short_name = ticker.info['shortName']
        symbol = ticker.info['symbol']
        isin = ticker.isin

        # Adding the data to tableWidget
        self.plainTextEdit.clear()
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        stockvalue = QTableWidgetItem()
        stockvalue.setData(Qt.EditRole, 1234)
        self.tableWidget.setItem(row_position, 0, QTableWidgetItem(short_name))
        self.tableWidget.setItem(row_position, 1, QTableWidgetItem(symbol))
        self.tableWidget.setItem(row_position, 2, QTableWidgetItem(isin))
        self.tableWidget.setItem(row_position, 3, stockvalue)
        analyze_checkbox = QCheckBox()
        analyze_checkbox.setChecked(True)
        self.tableWidget.setCellWidget(row_position, 4, analyze_checkbox)

    # removes selected stock from tablewidget
    def handle_delete_press_tableWidget(self):
        # Get the selected row
        selected_row = self.tableWidget.currentRow()
        # TODO: add variable for columnposition of symbol, shortname, isin, etc.
        removedSymbol = self.tableWidget.item(selected_row,1).text()
        self.tableWidget.removeRow(selected_row)
        return removedSymbol

    # sorts list based on input in search stock plainTextEdit 
    def handle_search_input_plainTextEdit_2(self):
        search_text = self.get_plaintextedit_input(self.plainTextEdit_2)

        for row in range(self.tableWidget.rowCount()):
            stockname_item = self.tableWidget.item(row, 0)
            symbolname_item = self.tableWidget.item(row, 1)

            if stockname_item is None or symbolname_item is None:
                print("stockname or symbolname == None!")
                continue

            stockname = stockname_item.text().lower()
            symbolname = symbolname_item.text().lower()
            if search_text in stockname or search_text in symbolname:
                self.tableWidget.setRowHidden(row, False)
            else:
                self.tableWidget.setRowHidden(row, True)
                    
    # function to get all selected checkboxes from watchlist, which shall be used for analysis and graph generation
    def get_selected_Checkboxes(self) -> list:
        ret = []
        for row in range(self.tableWidget.rowCount()):
            #TODO: use variables here to determine which column
            symbol = self.tableWidget.item(row, 1).text()
            checkbox = self.tableWidget.cellWidget(row, 4)
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
