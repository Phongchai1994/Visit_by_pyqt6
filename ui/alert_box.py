from PyQt6.QtWidgets import QMessageBox

class AlertBox:
    @staticmethod
    def info(parent, title, message):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f5f6fa;
                font-family: 'Sarabun', Arial, sans-serif;
                font-size: 16px;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #5e81f4;
                color: #fff;
                border-radius: 6px;
                padding: 6px 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4666c9;
            }
        """)
        msg.exec()

    @staticmethod
    def warning(parent, title, message):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f5f6fa;
                font-family: 'Sarabun', Arial, sans-serif;
                font-size: 16px;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #5e81f4;
                color: #fff;
                border-radius: 6px;
                padding: 6px 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4666c9;
            }
        """)
        msg.exec()

    @staticmethod
    def error(parent, title, message):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f5f6fa;
                font-family: 'Sarabun', Arial, sans-serif;
                font-size: 16px;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #5e81f4;
                color: #fff;
                border-radius: 6px;
                padding: 6px 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4666c9;
            }
        """)
        msg.exec()

    @staticmethod
    def question(parent, title, message):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f5f6fa;
                font-family: 'Sarabun', Arial, sans-serif;
                font-size: 16px;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #5e81f4;
                color: #fff;
                border-radius: 6px;
                padding: 6px 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4666c9;
            }
        """)
        msg.exec()