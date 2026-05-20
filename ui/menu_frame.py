from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

def add_section_label(text, layout):
    label = QLabel(text)
    label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
    label.setStyleSheet("""
        font-size: 16px;
        font-weight: bold;
        color: #222;
        margin-top: 22px;
        margin-bottom: 8px;
        background: transparent;
        border: none;
    """)
    layout.addWidget(label)

class MENU_FRAME(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFixedWidth(230)
        layout = QVBoxLayout()
        add_section_label('DASHBOARD',layout)
        self.btn_summery = QPushButton('สรุปผลข้อมูล')
        layout.addWidget(self.btn_summery)

        add_section_label('จัดการข้อมูลผู้ต้องขัง',layout)
        self.btn_prisoner_register = QPushButton('ลงทะเบียนผู้ต้องขัง')
        layout.addWidget(self.btn_prisoner_register)
        layout.addWidget(QPushButton('รายชื่อผู้ต้องขัง'))

        add_section_label('จัดการข้อมูลญาติ',layout)
        layout.addWidget(QPushButton('รายชื่อญาติ'))
        layout.addWidget(QPushButton('ลงทะเบียนลายนิ้วมือ'))

        add_section_label('จองเยี่ยม',layout)
        layout.addWidget(QPushButton('จองเยี่ยมญาติ'))
        layout.addWidget(QPushButton('จองเยี่ยมด้วยเลขบัตรฯ'))

        add_section_label('รายงาน',layout)
        layout.addWidget(QPushButton('รายงานประจำวัน'))
        layout.addWidget(QPushButton('รายงานประจำเดือน'))
        layout.addWidget(QPushButton('รายงานการเยี่ยมวันหยุด'))
        layout.addStretch()
        self.setLayout(layout)
        self.set_modern_style()
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(60, 60, 60, 40))  # สีเทาอ่อนโปร่งใส
        self.setGraphicsEffect(shadow)


    def set_modern_style(self):
        self.setStyleSheet("""
            QFrame {
                background: #fff;
                border: 1.5px solid #e0e0e0;
                border-radius: 10px;
                margin: 10px 1px 10px 10px;
                font-family: 'Sarabun', Arial, sans-serif;
                           
            }
            QLabel {
                color: #333;
                font-weight: bold;
                font-size: 15px;
                margin-top: 18px;
                margin-bottom: 6px;
            }
            QPushButton {
                background: #f5f6fa;
                color: #222;
                border: 1px solid #e0e0e0;
                border-radius: 7px;
                padding: 10px 0;
                margin-bottom: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #e3e8f0;
                color: #1a73e8;
                border: 1px solid #b3c6f7;
            }
        """)