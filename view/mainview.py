from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox
from view.qt.mainframe import Ui_frame_main
from model import Model
from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QPlainTextEdit

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
        for index,each in enumerate(self.model.tickerlist):
            # Adding the data to tableWidget
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

            stockvalue = QTableWidgetItem() # very inefficient!!! Fix it!
            stockvalue.setData(Qt.EditRole, 1234)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(each.info["shortName"]))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(each.info["symbol"]))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(each.isin))
            self.tableWidget.setItem(row_position, 3, stockvalue)

    # add statistical method to tableWidget_2 (analysislist)
    def handle_enter_press_plainTextEdit_3(self):
        input_text = self.get_plaintextedit_input(self.plainTextEdit_3)
        if input_text:
            try:
                input_text_filtered = int(input_text)
                self.plainTextEdit_3.clear()

                # Adding the data to tableWidget
                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

                statistical_method_value = QTableWidgetItem()
                statistical_method_value.setData(Qt.EditRole, input_text_filtered)

                self.tableWidget_2.setItem(row_position, 0, QTableWidgetItem("Moving Average"))
                self.tableWidget_2.setItem(row_position, 1, statistical_method_value)
            except ValueError:
                print("Input needs to be of type integer!")

    # removes selected method from tablewidget_2
    def handle_delete_press_tableWidget_2(self):
        # Get the selected rows
        selected_rows = self.tableWidget_2.selectionModel().selectedRows()
        # Iterate through the selected rows in reverse order and delete them
        for index in sorted(selected_rows, reverse=True):
            self.tableWidget_2.removeRow(index.row())

    # adds stockdata to tablewidget (watchlist)
    def handle_enter_press_plainTextEdit(self,ticker):
        input_text = self.get_plaintextedit_input(self.plainTextEdit)
        if input_text:
            #data from model
            short_name = ticker.info['shortName']
            symbol = ticker.info['symbol']
            isin = ticker.isin
            # Clear the plainTextEdit
            self.plainTextEdit.clear()

            # Adding the data to tableWidget
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
        # Get the selected rows
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        symbolDeleteList = list()
        # Iterate through the selected rows in reverse order and delete them
        for index in sorted(selected_rows, reverse=True):
            symbolDeleteList.append(self.tableWidget.item(selected_rows, 1).text())
            self.tableWidget.removeRow(index.row())
        return symbolDeleteList

    # sorts list based on input in search stock plainTextEdit 
    def handle_search_input_plainTextEdit_2(self):
        search_text = self.get_plaintextedit_input(self.plainTextEdit_2)

        for row in range(self.tableWidget.rowCount()):
            stockname_item = self.tableWidget.item(row, 0)
            symbolname_item = self.tableWidget.item(row, 1)

            if stockname_item is not None and symbolname_item is not None:
                stockname = stockname_item.text().lower()
                symbolname = symbolname_item.text().lower()

                if search_text in stockname or search_text in symbolname:
                    self.tableWidget.setRowHidden(row, False)
                else:
                    self.tableWidget.setRowHidden(row, True)

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
