from PyQt6.QtWidgets import (
   QWidget, 
   QLabel, 
   QLineEdit, 
   QPushButton, 
   QVBoxLayout,
   QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression
from ui.main_app import MAINWINDOW
from db.db import POSTGRESQL
from ui.alert_box import AlertBox
from utils.resource import Resource_Helper

class LOGIN(QWidget):
    def __init__(self):
        super().__init__()
        self.db = POSTGRESQL()
        self.db.create_tables_if_not_exist()
        self.setObjectName('Qwidget_login')

        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 300, 150)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.center()
        layout = QVBoxLayout()

        regex = QRegularExpression("^[a-zA-Z_]*$")
        validator = QRegularExpressionValidator(regex)
        self.label_user = QLabel('Username')
        self.input_user = QLineEdit()
        self.input_user.setValidator(validator)

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

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(60, 60, 60, 40))  # สีเทาอ่อนโปร่งใส
        self.setGraphicsEffect(shadow)

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


