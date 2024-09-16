# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainframe.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHeaderView, QLabel,
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy,
    QTabWidget, QTableWidget, QTableWidgetItem, QWidget)

class Ui_frame_main(object):
    def setupUi(self, frame_main):
        if not frame_main.objectName():
            frame_main.setObjectName(u"frame_main")
        frame_main.resize(1044, 837)
        self.centralwidget = QWidget(frame_main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.button_genGraph = QPushButton(self.centralwidget)
        self.button_genGraph.setObjectName(u"button_genGraph")
        self.button_genGraph.setGeometry(QRect(800, 30, 131, 81))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(20, 20, 761, 681))
        self.tab_watchlist = QWidget()
        self.tab_watchlist.setObjectName(u"tab_watchlist")
        self.table_watchlist = QTableWidget(self.tab_watchlist)
        if (self.table_watchlist.columnCount() < 6):
            self.table_watchlist.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_watchlist.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_watchlist.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_watchlist.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_watchlist.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_watchlist.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_watchlist.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.table_watchlist.setObjectName(u"table_watchlist")
        self.table_watchlist.setGeometry(QRect(20, 50, 711, 581))
        self.table_watchlist.setSortingEnabled(True)
        self.tabWidget.addTab(self.tab_watchlist, "")
        self.tab_analysis = QWidget()
        self.tab_analysis.setObjectName(u"tab_analysis")
        self.table_analysis = QTableWidget(self.tab_analysis)
        if (self.table_analysis.columnCount() < 2):
            self.table_analysis.setColumnCount(2)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_analysis.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_analysis.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        self.table_analysis.setObjectName(u"table_analysis")
        self.table_analysis.setGeometry(QRect(40, 50, 491, 531))
        self.comboBox_method = QComboBox(self.tab_analysis)
        self.comboBox_method.setObjectName(u"comboBox_method")
        self.comboBox_method.setGeometry(QRect(550, 100, 181, 31))
        self.label_method = QLabel(self.tab_analysis)
        self.label_method.setObjectName(u"label_method")
        self.label_method.setGeometry(QRect(580, 70, 111, 21))
        self.plainTextEdit_methodinput = QPlainTextEdit(self.tab_analysis)
        self.plainTextEdit_methodinput.setObjectName(u"plainTextEdit_methodinput")
        self.plainTextEdit_methodinput.setGeometry(QRect(580, 230, 111, 31))
        self.label_methodinput = QLabel(self.tab_analysis)
        self.label_methodinput.setObjectName(u"label_methodinput")
        self.label_methodinput.setGeometry(QRect(600, 200, 111, 21))
        self.tabWidget.addTab(self.tab_analysis, "")
        self.label_addTicker = QLabel(self.centralwidget)
        self.label_addTicker.setObjectName(u"label_addTicker")
        self.label_addTicker.setGeometry(QRect(820, 250, 131, 21))
        self.plainTextEdit_addTicker = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_addTicker.setObjectName(u"plainTextEdit_addTicker")
        self.plainTextEdit_addTicker.setGeometry(QRect(810, 280, 151, 31))
        self.plainTextEdit_searchTicker = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_searchTicker.setObjectName(u"plainTextEdit_searchTicker")
        self.plainTextEdit_searchTicker.setGeometry(QRect(810, 200, 141, 31))
        self.label_searchTicker = QLabel(self.centralwidget)
        self.label_searchTicker.setObjectName(u"label_searchTicker")
        self.label_searchTicker.setGeometry(QRect(840, 170, 81, 16))
        self.comboBox_period = QComboBox(self.centralwidget)
        self.comboBox_period.setObjectName(u"comboBox_period")
        self.comboBox_period.setGeometry(QRect(790, 400, 181, 31))
        self.label_period = QLabel(self.centralwidget)
        self.label_period.setObjectName(u"label_period")
        self.label_period.setGeometry(QRect(840, 370, 81, 21))
        frame_main.setCentralWidget(self.centralwidget)

        self.retranslateUi(frame_main)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(frame_main)
    # setupUi

    def retranslateUi(self, frame_main):
        frame_main.setWindowTitle(QCoreApplication.translate("frame_main", u"Way2WarrenBuffett", None))
        self.button_genGraph.setText(QCoreApplication.translate("frame_main", u"Generate Graph", None))
        ___qtablewidgetitem = self.table_watchlist.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("frame_main", u"Stockname", None));
        ___qtablewidgetitem1 = self.table_watchlist.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("frame_main", u"Symbolname", None));
        ___qtablewidgetitem2 = self.table_watchlist.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("frame_main", u"ISIN", None));
        ___qtablewidgetitem3 = self.table_watchlist.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("frame_main", u"Current Value", None));
        ___qtablewidgetitem4 = self.table_watchlist.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("frame_main", u"Delta", None));
        ___qtablewidgetitem5 = self.table_watchlist.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("frame_main", u"Analyze", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_watchlist), QCoreApplication.translate("frame_main", u"Configure Watchlist", None))
        ___qtablewidgetitem6 = self.table_analysis.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("frame_main", u"Method", None));
        ___qtablewidgetitem7 = self.table_analysis.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("frame_main", u"Value", None));
        self.label_method.setText(QCoreApplication.translate("frame_main", u"Statistical Method", None))
        self.label_methodinput.setText(QCoreApplication.translate("frame_main", u"Input value", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_analysis), QCoreApplication.translate("frame_main", u"Configure Analysis", None))
        self.label_addTicker.setText(QCoreApplication.translate("frame_main", u"Add ticker to watchlist", None))
        self.label_searchTicker.setText(QCoreApplication.translate("frame_main", u"Search ticker", None))
        self.label_period.setText(QCoreApplication.translate("frame_main", u"Time period", None))
    # retranslateUi

