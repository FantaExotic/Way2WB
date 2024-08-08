from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox
from view.qt.mainframe import Ui_frame_main
from model import Model
from PySide6.QtCore import Qt, QEvent

class Mainview(QMainWindow, Ui_frame_main):
    def __init__(self, model: Model):
        super().__init__()
        self.setupUi(self)
        self.model = model
        self.init_statMethods()

    # add statistical methods to combobox, which contains all statistical methods
    def init_statMethods(self):
        self.comboBox.addItem("Moving Average")

    # add statistical method to tableWidget_2 (analysislist)
    def handle_enter_press_plainTextEdit_3(self):
        input_text = self.plainTextEdit_3.toPlainText().strip()
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
    def handle_enter_press_plainTextEdit(self):
        input_text = self.plainTextEdit.toPlainText().strip()
        if input_text:
            # Clear the plainTextEdit
            self.plainTextEdit.clear()

            # Adding the data to tableWidget
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

            stockvalue = QTableWidgetItem()
            stockvalue.setData(Qt.EditRole, 1234)

            self.tableWidget.setItem(row_position, 0, QTableWidgetItem("Apple"))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem("AAPL"))
            self.tableWidget.setItem(row_position, 2, stockvalue)
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem("121"))

            analyze_checkbox = QCheckBox()
            analyze_checkbox.setChecked(True)
            self.tableWidget.setCellWidget(row_position, 4, analyze_checkbox)

    # removes selected stock from tablewidget
    def handle_delete_press_tableWidget(self):
        # Get the selected rows
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        # Iterate through the selected rows in reverse order and delete them
        for index in sorted(selected_rows, reverse=True):
            self.tableWidget.removeRow(index.row())

    # sorts list based on input in search stock plainTextEdit 
    def handle_search_input_plainTextEdit_2(self):
        search_text = self.plainTextEdit_2.toPlainText().strip().lower()

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