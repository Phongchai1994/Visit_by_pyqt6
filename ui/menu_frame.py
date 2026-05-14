from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton

class MENU_FRAME(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFixedWidth(180)
        layout = QVBoxLayout()
        layout.addWidget(QPushButton('ลงทะเบียนผู้ต้องขัง'))
        layout.addWidget(QPushButton('รายชื่อผู้ต้องขัง'))
        layout.addWidget(QPushButton('รายชื่อญาติ'))
        layout.addWidget(QPushButton('ลงทะเบียนผู้ต้องขัง'))
        layout.addWidget(QPushButton('ลงทะเบียนลายนิ้วมือ'))
        layout.addWidget(QPushButton('จองเยี่ยมญาติ'))
        layout.addWidget(QPushButton('จองเยี่ยมญาติด้วยบัตรประชาชน'))
        layout.addWidget(QPushButton('รายงานประจำวัน'))
        layout.addWidget(QPushButton('รายงานประจำเดือน'))
        layout.addWidget(QPushButton('รายงานการเยี่ยมวันหยุดพิเศษ'))
        layout.addStretch()
        self.setLayout(layout)