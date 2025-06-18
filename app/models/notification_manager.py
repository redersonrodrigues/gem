from PyQt5.QtWidgets import QApplication, QMessageBox


class NotificationManager:
    @staticmethod
    def success(message):
        app = QApplication.instance() or QApplication([])
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.exec_()

    @staticmethod
    def error(message):
        app = QApplication.instance() or QApplication([])
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.exec_()

    @staticmethod
    def info(message):
        app = QApplication.instance() or QApplication([])
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Informação")
        msg_box.setText(message)
        msg_box.exec_()

    @staticmethod
    def warning(message):
        app = QApplication.instance() or QApplication([])
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Aviso")
        msg_box.setText(message)
        msg_box.exec_()
