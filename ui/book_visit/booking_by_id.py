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


class Book_By_National_ID(QWidget):
    def __init__(self):
        super().__init__()
        self.group_relative_detail = None
        self.group_relations_detail = None
        self.group_button = None
        self.btn_booking = None
        self.btn_close = None
        self.form = None
        self.form_relations = None
        self.label_id = None
        self.label_title = None
        self.label_f_name = None
        self.label_l_name = None
        self.label_address = None
        self.label_tel = None
        self.label_status = None
        self.db = POSTGRESQL()

        self.setObjectName('Book_By_National_ID')

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(20, 12, 20, 12)

        # หัวข้อ
        title_label = QLabel('จองเยี่ยมด้วยหมายเลขประจำตัว')
        title_label.setObjectName('Book_By_National_ID_title_label')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # เส้นคั่น
        title_line = QFrame()
        title_line.setFrameShape(QFrame.Shape.HLine)
        title_line.setFrameShadow(QFrame.Shadow.Sunken)
        title_line.setStyleSheet("color: #000000; background: #000000;")

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
        self.input_id.returnPressed.connect(lambda: self.verify_input_id('enter'))
        self.btn_get_id = QPushButton('ดึงข้อมูลจากบัตรฯ')
        self.btn_get_id.released.connect(lambda: self.verify_input_id('button'))
        search_layout.addWidget(self.input_id, 0 , 0)
        search_layout.addWidget(self.btn_get_id, 0, 1)
        group_input_id.setLayout(search_layout)
        self.main_layout.addWidget(group_input_id, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)


    def verify_input_id(self, trigger):
        self.create_ui_relative_data()
        relative_id = None
        #  ตรวจสอบการกด button or enter
        if trigger == 'button':
            try: 
                from devices.read_card import read_card
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
            try:
                relative_data = self.db.get_relative_data(relative_id=relative_id)
                relations_data = self.db.get_prisoners_from_relative_id(relative_id=relative_id)
            except Exception as e:
                relative_data = []
                relations_data = []
                pass
        if not relative_data:
            AlertBox.error(self, 'Book_By_National_ID', 'ไม่พบข้อมูล' )
            return
        self.input_id.setReadOnly(True)
        for i, value in enumerate(relations_data, 1):
            disciplinary_text = '-'
            if value[7] is not None and str(value[7]).strip().lower() != 'none':
                disciplinary_text = str(value[7])

            status_text = str(value[6])
            status_html = status_text
            if status_text == 'ไม่อยู่':
                status_html = f'<span style="color: red;">{status_text}</span>'
            else:
                status_html = f'<span style="color: green;">{status_text}</span>'

            disciplinary_html = disciplinary_text
            if disciplinary_text == 'ผิดวินัย':
                disciplinary_html = f'<span style="color: red;">{disciplinary_text}</span>'

            prisoner_data = (
                f'ชื่อ {value[2]} {value[3]} เพศ {value[1]}<br>'
                f'ชั้น {value[4]} แดน {value[5]}<br>'
                f'สถานะ {status_html} วินัย {disciplinary_html}'
            )

            lbl_key = QLabel(f"คนที่ {i} :")
            lbl_val = QLabel(prisoner_data)
            lbl_val.setTextFormat(Qt.TextFormat.RichText)
            lbl_val.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.form_relations.addRow(lbl_key, lbl_val)

        rel_id = relative_data[0]
        rel_title = relative_data[1]
        rel_f_name = relative_data[2]
        rel_l_name = relative_data[3]
        rel_address = relative_data[4]
        rel_tel = relative_data[5]
        rel_status = relative_data[6]

        self.group_relative_detail.show()
        self.group_relations_detail.show()
        self.group_button.show()

        self.label_id.setText(str(rel_id))
        self.label_title.setText(rel_title)
        self.label_f_name.setText(rel_f_name)
        self.label_l_name.setText(rel_l_name)
        self.label_address.setText(rel_address)
        self.label_tel.setText(str(rel_tel))
        self.label_status.setText('ใช้งานอยู่' if rel_status else 'ยกเลิกแล้ว')

        self.btn_booking.clicked.connect(self.handle_booking)
        self.btn_close.clicked.connect(self.clear_old_detail)

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

        self.form.addRow('หมายเลขบัตรฯ :', self.label_id)
        self.form.addRow('คำนำหน้า :', self.label_title)
        self.form.addRow('ชื่อ :', self.label_f_name)
        self.form.addRow('นามสกุล :', self.label_l_name)
        self.form.addRow('ที่อยู่ :', self.label_address)
        self.form.addRow('เบอร์โทร :', self.label_tel)
        self.form.addRow('สถานะ :', self.label_status)

        self.group_relative_detail.setLayout(self.form)

        self.group_relations_detail = QGroupBox('ข้อมูลความสัมพันธ์')
        self.group_relations_detail.setMinimumWidth(420)

        self.form_relations = QFormLayout()
        self.form_relations.setVerticalSpacing(24)
        self.form_relations.setHorizontalSpacing(12)
        self.form_relations.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.form_relations.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        self.group_relations_detail.setLayout(self.form_relations)

        self.group_button = QGroupBox()
        self.group_button.setMinimumWidth(420)
        self.btn_booking = QPushButton('จองเยี่ยม')
        self.btn_close = QPushButton('เสร็จสิ้น')
        vbox_in_groupbox = QVBoxLayout()
        vbox_in_groupbox.addWidget(self.btn_booking)
        vbox_in_groupbox.addWidget(self.btn_close)
        self.group_button.setLayout(vbox_in_groupbox)
        
        self.main_layout.addWidget(self.group_relative_detail, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.group_relations_detail, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.group_button, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.group_relative_detail.hide()
        self.group_relations_detail.hide()
        self.group_button.hide()

    def clear_old_detail(self):
        self.input_id.clear()
        self.input_id.setReadOnly(False)
        self.btn_get_id.setEnabled(True)
        if hasattr(self, 'group_relative_detail') and self.group_relative_detail is not None:
            self.main_layout.removeWidget(self.group_relative_detail)
            self.group_relative_detail.deleteLater()
            self.group_relative_detail = None        

        if hasattr(self, 'group_relations_detail') and self.group_relations_detail is not None:
            self.main_layout.removeWidget(self.group_relations_detail)
            self.group_relations_detail.deleteLater()
            self.group_relations_detail = None

        if hasattr(self, 'group_button') and self.group_button is not None:
            self.main_layout.removeWidget(self.group_button)
            self.group_button.deleteLater()
            self.group_button = None

    def handle_booking(self):
        from ui.book_visit.booking import Booking
        prisoner_data = ['id','ชื่อ','สกุล','ชั้น','แดน','5', '6','ประเภท']
        relative_data = ['1560100345135', 'คำนำหน้า', 'ชื่อญาติ', 'สกุลญาติ']
        booking = Booking(
            prisoner_data=prisoner_data, relative_data=relative_data, reserve_now=True
        )
        booking.exec()









