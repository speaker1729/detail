# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'container-cfile.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import pymysql
from PySide6 import QtCore
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (QLabel, QListView, QPushButton)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(797, 562)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 40, 341, 16))
        self.listView = QListView(Form)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(60, 70, 471, 192))
        self.listView_2 = QListView(Form)
        self.listView_2.setObjectName(u"listView_2")
        self.listView_2.setGeometry(QRect(60, 320, 471, 192))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(70, 290, 351, 16))
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(630, 210, 81, 41))
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(630, 460, 81, 41))
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(630, 90, 81, 41))

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.download)
        self.pushButton_2.clicked.connect(Form.upload)
        self.pushButton_3.clicked.connect(Form.choose)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form",
                                                      u"\u4ece\u6587\u4ef6\u7a97\u53e3\u9009\u62e9\u60a8\u8981\u7f16\u8f91\u7684\u6587\u4ef6\uff1a",
                                                      None))
        self.label_2.setText(QCoreApplication.translate("Form",
                                                        u"\u4ece\u6587\u4ef6\u7a97\u53e3\u9009\u62e9\u60a8\u8981\u52a0\u5bc6\u7684\u6587\u4ef6\uff1a",
                                                        None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u4e0b\u8f7d", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u4e0a\u4f20", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", "选择", None))
    # retranslateUi


import Module.Admin as Admin
import Module.File as File
import Module.Logger as Logger
import Module.Chooser as Chooser
from PySide6.QtWidgets import *
from PySide6.QtGui import QStandardItem, QStandardItemModel
import os

class containcfile(QMainWindow):
    def __init__(self, base):
        super().__init__()
        # 继承主窗口
        self.dbmain = base
        self.model = [QStandardItemModel() for _ in range(2)]
        # 选择的文件名
        self.filename = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 绑定函数
        self.ui.listView.clicked.connect(self.select_0)
        self.ui.listView_2.clicked.connect(self.select_1)
        self.upview()
        self.downview()

    @QtCore.Slot()
    def download(self):
        # 导入密钥
        db = pymysql.connect(host='172.20.10.8', user='root', passwd='gfnb3017', database='myproject')
        cursor = db.cursor()
        sql="select password from filetable where filename=%s"
        cursor.execute(sql,(self.filename))
        key=cursor.fetchone()
        statue = File.down(self.filename, key[0])
        db.close()
        # 输出当前状态
        # self.ui.lab_statue_2.setText(statue)
        QMessageBox.about(self, 'Tips', statue)
        Logger.log_save(self.dbmain.user_cur+' '+self.filename + ' ' + statue)

    @QtCore.Slot()
    def upload(self):
        db=pymysql.connect(host='172.20.10.8',user='root',passwd='gfnb3017',database='myproject')
        cursor=db.cursor()
        # 导入密钥
        sql="select Password from persons where PersonID=%s"
        cursor.execute(sql,(self.dbmain.user_cur))
        data=cursor.fetchone()
        key = data[0]
        # 读取文件名
        file_cur = self.filename
        sql="insert into filetable(filename,personid,password) values(%s,%s,%s)"
        cursor.execute(sql,(file_cur,self.dbmain.user_cur,data[0]))
        db.commit()
        db.close()
        statue = File.up(file_cur, key)
        if self.dbmain.is_admin==1:
            self.dbmain.m_adminwindow.wigcuser.change_wiget2_view()
        # 输出当前状态
        # self.ui.lab_statue_2.setText(statue)
        Logger.log_save(self.dbmain.user_cur + ' ' + file_cur + ' ' + statue)
        QMessageBox.about(self, 'Tips', statue)
        # 在管理员文件夹注册
        Admin.up(file_cur, key)
        self.downview()

    # 文件选择
    def choose(self):
        res = Chooser.file_choose()
        if res:
            if len(res)>1:
                QMessageBox.about(self, 'Tips', "选择了多个文件")
            else:
                self.filename = res[0]
                QMessageBox.about(self, 'Tips', "选择了"+res[0])
                #######
                db = pymysql.connect(host='172.20.10.8', user='root', passwd='gfnb3017', database='myproject')
                cursor = db.cursor()
                # 导入密钥
                sql = "select Password from persons where PersonID=%s"
                cursor.execute(sql, (self.dbmain.user_cur))
                data = cursor.fetchone()
                key = data[0]
                # 读取文件名
                file_cur = os.path.basename(res[0])
                sql = "insert into filetable(filename,personid,password) values(%s,%s,%s)"
                cursor.execute(sql, (file_cur, self.dbmain.user_cur, data[0]))
                db.commit()
                db.close()
                statue = File.up(res[0], key,True)
                if self.dbmain.is_admin == 1:
                    self.dbmain.m_adminwindow.wigcuser.change_wiget2_view()
                # 输出当前状态
                # self.ui.lab_statue_2.setText(statue)
                Logger.log_save(self.dbmain.user_cur + ' ' + file_cur + ' ' + statue)
                QMessageBox.about(self, 'Tips', statue)
                # 在管理员文件夹注册
                Admin.up(file_cur, key)
                self.downview()
        else:
            QMessageBox.about(self, 'Tips', "未选择")

    # 文件界面刷新
    def downview(self):
        db=pymysql.connect(host='172.20.10.8',user='root',passwd='gfnb3017',database='myproject')
        cursor=db.cursor()
        if self.dbmain.is_admin==1:
            sql="select * from filetable"
            cursor.execute(sql)
        else:
            sql="select Filepath from personfile where PersonID=%s"
            cursor.execute(sql,(self.dbmain.user_cur))
        results=cursor.fetchall()
        self.model[0].clear()
        for file in results:
            item = QStandardItem(file[0])
            self.model[0].appendRow(item)
        self.ui.listView.setModel(self.model[0])
        db.close()

    def upview(self):
        files = File.get_all('Input')
        # 表明当前目录
        # self.ui.lab_folder_2.setText('输入区')
        # 清除存储的文件名
        # self.ui.lab_file.setText('无')
        # 清理现文件再添加
        self.model[1].clear()
        for file in files:
            item = QStandardItem(file)
            self.model[1].appendRow(item)
        self.ui.listView_2.setModel(self.model[1])

    # 绑定
    def select_0(self, index):
        # 选取文件页面的列表
        selected_item = self.model[0].itemFromIndex(index)
        # 将选择的文件存储
        self.filename = selected_item.text()

    def select_1(self, index):
        # 选取文件页面的列表
        selected_item = self.model[1].itemFromIndex(index)
        # 将选择的文件存储
        self.filename = selected_item.text()
