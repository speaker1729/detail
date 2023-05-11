# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'enroll.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QWidget, QMainWindow)
from PySide6 import QtCore
import pymysql

class Ui_enroll(object):
    def setupUi(self, enroll):
        if not enroll.objectName():
            enroll.setObjectName(u"enroll")
        enroll.resize(386, 215)
        self.lineEdit = QLineEdit(enroll)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(150, 30, 161, 20))
        self.lineEdit_2 = QLineEdit(enroll)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(150, 70, 161, 20))
        self.lineEdit_4 = QLineEdit(enroll)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(150, 110, 161, 20))
        self.lineEdit_4.setEchoMode(QLineEdit.Password)
        self.label = QLabel(enroll)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 30, 54, 16))
        self.label_2 = QLabel(enroll)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(70, 70, 54, 16))
        self.label_3 = QLabel(enroll)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(70, 110, 54, 16))
        self.pushButton = QPushButton(enroll)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(240, 150, 75, 24))

        self.retranslateUi(enroll)
        self.pushButton.clicked.connect(enroll.slot1)

        QMetaObject.connectSlotsByName(enroll)

    # setupUi

    def retranslateUi(self, enroll):
        enroll.setWindowTitle(QCoreApplication.translate("enroll", u"Form", None))
        self.label.setText(QCoreApplication.translate("enroll", u"\u59d3\u540d\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("enroll", u"\u5de5\u53f7\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("enroll", u"\u5bc6\u7801\uff1a", None))
        self.pushButton.setText(QCoreApplication.translate("enroll", u"\u6ce8\u518c", None))
    # retranslateUi


import Module.User as User
import Module.Admin as Admin
import Module.Logger as Logger
from PySide6.QtWidgets import *
from admin_container import admin_containerwindow
from user_container import user_containerwindow


class enrollwindoe(QMainWindow):
    def __init__(self, base):
        super().__init__()
        self.ui = Ui_enroll()
        self.ui.setupUi(self)
        self.dbmain = base

    @QtCore.Slot()
    def slot1(self):
        username=self.ui.lineEdit_2.text()
        name=self.ui.lineEdit.text()
        password=self.ui.lineEdit_4.text()
        db=pymysql.connect(host='172.20.10.8',user='root',passwd='gfnb3017',database='myproject')
        cursor=db.cursor()
        sql="SELECT PersonID,isAdmin FROM Persons"
        cursor.execute(sql)
        results=cursor.fetchall()
        for row in results:
            if username==row[0]:
                sql2="UPDATE Persons SET Name=%s,Password=%s WHERE PersonID=%s;"
                cursor.execute(sql2,(name,password,row[0]))
                db.commit()
                self.dbmain.user_cur=row[0]
                if row[1]==True:
                    self.dbmain.is_admin=1
                    self.dbmain.m_adminwindow=admin_containerwindow(self.dbmain)
                    self.dbmain.m_adminwindow.show()
                    Logger.log_save(f' 用户 {username} 注册成功')
                else:
                    self.dbmain.is_admin=0
                    self.dbmain.m_userwindow=user_containerwindow(self.dbmain)
                    self.dbmain.m_userwindow.show()
                    Logger.log_save(f' 用户 {username} 注册成功')
                self.destroy()
                db.close()
                return
        #登录失败默认无行为，可以添加提示窗口
