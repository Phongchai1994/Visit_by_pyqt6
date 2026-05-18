from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel


class MENU_FRAME(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFixedWidth(230)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('DASHBOARD'))
        btn_summery = QPushButton('สรุปผลข้อมูล')
        layout.addWidget(btn_summery)


        layout.addWidget(QLabel('จัดการผู้ต้องขัง'))
        layout.addWidget(QPushButton('ลงทะเบียนผู้ต้องขัง'))
        layout.addWidget(QPushButton('รายชื่อผู้ต้องขัง'))

        layout.addWidget(QLabel('ข้อมูลญาติ'))
        layout.addWidget(QPushButton('รายชื่อญาติ'))
        layout.addWidget(QPushButton('ลงทะเบียนลายนิ้วมือ'))

        layout.addWidget(QLabel('จองเยี่ยม'))
        layout.addWidget(QPushButton('จองเยี่ยมญาติ'))
        layout.addWidget(QPushButton('จองเยี่ยมญาติด้วยบัตรประชาชน'))

        layout.addWidget(QLabel('รายงาน'))
        layout.addWidget(QPushButton('รายงานประจำวัน'))
        layout.addWidget(QPushButton('รายงานประจำเดือน'))
        layout.addWidget(QPushButton('รายงานการเยี่ยมวันหยุดพิเศษ'))
        layout.addStretch()
        self.setLayout(layout)
