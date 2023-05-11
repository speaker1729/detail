# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'container-cuser.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import pymysql
import Module.Logger as Logger
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
                               QPushButton, QSizePolicy, QWidget, QMainWindow)
from PySide6 import QtCore
import os


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(798, 563)
        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(30, 70, 211, 341))
        self.listWidget_2 = QListWidget(Form)
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setGeometry(QRect(280, 70, 211, 341))
        self.listWidget_3 = QListWidget(Form)
        self.listWidget_3.setObjectName(u"listWidget_3")
        self.listWidget_3.setGeometry(QRect(530, 70, 211, 341))
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(90, 450, 111, 51))
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(340, 450, 111, 51))
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 40, 81, 21))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(300, 40, 81, 21))
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(550, 40, 81, 21))
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(580, 450, 121, 51))

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.add)
        self.pushButton_2.clicked.connect(Form.delete)
        self.pushButton_3.clicked.connect(Form.deleteall)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u589e\u52a0\u6587\u4ef6\u6743\u9650", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u6587\u4ef6\u6743\u9650", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u7528\u6237\u89c6\u56fe", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u89c6\u56fe", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u7528\u6237\u6587\u4ef6\u89c6\u56fe", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"\u4ece\u5e93\u4e2d\u5220\u9664\u6587\u4ef6", None))

    # retranslateUi


class containercuser(QMainWindow):
    def __init__(self, base):
        super().__init__()
        self.lw_data=None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.dbmain = base
        db = pymysql.connect(host='172.20.10.8', user='root', passwd='gfnb3017', database='myproject')
        cursor = db.cursor()
        sql = "SELECT Name FROM Persons WHERE Name!='NULL' and isAdmin=0"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            self.ui.listWidget.addItem(row[0])
        sql2 = "SELECT * FROM filetable"
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        for row in results2:
            self.ui.listWidget_2.addItem(row[0])
        self.ui.listWidget.itemClicked.connect(self.cache1)
        self.ui.listWidget_2.itemClicked.connect(self.cache)
        db.close()

    @QtCore.Slot()
    def cache1(self):
        self.lw_data=self.ui.listWidget.selectedItems()
        self.changeview()
    @QtCore.Slot()
    def cache(self):
        self.lw2_data = self.ui.listWidget_2.selectedItems()

    @QtCore.Slot()
    def add(self):
        db = pymysql.connect(host='172.20.10.8', user='root', passwd='gfnb3017', database='myproject')
        cursor = db.cursor()
        sql_0 = "select PersonID from persons where Name=%s"
        cursor.execute(sql_0, (self.lw_data[0].text()))
        data = cursor.fetchone()
        sql = "insert into personfile values(%s,%s)"
        cursor.execute(sql, (data, self.lw2_data[0].text()))
        Logger.log_save(f'用户{data[0]}被{self.dbmain.user_cur}授予访问{self.lw2_data[0].text()}的权限')
        db.commit()
        self.changeview()
        db.close()

    @QtCore.Slot()
    def delete(self):
        db = pymysql.connect(host='172.20.10.8', user='root', passwd='gfnb3017', database='myproject')
        cursor = db.cursor()
        sql_0 = "select PersonID from persons where Name=%s"
        cursor.execute(sql_0, (self.lw_data[0].text()))
        data = cursor.fetchone()
        sql = "delete from personfile where PersonID=%s and Filepath=%s"
        cursor.execute(sql, (data[0], self.lw2_data[0].text()))
        Logger.log_save(f'用户{data[0]}访问{self.lw2_data[0].text()}的权限被{self.dbmain.user_cur}删除')
        db.commit()
        self.changeview()
        db.close()

    @QtCore.Slot()
    def deleteall(self):
        db = pymysql.connect(host='172.20.10.8', user='root', passwd='gfnb3017', database='myproject')
        cursor = db.cursor()
        sql="delete from filetable where filename=%s"
        cursor.execute(sql,(self.lw2_data[0].text()))
        sql="delete from personfile where FilePath=%s"
        cursor.execute(sql,(self.lw2_data[0].text()))
        os.remove("Data/"+self.lw2_data[0].text())
        Logger.log_save(f'用户{self.dbmain.user_cur}将{self.lw2_data[0].text()}从库中删除')
        db.commit()
        self.changeview()
        self.change_wiget2_view()
        self.dbmain.m_adminwindow.wigcfile.downview()
        db.close()

    @QtCore.Slot()
    def changeview(self):
        if self.lw_data==None:
            return
        self.ui.listWidget_3.clear()
        db = pymysql.connect(host='172.20.10.8', user='root', passwd='gfnb3017', database='myproject')
        cursor = db.cursor()
        sql = "select PersonID,isAdmin from persons where Name=%s"
        cursor.execute(sql, (self.lw_data[0].text()))
        data = cursor.fetchone()
        if data[1] == False:
            sql = "SELECT Filepath FROM personfile WHERE PersonID=%s"
            cursor.execute(sql, (data[0]))
        else:
            sql = "select * from filetable"
            cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            self.ui.listWidget_3.addItem(row[0])
        db.close()

    def change_wiget2_view(self):
        self.ui.listWidget_2.clear()
        db = pymysql.connect(host='172.20.10.8', user='root', passwd='gfnb3017', database='myproject')
        cursor = db.cursor()
        sql2 = "SELECT * FROM filetable"
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        for row in results2:
            self.ui.listWidget_2.addItem(row[0])
        db.close()
