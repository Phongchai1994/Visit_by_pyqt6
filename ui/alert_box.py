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
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg.exec()
        return result == QMessageBox.StandardButton.Yes
    
    @staticmethod
    def success(parent, title, message):
        msg = QMessageBox(parent)
        msg.setObjectName("appMessageBox")
        msg.setIcon(QMessageBox.Icon.Information)  # Qt ไม่มีไอคอน Success โดยตรง ใช้ Information แทน
        msg.setWindowTitle(title)
        msg.setText(message)
        # สามารถเปลี่ยนปุ่มหรือ style เพิ่มเติมได้
        msg.exec()
