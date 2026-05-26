from PyQt6.QtWidgets import QMessageBox

class AlertBox:
    @staticmethod
    def info(parent, title, message):
        msg = QMessageBox(parent)
        msg.setObjectName("appMessageBox")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    @staticmethod
    def warning(parent, title, message):
        msg = QMessageBox(parent)
        msg.setObjectName("appMessageBox")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    @staticmethod
    def error(parent, title, message):
        msg = QMessageBox(parent)
        msg.setObjectName("appMessageBox")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    @staticmethod
    def question(parent, title, message):
        msg = QMessageBox(parent)
        msg.setObjectName("appMessageBox")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()