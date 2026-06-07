
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from db.db import POSTGRESQL
from ui.alert_box import AlertBox

def read_card():
    from devices.card_reader import ThaiIDReader
    card_reader_device = ThaiIDReader()
    card_reader_device.read_card()
    info = card_reader_device.get_person_info()
    return info


class Register_Fingerprint(QWidget):
    def __init__(self, user_role=None):
        super().__init__()
        self.user_role = user_role
        self.db = POSTGRESQL()

        self.setObjectName('Register_Fingerprint')
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(20, 12, 20,12)

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

        self.main_layout.addLayout(vbox)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        group_input_id = QGroupBox('ค้นหาด้วยหมายเลขประจำตัว')
        group_input_id.setMinimumWidth(420)

        search_layout = QGridLayout()
        self.input_id = QLineEdit()
        self.input_id.setValidator(QIntValidator())
        self.input_id.setPlaceholderText('ป้อนหมายเลขฯ แล้วกด Enter')
        self.input_id.returnPressed.connect(lambda: self.get_id_on_readcard('enter'))
        self.btn_get_id = QPushButton('ดึงข้อมูลจากบัตรฯ')
        self.btn_get_id.released.connect(lambda: self.get_id_on_readcard('button'))
        search_layout.addWidget(self.input_id, 0 , 0)
        search_layout.addWidget(self.btn_get_id, 0, 1)
        group_input_id.setLayout(search_layout)        

        self.main_layout.addWidget(group_input_id, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        # self.main_layout.addStretch(1)


        self.group_relative_detail = QGroupBox('ข้อมูลญาติ')
        self.group_relative_detail.setMinimumWidth(420)

        self.form = QFormLayout()
        self.form.setVerticalSpacing(24)
        self.form.setHorizontalSpacing(12)
        self.form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.form.setFormAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_id = QLabel()
        self.label_title = QLabel()
        self.label_f_name = QLabel()
        self.label_l_name = QLabel()
        self.label_address = QLabel()
        self.label_tel = QLabel()

        self.form.addRow('หมายเลขบัตรฯ ', self.label_id)
        self.form.addRow('คำนำหน้า', self.label_title)
        self.form.addRow('ชื่อ', self.label_f_name)
        self.form.addRow('นามสกุล', self.label_l_name)
        self.form.addRow('ที่อยู่', self.label_address)
        self.form.addRow('เบอร์โทร', self.label_tel)

        self.group_relative_detail.setLayout(self.form)
        self.main_layout.addWidget(self.group_relative_detail, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

    def show_datail_and_finger_fp_list(self):
        try:
            data_relative = self.db.get_relative_data(self.input_id.text().strip())
            print(data_relative)
            data_fingerprint = self.db.get_relative_fingerprint_return_fp_name(self.input_id.text().strip())
            print(data_fingerprint)
        except Exception as e:
            print(f'error show_datail_and_finger_fp_list : {e}')

    def get_id_on_readcard(self,trigger ):
        print(trigger)
        # try: 
        #     info_card = read_card()
        #     print(info_card)
        # except Exception as e:
        #     AlertBox.error(self, 'Card Reader', f'ตรวจสอบเครื่องอ่านบัตร {__name__} : {e}')
        #     return
        # try:
        #     if id:
        #         id = self.input_id.text()
        #         self.db.get_relative_data(id)
        # except Exception as e:
        #     AlertBox.error(self, 'ขอมูลของญาติ', f'ปัญหา {__name__} : {e}')
        #     return

        # self.input_id.setText(int(info_card['cid']))
        # self.input_id.setReadOnly(True)
        self.clear_old_relative_detail()

        form = QFormLayout()
        form.setVerticalSpacing(24)
        form.setHorizontalSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        form.setFormAlignment(Qt.AlignmentFlag.AlignCenter)

        self.group_relative_detail = QGroupBox('ข้อมูลญาติ')
        self.group_relative_detail.setMinimumWidth(420)

        label_id = QLabel()
        label_title = QLabel()
        label_f_name = QLabel()
        label_l_name = QLabel()
        label_address = QLabel()
        label_tel = QLabel()

        form.addItem(QSpacerItem(0, 12))
        form.addRow('หมายเลขบัตรฯ ', label_id)
        form.addRow('คำนำหน้า', label_title)
        form.addRow('ชื่อ', label_f_name)
        form.addRow('นามสกุล', label_l_name)
        form.addRow('ที่อยู่', label_address)
        form.addRow('เบอร์โทร', label_tel)

        self.group_relative_detail.setLayout(form)
        self.main_layout.addWidget(
            self.group_relative_detail,
            0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
            
        
    def clear_old_relative_detail(self):
        if hasattr(self, 'group_relative_detail') and self.group_relative_detail is not None:
            self.main_layout.removeWidget(self.group_relative_detail)
            self.group_relative_detail.deleteLater()
            self.group_relative_detail = None











