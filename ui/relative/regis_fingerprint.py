
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QGroupBox
)
from PyQt6.QtCore import Qt
from db.db import POSTGRESQL

class Register_Fingerprint(QWidget):
    def __init__(self, user_role=None):
        super().__init__()
        self.user_role = user_role
        self.db = POSTGRESQL()

        self.setObjectName('Register_Fingerprint')
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 12, 20,12)

        title_label = QLabel('ลงทะเบียนลายนิ้วมือ')
        title_label.setObjectName('Register_Fingerprint_title_label')
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title_line = QFrame()
        title_line.setFrameShape(QFrame.Shape.HLine)
        title_line.setFrameShadow(QFrame.Shadow.Sunken)
        title_line.setStyleSheet('color: #000000; background: #000000;')

        # layout
        vbox = QVBoxLayout()
        vbox.addItem(QSpacerItem(0, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        vbox.addWidget(title_label)
        vbox.addWidget(title_line)

        main_layout.addLayout(vbox)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        group_input_id = QGroupBox('ค้นหาด้วยหมายเลขประจำตัว')
        group_input_id.setMinimumWidth(420)

        search_layout = QGridLayout()
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText('ป้อนหมายเลขฯ แล้วกด Enter')
        self.input_id.returnPressed.connect(self.show_datail_and_finger_fp_list)
        btn_get_id = QPushButton('ดึงข้อมูลจากบัตรฯ')
        btn_get_id.clicked.connect(self.get_id_on_readcard)
        search_layout.addWidget(self.input_id, 0 , 0)
        search_layout.addWidget(btn_get_id, 0, 1)
        group_input_id.setLayout(search_layout)        
        
        main_layout.addWidget(group_input_id, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        main_layout.addStretch(1)

    def show_datail_and_finger_fp_list(self):
        try:
            data_relative = self.db.get_relative_data(self.input_id.text().strip())
            print(data_relative)
            data_fingerprint = self.db.get_relative_fingerprint_return_fp_name(self.input_id.text().strip())
            print(data_fingerprint)
        except Exception as e:
            print(f'error show_datail_and_finger_fp_list : {e}')

    def get_id_on_readcard(self):
        try:
            from devices.card_reader import ThaiIDReader
            thai_id = ThaiIDReader()
            relative_id = thai_id.read_card()
        except Exception as e:
            print(f'errror get_id_on_readcard :{e}')
            
        












