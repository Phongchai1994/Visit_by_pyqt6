from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel
from ui.menu_frame import MENU_FRAME

import sys

class MAINWINDOW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MAIN WINDOW')
        self.setGeometry(200, 200, 720, 480)

        central = QWidget()
        layout = QHBoxLayout(central)
        self.menu = MENU_FRAME(self)
        layout.addWidget(self.menu)
        layout.addWidget(QLabel('main content'))
        # ส่วนนี้สำหรับเนื้อหาหลัก (main content)
        # สามารถเพิ่ม widget อื่นๆ ทางขวาได้
        self.setCentralWidget(central)