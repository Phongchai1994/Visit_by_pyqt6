
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
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from db.db import POSTGRESQL
from ui.alert_box import AlertBox
from utils.date_convers import DATE_STR
from ui.list_popup import List_popup

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

        regex = QRegularExpression(r"\d{0,13}")

        search_layout = QGridLayout()
        self.input_id = QLineEdit()
        self.input_id.setValidator(QRegularExpressionValidator(regex))
        self.input_id.setPlaceholderText('ป้อนหมายเลขฯ แล้วกด Enter')
        self.input_id.returnPressed.connect(lambda: self.get_id_on_readcard('enter'))
        self.btn_get_id = QPushButton('ดึงข้อมูลจากบัตรฯ')
        self.btn_get_id.released.connect(lambda: self.get_id_on_readcard('button'))
        search_layout.addWidget(self.input_id, 0 , 0)
        search_layout.addWidget(self.btn_get_id, 0, 1)
        group_input_id.setLayout(search_layout)
        self.main_layout.addWidget(group_input_id, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.create_ui_relative_data()

    def create_ui_relative_data(self):
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
        self.label_status = QLabel()
        self.label_time_insert = QLabel()
        self.label_time_update = QLabel()
        self.label_user_insert = QLabel()

        self.form.addRow('หมายเลขบัตรฯ ', self.label_id)
        self.form.addRow('คำนำหน้า', self.label_title)
        self.form.addRow('ชื่อ', self.label_f_name)
        self.form.addRow('นามสกุล', self.label_l_name)
        self.form.addRow('ที่อยู่', self.label_address)
        self.form.addRow('เบอร์โทร', self.label_tel)
        self.form.addRow('สถานะ', self.label_status)
        self.form.addRow('วันที่เพิ่มข้อมูล', self.label_time_insert)
        self.form.addRow('วันที่อัพเดทล่าสุด', self.label_time_update)
        self.form.addRow('เพิ่มโดย', self.label_user_insert)

        self.group_relative_detail.setLayout(self.form)

        self.group_fingerprint_detail = QGroupBox('ข้อมูลลายนิ้วมือ')
        self.group_fingerprint_detail.setMinimumWidth(420)
        self.grid_layout_finger_detail = QGridLayout()
        self.btn_regis = QPushButton('ลงทะเบียน')
        self.grid_layout_finger_detail.addWidget(self.btn_regis, 1 , 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.group_fingerprint_detail.setLayout(self.grid_layout_finger_detail)

        self.group_button = QGroupBox()
        self.group_button.setMinimumWidth(420)

        self.btn_close = QPushButton('เสร็จสิ้น')
        vbox_in_groupbox = QVBoxLayout()
        vbox_in_groupbox.addWidget(self.btn_close)
        self.group_button.setLayout(vbox_in_groupbox)
        
        self.main_layout.addWidget(self.group_relative_detail, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.group_fingerprint_detail, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.group_button, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.group_relative_detail.hide()
        self.group_fingerprint_detail.hide()
        self.group_button.hide()   

    def get_id_on_readcard(self, trigger):
        self.create_ui_relative_data()
        relative_id = None
        #  ตรวจสอบการกด button or enter
        if trigger == 'button':
            try: 
                info_card = read_card()
                self.input_id.setText(str(info_card['cid']))
                relative_id = info_card['cid']
            except Exception as e:
                AlertBox.error(self, 'Card Reader', f'ตรวจสอบเครื่องอ่านบัตร {__name__} : {e}')
                return
        elif trigger == 'enter':
            try:
                relative_id = self.input_id.text().strip().lower()
            except Exception as e:
                AlertBox.error(self, 'ขอมูลของญาติ', f'ปัญหา {__name__} : {e}')
                return
        else:
            return
        
        if relative_id:
            self.input_id.setReadOnly(True)
            try:
                relative_data = self.db.get_relative_data(relative_id=relative_id)
                fingerprint_data = self.db.get_relative_fingerprint_return_fp_name(relative_id=relative_id)
            except Exception as e:
                pass
        # print(relative_data)
        if fingerprint_data:
            label_fp_name = QLabel(fingerprint_data[0][0])
            self.grid_layout_finger_detail.addWidget(QLabel('นิ้วที่ลงทะเบียน : '), 0, 0, Qt.AlignmentFlag.AlignRight)
            self.grid_layout_finger_detail.addWidget(label_fp_name, 0, 1, Qt.AlignmentFlag.AlignLeft)
            # print(fingerprint_data)
            # print(fingerprint_data[0])
        else:
            label = QLabel('ไม่พบลายนิ้วมือ')
            self.grid_layout_finger_detail.addWidget(label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.btn_get_id.setEnabled(False)


        rel_id = relative_data[0]
        rel_title = relative_data[1]
        rel_f_name = relative_data[2]
        rel_l_name = relative_data[3]
        rel_address = relative_data[4]
        rel_tel = relative_data[5]
        rel_status = relative_data[6]
        rel_user_insert = relative_data[7]
        rel_time_insert = DATE_STR.date_full(relative_data[8])
        rel_time_update = '-' if relative_data[9] is None else DATE_STR.date_full(relative_data[9])

        self.group_relative_detail.show()
        self.group_fingerprint_detail.show()
        self.group_button.show()

        self.label_id.setText(str(rel_id))
        self.label_title.setText(rel_title)
        self.label_f_name.setText(rel_f_name)
        self.label_l_name.setText(rel_l_name)
        self.label_address.setText(rel_address)
        self.label_tel.setText(str(rel_tel))
        self.label_status.setText('ใช้งานอยู่' if rel_status else 'ยกเลิกแล้ว')
        self.label_time_insert.setText(rel_time_insert)
        self.label_time_update.setText(rel_time_update)
        self.label_user_insert.setText(rel_user_insert)
        self.btn_regis.clicked.connect(lambda: self.manage_fingerprint(relative_data=relative_data))
        self.btn_close.clicked.connect(self.clear_old_relative_detail)
   
    def manage_fingerprint(self, relative_data):
        from devices.regis_fp import Fingerprint_Register_Dialog
        dialog_popup = Fingerprint_Register_Dialog(relative_data)
        dialog_popup.exec()

    def clear_old_relative_detail(self):
        self.input_id.clear()
        self.input_id.setReadOnly(False)
        self.btn_get_id.setEnabled(True)
        if hasattr(self, 'group_relative_detail') and self.group_relative_detail is not None:
            self.main_layout.removeWidget(self.group_relative_detail)
            self.group_relative_detail.deleteLater()
            self.group_relative_detail = None        

        if hasattr(self, 'group_fingerprint_detail') and self.group_fingerprint_detail is not None:
            self.main_layout.removeWidget(self.group_fingerprint_detail)
            self.group_fingerprint_detail.deleteLater()
            self.group_fingerprint_detail = None

        if hasattr(self, 'group_button') and self.group_button is not None:
            self.main_layout.removeWidget(self.group_button)
            self.group_button.deleteLater()
            self.group_button = None











