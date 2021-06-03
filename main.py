# This Python file uses the following encoding: utf-8
import sys
import os

from PySide6.QtGui import QIcon
from Database import Database
import datetime
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QPushButton, QWidget
from PySide6.QtCore import QFile, QSize
from PySide6.QtUiTools import QUiLoader
from functools import partial


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load('form.ui')
        self.ui.show()
        self.dark = False
        self.ui.btn_send.clicked.connect(self.addNewMessage)
        self.ui.darkbtn.clicked.connect(self.darkmode)
        self.ui.delall_btn.clicked.connect(self.deleteall)

        self.readMessages()

    def readMessages(self):
        messages = Database.select()
        for i, message in enumerate(messages):
            label = QLabel()
            label.setText(message[3] + "-" + message[1] + ": " + message[2])
            self.ui.vl_messages.addWidget(label, i, 1)
            label.setStyleSheet('font-family: B YEKAN, Helvetica, sans-serif')

            btn = QPushButton()
            btn.setIcon(QIcon("recycle-bin.png"))
            btn.setIconSize(QSize(20, 20))
            btn.setShortcut('Ctrl+d')
            btn.setStyleSheet(
                'max-width: 18px; min-height: 18px; color: white; border: 0px; border-radius: 5px;')
            btn.clicked.connect(partial(self.delete, message[0], btn, label))
            self.ui.vl_messages.addWidget(btn, i, 0)

    def addNewMessage(self):
        name = self.ui.txt_name.text()
        text = self.ui.txt_message.text()
        messages = Database.select()

        if name != "" and text != "":
            response = Database.insert(name, text)
            if response:
                label = QLabel()
                label.setText(name + ": " + text)

                self.ui.vl_messages.addWidget(label, len(messages)+1, 1)
                btn = QPushButton()
                btn.setIcon(QIcon('recycle bin.png'))
                btn.setFixedWidth(20)
                btn.clicked.connect(partial(self.delete, btn, len(messages)+1))
                self.ui.vl_messages.addWidget(btn, len(messages)+1, 0)

                msg_box = QMessageBox()
                msg_box.setText("Your message sent successfully!")
                msg_box.exec_()

                self.ui.txt_name.setText("")
                self.ui.txt_message.setText("")

            else:
                msg_box = QMessageBox()
                msg_box.setText("Database error!")
                msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setText("Error: feilds are empty!")
            msg_box.exec_()

    def delete(self, id, btn, label):
        resp = Database.delete(id)
        if resp:
            btn.hide()
            label.hide()

    def deleteall(self):
        response = Database.deleteall()

        if response:
            msg_box = QMessageBox()

            self.msg_box("all of messages deleted!")
            msg_box.exec_()
            self.readMessages()

            for i in range(self.ui.vl_messages.count()):
                self.ui.vl_messages.itemAt(i).widget().hide()
        else:
            msg_box = QMessageBox()
            self.msg_box("Database error!")
            msg_box.exec_()

    def darkmode(self):
        if not self.dark:
            self.ui.setStyleSheet("background-color: rgb(80, 80, 80)")
            self.dark = not self.dark
            self.ui.btn_send.setStyleSheet(
                "background-color: rgb(0, 90, 10); color: rgb(255,255,255)")
            self.ui.btn_messagebox.setStyleSheet(
                "background-color: rgb(88, 15, 55);color: rgb(0, 160, 65);border-radius: 45px;border: 2px;border-radius: 10px")

        else:
            self.ui.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(208, 210, 236, 255), stop:1 rgba(255, 255, 255, 255));")
            self.ui.btn_send.setStyleSheet(
                "background-color: rgb(200, 255, 199)")
            self.ui.btn_messagebox.setStyleSheet(
                "color: rgb(255, 238, 41);\nbackground-color: rgb(255, 255, 255);\nborder-radius: 45px;\nborder: 2px ;\n  border-radius:10px;")
            self.dark = not self.dark


if __name__ == "__main__":
    app = QApplication([])
    widget = Main()
    sys.exit(app.exec_())
