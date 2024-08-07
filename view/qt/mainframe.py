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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_frame_main(object):
    def setupUi(self, frame_main):
        if not frame_main.objectName():
            frame_main.setObjectName(u"frame_main")
        frame_main.resize(984, 773)
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
        self.tableWidget = QTableWidget(self.tab_watchlist)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(20, 30, 701, 591))
        self.tabWidget.addTab(self.tab_watchlist, "")
        self.tab_analysis = QWidget()
        self.tab_analysis.setObjectName(u"tab_analysis")
        self.pushButton_2 = QPushButton(self.tab_analysis)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(250, 170, 75, 24))
        self.tabWidget.addTab(self.tab_analysis, "")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(800, 160, 131, 21))
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(790, 190, 151, 31))
        frame_main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(frame_main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 984, 22))
        frame_main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(frame_main)
        self.statusbar.setObjectName(u"statusbar")
        frame_main.setStatusBar(self.statusbar)

        self.retranslateUi(frame_main)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(frame_main)
    # setupUi

    def retranslateUi(self, frame_main):
        frame_main.setWindowTitle(QCoreApplication.translate("frame_main", u"MainWindow", None))
        self.button_genGraph.setText(QCoreApplication.translate("frame_main", u"Generate Graph", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("frame_main", u"Stockname", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("frame_main", u"Symbolname", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("frame_main", u"ISIN", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("frame_main", u"Value", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("frame_main", u"Analyze", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_watchlist), QCoreApplication.translate("frame_main", u"Configure Watchlist", None))
        self.pushButton_2.setText(QCoreApplication.translate("frame_main", u"button2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_analysis), QCoreApplication.translate("frame_main", u"Configure Analysis", None))
        self.label.setText(QCoreApplication.translate("frame_main", u"add symbol to watchlist", None))
    # retranslateUi

