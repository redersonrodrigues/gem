"""
Componente de notificações e alertas para PyQt5
"""
from PyQt5.QtWidgets import QMessageBox, QWidget

class Notifier:
    @staticmethod
    def info(parent: QWidget, title: str, message: str):
        QMessageBox.information(parent, title, message)

    @staticmethod
    def warning(parent: QWidget, title: str, message: str):
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def error(parent: QWidget, title: str, message: str):
        QMessageBox.critical(parent, title, message)

    @staticmethod
    def ask(parent: QWidget, title: str, message: str) -> bool:
        reply = QMessageBox.question(parent, title, message, QMessageBox.Yes | QMessageBox.No)
        return reply == QMessageBox.Yes
