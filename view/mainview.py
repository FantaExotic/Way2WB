from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox
from view.qt.mainframe import Ui_frame_main
from model import Model

class Mainview(QMainWindow, Ui_frame_main):
    def __init__(self, model: Model):
        super().__init__()
        self.setupUi(self)
        self.model = model
        self.plainTextEdit.installEventFilter(self)

    def handle_enter_press(self):
        input_text = self.plainTextEdit.toPlainText().strip()
        if input_text:
            # Clear the plainTextEdit
            self.plainTextEdit.clear()

            # Adding the data to tableWidget
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

            self.tableWidget.setItem(row_position, 0, QTableWidgetItem("Apple"))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem("AAPL"))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem("1234456"))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem("121"))

            analyze_checkbox = QCheckBox()
            analyze_checkbox.setChecked(True)
            self.tableWidget.setCellWidget(row_position, 4, analyze_checkbox)
