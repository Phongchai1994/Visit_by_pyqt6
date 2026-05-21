from PyQt6.QtWidgets import (
   QWidget, 
   QLabel, 
   QLineEdit, 
   QPushButton, 
   QVBoxLayout,
   QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from ui.main_app import MAINWINDOW
from db.db import POSTGRESQL
from ui.alert_box import AlertBox

class LOGIN(QWidget):
    def __init__(self):
        super().__init__()
        self.db = POSTGRESQL()
        self.db.create_tables_if_not_exist()

        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 300, 150)
        self.center()
        layout = QVBoxLayout()

        self.label_user = QLabel('Username')
        self.input_user = QLineEdit()
        self.label_password = QLabel('Password')
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.returnPressed.connect(self.handle_login)

        self.btn_login = QPushButton('Login')
        self.btn_login.clicked.connect(self.handle_login)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)
        self.setLayout(layout)
        self.set_modern_style()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(60, 60, 60, 40))  # สีเทาอ่อนโปร่งใส
        self.setGraphicsEffect(shadow)

    def set_modern_style(self):
        self.setStyleSheet(
            '''
                QWidget {
                    background-color: #fff;
                    color: #222;
                    font-family: 'Sarabun', Arial, sans-serif;
                    font-size: 14px
                }
                QLabel {
                    color: #333;
                    font-weight: bold;
                }
                QLineEdit {
                    background: #f5f6fa;
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                    padding: 6px;
                    color: #222;
                }
                QLineEdit:focus {
                    border: 1.5px solid #5e81f4;
                    background: #fff;
                }
                QPushButton {
                    background-color: #5e81f4;
                    color: #fff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 0;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4666c9;
                }
            '''
        )

    def center(self):
        frameGm = self.frameGeometry()
        screen = self.screen().availableVirtualGeometry().center()
        frameGm.moveCenter(screen)
        self.move(frameGm.topLeft())

    def handle_login(self):
        # self.main_window = MAINWINDOW()
        # self.main_window.show()
        # self.close()

        username = self.input_user.text()
        password = self.input_password.text()
        if self.db.check_db_login(username, password):
            self.close()
            # เพิมโปรแกรมหลัก
            self.main_window = MAINWINDOW(user_role=username)
            self.main_window.show()
        else:
            self.input_password.clear()
            AlertBox.error(self, 'เข้าสู่ระบบ', 'เข้าสู่ระบบไม่สำเร็จ')


