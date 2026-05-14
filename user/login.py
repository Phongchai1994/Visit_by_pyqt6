from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from dotenv import load_dotenv
from ui.main_app import MAINWINDOW

import sys
import psycopg2
import os
import hashlib

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

class LOGIN(QWidget):
    def __init__(self):
        super().__init__()
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

    def center(self):
        frameGm = self.frameGeometry()
        screen = self.screen().availableVirtualGeometry().center()
        frameGm.moveCenter(screen)
        self.move(frameGm.topLeft())

    def handle_login(self):
        username = self.input_user.text()
        password = self.input_password.text()
        if self.check_db_login(username, password):
            # QMessageBox.information(self, "Success", "Login Success!")
            self.close()
            # เพิมโปรแกรมหลัก
            self.main_window = MAINWINDOW()
            self.main_window.show()
        else:
            self.input_password.clear()
            QMessageBox.warning(self, 'Failed', 'Login Failed!')


    def check_db_login(self, username, password):
        try:
            conn = psycopg2.connect(
                host=os.getenv("PG_HOST"),
                port=os.getenv("PG_PORT"),
                dbname=os.getenv("PG_NAME"),
                user=os.getenv("PG_USER"),
                password=os.getenv("PG_PASS")
            )
            with conn.cursor() as cur:
                cur.execute("SELECT password FROM users WHERE username=%s", (username,))
                row = cur.fetchone()
                if row:
                    db_password = row[0].tobytes()
                    input_hash = hashlib.sha256(password.encode()).digest()
                    # print(db_password, input_hash)
                    return db_password == input_hash
                else:
                    return False
        except Exception as e:
            print(f'DB ERROR:{e}')
        
        return False

