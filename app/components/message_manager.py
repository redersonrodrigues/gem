from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtCore import Qt

class MessageManager:
    @staticmethod
    def info(parent, title, text):
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle(title)
        box.setText(text)
        ok_btn = box.addButton(QMessageBox.Ok)
        ok_btn.setStyleSheet('background-color: #388e3c; color: white; font-weight: bold;')
        box.setDefaultButton(ok_btn)
        box.exec_()
        return box

    @staticmethod
    def warning(parent, title, text):
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle(title)
        box.setText(text)
        ok_btn = box.addButton(QMessageBox.Ok)
        ok_btn.setStyleSheet('background-color: #388e3c; color: white; font-weight: bold;')
        box.setDefaultButton(ok_btn)
        box.exec_()
        return box

    @staticmethod
    def error(parent, title, text):
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Critical)
        box.setWindowTitle(title)
        box.setText(text)
        ok_btn = box.addButton(QMessageBox.Ok)
        ok_btn.setStyleSheet('background-color: #388e3c; color: white; font-weight: bold;')
        box.setDefaultButton(ok_btn)
        box.exec_()
        return box

    @staticmethod
    def confirm(parent, title, text):
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle(title)
        box.setText(text)
        yes_btn = box.addButton('Sim', QMessageBox.YesRole)
        yes_btn.setStyleSheet('background-color: #1976d2; color: white; font-weight: bold;')
        no_btn = box.addButton('Não', QMessageBox.NoRole)
        no_btn.setStyleSheet('background-color: #d32f2f; color: white; font-weight: bold;')
        box.setDefaultButton(yes_btn)
        box.exec_()
        return box.clickedButton() == yes_btn
