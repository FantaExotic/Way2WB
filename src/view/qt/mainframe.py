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
    QStackedWidget, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_frame_main(object):
    def setupUi(self, frame_main):
        if not frame_main.objectName():
            frame_main.setObjectName(u"frame_main")
        frame_main.resize(1068, 699)
        self.centralwidget = QWidget(frame_main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setToolTipDuration(-1)
        self.centralwidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.centralwidget.setAutoFillBackground(False)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(9, 9, 1151, 661))
        self.page_startup = QWidget()
        self.page_startup.setObjectName(u"page_startup")
        self.label_watchlistpath_startup = QLabel(self.page_startup)
        self.label_watchlistpath_startup.setObjectName(u"label_watchlistpath_startup")
        self.label_watchlistpath_startup.setGeometry(QRect(490, 310, 161, 161))
        self.label_watchlistpath_startup.setWordWrap(True)
        self.label_watchlist_startup = QLabel(self.page_startup)
        self.label_watchlist_startup.setObjectName(u"label_watchlist_startup")
        self.label_watchlist_startup.setGeometry(QRect(540, 270, 51, 21))
        self.button_selectWatchlist = QPushButton(self.page_startup)
        self.button_selectWatchlist.setObjectName(u"button_selectWatchlist")
        self.button_selectWatchlist.setGeometry(QRect(500, 200, 131, 51))
        self.button_startAppliction = QPushButton(self.page_startup)
        self.button_startAppliction.setObjectName(u"button_startAppliction")
        self.button_startAppliction.setGeometry(QRect(450, 90, 231, 61))
        self.button_createWatchlist = QPushButton(self.page_startup)
        self.button_createWatchlist.setObjectName(u"button_createWatchlist")
        self.button_createWatchlist.setGeometry(QRect(690, 210, 111, 31))
        self.stackedWidget.addWidget(self.page_startup)
        self.page_main = QWidget()
        self.page_main.setObjectName(u"page_main")
        self.tabWidget = QTabWidget(self.page_main)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(8, 19, 961, 641))
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
        self.table_watchlist.setGeometry(QRect(-1, -1, 765, 621))
        self.table_watchlist.setSortingEnabled(True)
        self.button_genGraph = QPushButton(self.tab_watchlist)
        self.button_genGraph.setObjectName(u"button_genGraph")
        self.button_genGraph.setGeometry(QRect(790, 10, 131, 81))
        self.plainTextEdit_addTicker = QPlainTextEdit(self.tab_watchlist)
        self.plainTextEdit_addTicker.setObjectName(u"plainTextEdit_addTicker")
        self.plainTextEdit_addTicker.setGeometry(QRect(780, 240, 151, 31))
        self.label_searchTicker = QLabel(self.tab_watchlist)
        self.label_searchTicker.setObjectName(u"label_searchTicker")
        self.label_searchTicker.setGeometry(QRect(810, 130, 81, 16))
        self.label_addTicker = QLabel(self.tab_watchlist)
        self.label_addTicker.setObjectName(u"label_addTicker")
        self.label_addTicker.setGeometry(QRect(790, 210, 131, 21))
        self.comboBox_period = QComboBox(self.tab_watchlist)
        self.comboBox_period.setObjectName(u"comboBox_period")
        self.comboBox_period.setGeometry(QRect(770, 360, 181, 31))
        self.plainTextEdit_searchTicker = QPlainTextEdit(self.tab_watchlist)
        self.plainTextEdit_searchTicker.setObjectName(u"plainTextEdit_searchTicker")
        self.plainTextEdit_searchTicker.setGeometry(QRect(780, 160, 151, 31))
        self.label_period = QLabel(self.tab_watchlist)
        self.label_period.setObjectName(u"label_period")
        self.label_period.setGeometry(QRect(820, 320, 81, 21))
        self.label_watchlistpath = QLabel(self.tab_watchlist)
        self.label_watchlistpath.setObjectName(u"label_watchlistpath")
        self.label_watchlistpath.setGeometry(QRect(780, 460, 161, 111))
        self.label_watchlist = QLabel(self.tab_watchlist)
        self.label_watchlist.setObjectName(u"label_watchlist")
        self.label_watchlist.setGeometry(QRect(830, 420, 51, 21))
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
        self.table_analysis.setGeometry(QRect(2, 2, 541, 739))
        self.comboBox_method = QComboBox(self.tab_analysis)
        self.comboBox_method.setObjectName(u"comboBox_method")
        self.comboBox_method.setGeometry(QRect(670, 160, 181, 31))
        self.label_method = QLabel(self.tab_analysis)
        self.label_method.setObjectName(u"label_method")
        self.label_method.setGeometry(QRect(700, 130, 111, 21))
        self.plainTextEdit_methodinput = QPlainTextEdit(self.tab_analysis)
        self.plainTextEdit_methodinput.setObjectName(u"plainTextEdit_methodinput")
        self.plainTextEdit_methodinput.setGeometry(QRect(700, 290, 111, 31))
        self.label_methodinput = QLabel(self.tab_analysis)
        self.label_methodinput.setObjectName(u"label_methodinput")
        self.label_methodinput.setGeometry(QRect(720, 260, 111, 21))
        self.tabWidget.addTab(self.tab_analysis, "")
        self.stackedWidget.addWidget(self.page_main)
        frame_main.setCentralWidget(self.centralwidget)

        self.retranslateUi(frame_main)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(frame_main)
    # setupUi

    def retranslateUi(self, frame_main):
        frame_main.setWindowTitle(QCoreApplication.translate("frame_main", u"Way2WarrenBuffett", None))
        self.label_watchlistpath_startup.setText("")
        self.label_watchlist_startup.setText(QCoreApplication.translate("frame_main", u"Watchlist", None))
        self.button_selectWatchlist.setText(QCoreApplication.translate("frame_main", u"Select Watchlist", None))
        self.button_startAppliction.setText(QCoreApplication.translate("frame_main", u"Start the way to Warren Buffett", None))
        self.button_createWatchlist.setText(QCoreApplication.translate("frame_main", u"Create Watchlist", None))
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
        self.button_genGraph.setText(QCoreApplication.translate("frame_main", u"Generate Graph", None))
        self.label_searchTicker.setText(QCoreApplication.translate("frame_main", u"Search ticker", None))
        self.label_addTicker.setText(QCoreApplication.translate("frame_main", u"Add ticker to watchlist", None))
        self.label_period.setText(QCoreApplication.translate("frame_main", u"Time period", None))
        self.label_watchlistpath.setText("")
        self.label_watchlist.setText(QCoreApplication.translate("frame_main", u"Watchlist", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_watchlist), QCoreApplication.translate("frame_main", u"Configure Watchlist", None))
        ___qtablewidgetitem6 = self.table_analysis.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("frame_main", u"Method", None));
        ___qtablewidgetitem7 = self.table_analysis.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("frame_main", u"Value", None));
        self.label_method.setText(QCoreApplication.translate("frame_main", u"Statistical Method", None))
        self.label_methodinput.setText(QCoreApplication.translate("frame_main", u"Input value", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_analysis), QCoreApplication.translate("frame_main", u"Configure Analysis", None))
    # retranslateUi

