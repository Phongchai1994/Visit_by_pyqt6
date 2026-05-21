from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


class MENU_FRAME(QFrame):
    def __init__(self, user_role='user', parent=None):
        super().__init__(parent)

        self.user_role = user_role

        self.setFixedWidth(230)
        layout = QVBoxLayout()

        self.lb_dashboard = self.create_section_label('DASHBOARD')
        self.btn_summery = QPushButton('สรุปผลข้อมูล')
        layout.addWidget(self.lb_dashboard)
        layout.addWidget(self.btn_summery)

        self.lb_manage_prisoner = self.create_section_label('จัดการข้อมูลผู้ต้องขัง')
        self.btn_prisoner_register = QPushButton('ลงทะเบียนผู้ต้องขัง')
        self.btn_prisoners_list = QPushButton('รายชื่อผู้ต้องขัง')
        layout.addWidget(self.lb_manage_prisoner)
        layout.addWidget(self.btn_prisoner_register)
        layout.addWidget(self.btn_prisoners_list)

        self.lb_manage_relative = self.create_section_label('จัดการข้อมูลญาติ')
        self.btn_relatives_list = QPushButton('รายชื่อญาติ')
        self.btn_register_fingerprint = QPushButton('ลงทะเบียนลายนิ้วมือ')
        layout.addWidget(self.lb_manage_relative)
        layout.addWidget(self.btn_relatives_list)
        layout.addWidget(self.btn_register_fingerprint)

        self.lb_book_visit = self.create_section_label('จองเยี่ยม')
        self.btn_book_visit = QPushButton('จองเยี่ยมญาติ')
        self.btn_book_by_id_card = QPushButton('จองเยี่ยมด้วยเลขบัตรฯ')
        layout.addWidget(self.lb_book_visit)
        layout.addWidget(self.btn_book_visit)
        layout.addWidget(self.btn_book_by_id_card)

        self.lb_report = self.create_section_label('รายงาน')
        
        self.btn_daily_report = QPushButton('รายงานประจำวัน')
        self.btn_monthly_report = QPushButton('รายงานประจำเดือน')
        self.btn_special_report = QPushButton('รายงานการเยี่ยมวันหยุด')
        layout.addWidget(self.lb_report)
        layout.addWidget(self.btn_daily_report)
        layout.addWidget(self.btn_monthly_report)
        layout.addWidget(self.btn_special_report)
        layout.addStretch()
        self.setLayout(layout)
        self.set_modern_style()
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(60, 60, 60, 40))  # สีเทาอ่อนโปร่งใส
        self.setGraphicsEffect(shadow)

        self.setup_permissions()

    def create_section_label(self, text):
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
        return label
    
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

    def setup_permissions(self):
        if self.user_role == 'admin':
            pass
        if self.user_role == 'user':
            self.lb_manage_relative.hide()
            self.btn_relatives_list.hide()
            self.btn_register_fingerprint.hide()
            self.lb_book_visit.hide()
            self.btn_book_visit.hide()
            self.btn_book_by_id_card.hide()
        if self.user_role == 'user_visit':
            self.lb_dashboard.hide()
            self.btn_summery.hide()
            self.lb_manage_prisoner.hide()
            self.btn_prisoner_register.hide()
            self.btn_prisoners_list.hide()
            self.lb_manage_relative.hide()
            self.btn_relatives_list.hide()
            self.btn_register_fingerprint.hide()
            self.btn_book_by_id_card.hide()
            self.lb_report.hide()
            self.btn_daily_report.hide()
            self.btn_monthly_report.hide()
            self.btn_special_report.hide()