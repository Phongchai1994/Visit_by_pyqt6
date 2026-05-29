from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableView,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QHeaderView,
    QGroupBox,
    QCheckBox,
    QGridLayout,
    QLineEdit,
    QMenu,
    QDialog,
    QFormLayout,
    QPushButton,
    QComboBox, 
    QTextEdit,
    QFrame
)

from PyQt6.QtCore import Qt, QAbstractTableModel, QEvent, QRegularExpression
from PyQt6.QtGui import QBrush, QColor, QAction, QRegularExpressionValidator
from db.db import log_db_exceptions

from devices.card_reader import ThaiIDReader
from db.db import POSTGRESQL
from ui.alert_box import AlertBox

from datetime import datetime

import os
import traceback
import inspect

class Prisoner_list_popup(QDialog):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.setModal(True)
        self.setMinimumWidth(420)
        self.db = POSTGRESQL()
        self.setObjectName('prisoner_list_popup')

    def show_detail(self, prisoner, title):
        try:
            data_relatives = self.db.get_relatives(prisoner_id=prisoner[0])
        except Exception as e:
            print("get_relatives error:", e)
            data_relatives = []
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(12)

        # หัวข้อใหญ่
        header = QLabel('รายละเอียดผู้ต้องขัง')
        header.setObjectName('Qlabel_header')
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

        # เส้นคั่น
        line = QLabel()
        line.setFixedHeight(2)
        line.setObjectName('Qlabel_line')
        layout.addWidget(line)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(8)


        headers = ['รหัสประจำตัว', 'เพศ', 'ชื่อ', 'สกุล', 'คดี', 'ชั้น', 'แดน', 'ประเภท', 'สถานะ', 'วินัย', 'วันบันทึกข้อมูล']
        for i, label in enumerate(headers):
            value = ''
            if prisoner and i < len(prisoner) and prisoner[i] is not None:
                value = str(prisoner[i])
                if i == 10:
                    try: 
                        dt = datetime.strptime(value.split('.')[0], "%Y-%m-%d %H:%M:%S")
                        months = [
                            "", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
                            "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
                        ]
                        day = dt.day
                        month = months[dt.month]
                        year = dt.year
                        hour = dt.hour
                        minute = dt.minute
                        value = f"{day} {month} {year} เวลา {hour:02d}:{minute:02d} น."
                    except Exception as e:
                        pass  # ถ้าแปลงไม่ได้ ให้แสดงค่าดิบ
            lbl_key = QLabel(label + " :")
            lbl_key.setObjectName('Qlabel_lbl_key')
            lbl_val = QLabel(value)
            lbl_val.setObjectName('Qlabel_lbl_val')
            lbl_val.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            form.addRow(lbl_key, lbl_val)

        rel_header = QLabel('ข้อมูลญาติ')
        rel_header.setObjectName('Qlabel_rel_header')
        form.addRow(rel_header, QLabel(''))
        
        if data_relatives:
            for idx, rel in enumerate(data_relatives, 1):
                try:
                    rel_text = f"{idx}. {rel[1]} {rel[2]} {rel[3]} โทร {rel[4]}\n ความสัมพันธ์ : {rel[5]}"
                except Exception as e:
                    rel_text = f"ข้อมูลผิดปกติ: {rel} ({e})"
                lbl_rel = QLabel(rel_text)
                lbl_rel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
                lbl_rel.setObjectName('Qlabel_lbl_rel')
                form.addRow(QLabel(''), lbl_rel)
        else:
            lbl_none = QLabel("ไม่มีข้อมูลญาติ")
            lbl_none.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            lbl_none.setObjectName('Qlabel_lbl_none')
            form.addRow(QLabel(""), lbl_none)

        layout.addLayout(form)

        btn_close = QPushButton('ปิด')
        btn_close.setObjectName('btn_close')

        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)

    def show_add_relative_form(self, prisoner, title):

        def read_id_card():
            thai_id_card = ThaiIDReader()
            thai_id_card.read_card()
            info = thai_id_card.get_person_info()
            return info

        def get_id_on_smartcard():
            '''
            ตรวจสอบข้อมูลญาติจาก การอ่านบัตรประชาชน
            '''
            try:
                thai_id = read_id_card()
                relative_id = thai_id['cid']
                check_id_in_db(id_card_num=relative_id)

            except Exception as e:
                AlertBox.error(self, 'การอ่านบัตรฯ', 'ตรวจสอบเครื่องอ่านบัตรฯ')
                func = inspect.currentframe().f_code.co_name
                self.db.log_error(
                function_name=f"{os.path.basename(__file__)}::{self.__class__.__name__}::{func}",
                error_message=f"Error in {func}::: {e}",
                extra_info=traceback.format_exc()
                )
                print(f'ปัญหาการอ่านบัตร {e}')

        def check_id_in_db(id_card_num = None):
            '''
                เอาเลขบัตรไปตรวจสอบใน ฐานข้อมูล
            '''
            rel_data = self.db.get_relative_data(id_card_num)
            print(rel_data)
            if rel_data:
                self.input_id_card.setText(str(rel_data[0]))
                self.input_title.setEditText(str(rel_data[1]))
                self.input_fname.setText(str(rel_data[2]))
                self.input_lname.setText(str(rel_data[3]))
                self.input_address.setText(str(rel_data[4]))
                self.input_tel.setText(str(rel_data[5]))
            else:
                AlertBox.error(self, 'ไม่พบข้อมูล', 'ไม่พบข้อมูลญาติในระบบ โปรดป้อนข้อมูลด้วยตนเอง')
        
        def save_relative_relation_to_db(prisoner):
            '''
            บันทึกข้อมุลลง db'''
            print(prisoner)

            relative_id = self.input_id_card.text()
            prisoner_id = prisoner[0]
            title = self.input_title.currentText()       
            f_name = self.input_fname.text(),
            l_name = self.input_lname.text(),
            address = self.input_address.toPlainText(),
            tel = self.input_tel.text(),
            relation = self.input_relation.currentText(),

            if not all([relative_id, title, f_name, l_name, address, tel, relation]):
                AlertBox.warning(self, 'กรอกข้อมูลไม่ครบ', 'กรุณากรอกข้อมูลให้ครบทุกช่อง')
                return

            from user.login import USER_NAME
            # print(self.input_id_card.text())
            result_insert_data = self.db.insert_relative_and_relation(
                relative_id = relative_id,
                prisoner_id = prisoner_id,
                title = title,
                f_name = f_name,
                l_name = l_name,
                address = address,
                tel = tel,
                relation = relation,
                user_insert = USER_NAME
            )
            if result_insert_data:
                AlertBox.info(self, title='บันทึกข้อมูล', message=f'บันทึกข้อมูลญาติของ {prisoner[2]} {prisoner[3]} สำเร็จ')
                self.close()
            else:
                AlertBox.error(self, title='บันทึกข้อมูล', message=f'บันทึกข้อมูลญาติของ {prisoner[2]} {prisoner[3]} ไม่สำเร็จ')
            
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        regex = QRegularExpression(r"\d{0,13}")

        header_label = QLabel(f'เพิ่ม/แก้ไข ข้อมูลญาติ ราย "{prisoner[2]} {prisoner[3]}"')
        header_label.setObjectName('header_label')
        layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_btn_read_card = QPushButton('อ่านบัตรฯ')
        self.input_btn_read_card.setObjectName('Qpush_input_btn_read_card')
        self.input_btn_read_card.setAutoDefault(False)
        self.input_btn_read_card.setDefault(False)
        self.input_btn_read_card.clicked.connect(lambda: get_id_on_smartcard())
        self.input_id_card = QLineEdit()
        self.input_id_card.setPlaceholderText('ป้อนหมายเลขแล้วกด Enter เพื่อค้นหา')
        self.input_id_card.setValidator(QRegularExpressionValidator(regex))
        self.input_id_card.setMaxLength(13)
        self.input_id_card.returnPressed.connect(lambda: check_id_in_db(self.input_id_card.text()))

        self.input_title = QComboBox()
        self.input_fname = QLineEdit()
        self.input_lname = QLineEdit()
        self.input_address = QTextEdit()
        self.input_tel = QLineEdit()
        self.input_relation = QComboBox()

        self.input_title.addItems(['นาย','นาง','นางสาว','เด็กหญิง','เด็กชาย', ])
        self.input_relation.addItems(['ปู่', 'ย่า', 'ตา', 'ยาย', 'ลุง', 'ป้า', 'พ่อ', 'แม่', 'น้า', 'พี่ชาย', 'พี่สาว', 'น้องชาย', 'น้องสาว', 'สามี', 'ภรรยา', 'ลูกสาว', 'ลูกชาย', 'อื่น ๆ'])

        form.addRow('', self.input_btn_read_card)
        form.addRow('หมายเลขบัตรฯ ', self.input_id_card)
        form.addRow('คำนำหน้า', self.input_title)
        form.addRow('ชื่อ', self.input_fname)
        form.addRow('นามสกุล', self.input_lname)
        form.addRow('ที่อยู่', self.input_address)
        form.addRow('เบอร์โทร', self.input_tel)
        form.addRow('ความสัมพันธ์', self.input_relation)

        layout.addLayout(form)

        btn_save = QPushButton('บันทึก')
        btn_save.setObjectName('Qpush_btn_save')
        btn_save.setAutoDefault(False)
        btn_save.setDefault(False)
        btn_save.clicked.connect(lambda: save_relative_relation_to_db(prisoner))

        btn_close = QPushButton('ปิด')
        btn_close.setObjectName('Qpush_btn_close')
        btn_close.setAutoDefault(False)
        btn_close.setDefault(False)
        btn_close.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)

    def show_delete_relative_form(self, prisoner, title):
        def delete_relative_form_db(pri_id, rel_id, is_active):
            result = AlertBox.question(self, 'ลบข้อมูล', f'ต้องการลบความสัมพันธ์ ผตข.ราย{prisoner[2]} {prisoner[3]} \nกับ\nญาติ ราย{rel_id} ')
            if result:
                self.close()
                if self.db.updete_relation(prisoner_id=str(pri_id), relative_id=str(rel_id),is_active=is_active):
                    AlertBox.success(self, 'เพิ่ม/ลบ ความสัมพันธ์', 'เพิ่ม/ลบ ความสัมพันธ์สำเร็จ')
                else:
                    AlertBox.error(self, 'เพิ่ม/ลบ ความสัมพันธ์', 'เพิ่ม/ลบ ความสัมพันธ์ไม่สำเร็จ')
            else:
                self.close()
                AlertBox.error(self, 'เพิ่ม/ลบ ความสัมพันธ์', 'เพิ่ม/ลบ ความสัมพันธ์ไม่สำเร็จ')

        try:
            data_relatives = self.db.get_relatives(prisoner_id=prisoner[0])
        except Exception as e:
            print("get_relatives error:", e)
            data_relatives = []

        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        header_label = QLabel(f'รายชื่อญาติของ "{prisoner[2]} {prisoner[3]}"')
        header_label.setObjectName('header_label')
        layout.addWidget(header_label,alignment=Qt.AlignmentFlag.AlignCenter)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #bdbdbd; background: #bdbdbd; min-height:2px; max-height:2px;")
        layout.addWidget(line)

        if data_relatives:
            for index, value in enumerate(data_relatives,1):
                try:
                    rel_text = f"{index}. {value[1]} {value[2]} {value[3]}\n ความสัมพันธ์ : {value[5]}"
                except Exception as e:
                    rel_text = f"ข้อมูลผิดปกติ: {value} ({e})"
                layout_hb = QHBoxLayout()
                lbl_rel = QLabel(rel_text)
                lbl_rel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
                lbl_rel.setObjectName('Qlabel_lbl_rel')
                btn_delete = QPushButton()
                btn_delete.setFixedWidth(50)
                btn_delete.setObjectName('btn_delete')
                btn_delete.setText('ลบข้อมูล')
                
                btn_delete.clicked.connect(lambda checked, rel_id = value[0], pri_id = prisoner[0]: delete_relative_form_db(pri_id, rel_id, False))
                layout_hb.addWidget(lbl_rel)
                layout_hb.addWidget(btn_delete, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
                layout.addLayout(layout_hb)
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setStyleSheet("color: #bdbdbd; background: #bdbdbd; min-height:2px; max-height:2px;")
                layout.addWidget(line)

        else:
            lbl_none = QLabel("ไม่มีข้อมูลญาติ")
            lbl_none.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            lbl_none.setObjectName('Qlabel_lbl_none')
            layout.addWidget(lbl_none)

    def edit_data_prisoner(self, prisoner, title):
        self.windowTitle(title)
        layout = QVBoxLayout(self)
        header_label = QLabel(f'แก้ไขข้อมูลผู้ต้องขัง "{prisoner[2]} {prisoner[3]}"')
        header_label.setObjectName('header_label')
        layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        h_layout = QHBoxLayout()

        form = QFormLayout()
        form.setVerticalSpacing(24)
        form.setHorizontalSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        form.setFormAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addLayout(form)
        layout.addLayout(h_layout)
