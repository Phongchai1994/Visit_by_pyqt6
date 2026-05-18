from PyQt6.QtWidgets import QFrame, QVBoxLayout, QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from ui.menu_frame import MENU_FRAME

import sys

class MAINWINDOW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MAIN WINDOW')
        self.setGeometry(200, 200, 720, 480)

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        self.menu = MENU_FRAME(self)
        layout.addWidget(self.menu)

        # สร้าง QFrame สำหรับ main content
        self.main_content = QFrame()
        self.main_content.setObjectName("mainContentFrame")
        main_layout = QVBoxLayout(self.main_content)
        main_layout.setContentsMargins(0, 0, 0, 0)  # ชิดขอบใน QFrame
        main_label = QLabel('main content')
        main_label.setObjectName("mainContentLabel")
        main_layout.addWidget(main_label)
        layout.addWidget(self.main_content)

        self.setCentralWidget(central)
        self.set_modern_style()

        # ใส่เงาให้ main_content
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(60, 60, 60, 40))  # สีเทาอ่อนโปร่งใส
        self.main_content.setGraphicsEffect(shadow)

    def set_modern_style(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background: #fff;
                color: #23272f;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 15px;
            }
            QFrame#mainContentFrame {
                background: #fff;
                border: 1.5px solid #e0e0e0;
                border-radius: 10px;
                margin: 10px 10px 10px 1px;
            }
            QLabel#mainContentLabel {
                background: transparent;
                color: #23272f;
                border-radius: 8px;
                padding: 32px 0;
                font-size: 20px;
                font-weight: 500;
                margin: 32px 24px;
            }
        """)