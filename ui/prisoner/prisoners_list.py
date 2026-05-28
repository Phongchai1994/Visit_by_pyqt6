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

from db.db import POSTGRESQL
from db.db import log_db_exceptions
from ui.alert_box import AlertBox
from devices.card_reader import ThaiIDReader

from datetime import datetime

import os
import traceback
import inspect

class PrisonersTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row_data = self._data[index.row()]
        value = row_data[index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            return "" if value is None else str(value)

        if role == Qt.ItemDataRole.ForegroundRole:
            status_value = row_data[8] if len(row_data) > 8 else None
            discipline_value = row_data[9] if len(row_data) > 9 else None

            if discipline_value not in (None, "", "null", "None"):
                return QBrush(QColor("#d32f2f"))

            if status_value == "ไม่อยู่":
                return QBrush(QColor("#b0b0b0"))

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            else:
                return section + 1
        return None

class ResponsiveTableView(QTableView):
    def __init__(self, proportions, parent=None):
        super().__init__(parent)
        self.proportions = proportions
        self.setObjectName('Qtable_View')

    def apply_column_widths(self):
        model = self.model()
        if model is None:
            return

        total_width = self.viewport().width()
        if total_width <= 0:
            return

        for i, proportion in enumerate(self.proportions):
            self.setColumnWidth(i, max(20, int(total_width * proportion)))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.apply_column_widths()

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


class Prisoners_list(QWidget):
    def __init__(self):
        super().__init__()
        self.db = POSTGRESQL()

        self.setObjectName('main_prisoner_list_widget')
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 12, 20, 12)
     
        # หัวข้อ
        title_label = QLabel('รายชื่อผู้ต้องขัง')
        title_label.setObjectName('Qlabel_title_lable')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        vbox = QVBoxLayout()
        vbox.addItem(QSpacerItem(0, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        vbox.addWidget(title_label)

        main_layout.addLayout(vbox)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.proportions = [
            0.06,  # รหัสประจำตัว
            0.04,  # เพศ
            0.10,  # ชื่อ
            0.10,  # สกุล
            0.38,  # คดี
            0.08,  # ชั้น
            0.06,  # แดน
            0.06,  # ประเภท
            0.06,  # สถานะ
            0.06,  # วินัย
        ]
        self.table_view = None

        self.filer_options = {
            'เพศ': [],
            'ชั้น': [],
            'แดน': [],
            'ประเภท': [],
            'สถานะ': [],
            'วินัย': []
        }
        self.search_text = ''
        self.create_filter_ui(main_layout)
        self.load_prisoners()
        self.apply_filters()

    def create_filter_ui(self,layout):
        filter_layout = QGridLayout()

        # เพศ
        gender_group = QGroupBox('เพศ')
        self.gender_checkboxes = []
        gender_male = QCheckBox('ชาย')
        gender_female = QCheckBox('หญิง')
        for cb in [gender_male, gender_female]:
            cb.stateChanged.connect(self.apply_filters)
            self.gender_checkboxes.append(cb)
        gender_layout = QGridLayout()
        gender_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        gender_layout.addWidget(gender_male, 0, 0)
        gender_layout.addWidget(gender_female, 1, 0)
        gender_group.setLayout(gender_layout)
        filter_layout.addWidget(gender_group, 0, 0)

        # ชั้น
        level_group = QGroupBox('ชั้น')
        levels = ['ระหว่างพิจารณาคดี', 'เยี่ยม', 'ดีมาก', 'ดี', 'กลาง', 'ปรับปรุง', 'ปรับปรุงมาก']
        self.level_checkboxes = []
        level_layout = QGridLayout()
        level_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for i, level in enumerate(levels):
            cb = QCheckBox(level)
            cb.stateChanged.connect(self.apply_filters)
            self.level_checkboxes.append(cb)
            level_layout.addWidget(cb, i // 2, i % 2)
        level_group.setLayout(level_layout)
        filter_layout.addWidget(level_group, 0, 1)

        # แดน
        dan_group = QGroupBox('แดน')
        dan_names = ['รจช', "7", "6", "5", "4", "3", "2", "1"]
        self.dan_checkboxes = []
        dan_layout = QGridLayout()
        dan_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for i, dan in enumerate(dan_names):
            cb = QCheckBox(dan)
            cb.stateChanged.connect(self.apply_filters)
            self.dan_checkboxes.append(cb)
            dan_layout.addWidget(cb, i // 2, i % 2)
        dan_group.setLayout(dan_layout)
        filter_layout.addWidget(dan_group, 0, 2)
        
        # ประเภท
        type_group = QGroupBox('ประเภท')
        type_names =['ผู้ต้องขัง', 'ผู้ต้องกักขัง']
        self.type_checkboxes = []
        type_layout = QGridLayout()
        type_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for i, type_ in enumerate(type_names):
            cb = QCheckBox(type_)
            cb.stateChanged.connect(self.apply_filters)
            self.type_checkboxes.append(cb)
            type_layout.addWidget(cb, i // 2, i % 2)
        type_group.setLayout(type_layout)
        filter_layout.addWidget(type_group, 0, 3)

        # สถานะ
        status_group = QGroupBox('สถานะ')
        status_names = ['อยู่', 'ไม่อยู่']
        self.status_checkboxes = []
        status_layout = QGridLayout()
        status_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for i, status in enumerate(status_names):
            cb = QCheckBox(status)
            if status == 'อยู่':
                cb.setChecked(True)
            cb.stateChanged.connect(self.apply_filters)
            self.status_checkboxes.append(cb)
            status_layout.addWidget(cb, i // 2, i % 2)
        status_group.setLayout(status_layout)
        filter_layout.addWidget(status_group, 0, 4)

        # วินัย
        disciplinary_group = QGroupBox('วินัย')
        self.disciplinary_checkbox = []
        disciplinary_layout = QGridLayout()
        disciplinary_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        cb_disciplinary = QCheckBox('ผิดวินัย')
        cb_disciplinary.stateChanged.connect(self.apply_filters)
        self.disciplinary_checkbox.append(cb_disciplinary)
        disciplinary_layout.addWidget(cb_disciplinary, 0, 0)
        disciplinary_group.setLayout(disciplinary_layout)
        filter_layout.addWidget(disciplinary_group, 0, 5)

        # ช่องค้นหา
        search_group = QGroupBox('ค้นหาและแสดงผล')
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText('ค้นหาด้วย เลขประจำตัว ชื่อหรือสกุล...')
        self.search_box.textChanged.connect(self.apply_filters)
        search_layout = QGridLayout()
        search_layout.addWidget(self.search_box, 0, 0)

        self.result_count_label = QLabel()
        self.result_count_label.setText("จำนวนทั้งหมด : 0 ราย")
        search_layout.addWidget(self.result_count_label, 1, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom )

        search_group.setLayout(search_layout)
        filter_layout.addWidget(search_group, 0, 6)
        
        layout.addLayout(filter_layout)

    def apply_filters(self):
        # ดึงค่าจาก checkbox และ search box
        search_text = self.search_box.text().strip().lower()
        genders = [cb.text() for cb in self.gender_checkboxes if cb.isChecked()]
        levels = [cb.text() for cb in self.level_checkboxes if cb.isChecked()]
        dans = [cb.text() for cb in self.dan_checkboxes if cb.isChecked()]
        types = [cb.text() for cb in self.type_checkboxes if cb.isChecked()]
        status = [cb.text() for cb in self.status_checkboxes if cb.isChecked()]
        disciplinary = [cb.text() for cb in self.disciplinary_checkbox if cb.isChecked()]
        filtered = []
        for row in self.all_prisoners:
            # row: [รหัส, เพศ, ชื่อ, สกุล, ...]
            if search_text and (search_text not in row[2].lower() and search_text not in row[3].lower() and search_text not in str(row[0]).lower()):
                continue
            if genders and row[1] not in genders:
                continue
            if levels and row[5] not in levels:
                continue
            if dans and row[6] not in dans:
                continue
            if types and row[7] not in types:
                continue
            if status and row[8] not in status:
                continue
            if disciplinary and row[9] not in disciplinary:
                continue
            # เพิ่มเงื่อนไง
            filtered.append(row)
        self.result_count_label.setText(f'จำนวนทั้งหมด : {len(filtered)} ราย')
        self.table_model._data = filtered
        self.table_model.layoutChanged.emit()
        self.table_view.apply_column_widths()

    def load_prisoners(self):
        prisoners = self.db.get_all_prisoners_list()
        if not prisoners:
            AlertBox.error(self, 'load prisoner', 'ดึงข้อมูลผู้ต้องขังไม่สำเร็จ')
            return
        self.all_prisoners = prisoners # เก็บข้อมูลไว้
        headers = ['รหัสประจำตัว', 'เพศ', 'ชื่อ', 'สกุล', 'คดี', 'ชั้น', 'แดน', 'ประเภท', 'สถานะ', 'วินัย']

        self.table_model = PrisonersTableModel(prisoners, headers)
        self.table_view = ResponsiveTableView(self.proportions)
        self.table_view.setModel(self.table_model)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setAlternatingRowColors(True)

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        header.setStretchLastSection(False)


        self.table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.create_table_context_menu)

        self.layout().addWidget(self.table_view)
        self.table_view.apply_column_widths()

    def create_table_context_menu(self, position):
        index = self.table_view.indexAt(position)
        if not index.isValid():
            return
        menu = QMenu()
        menu.setObjectName('menu_prisoner_list')

        # ดึงชื่อ - สกุลจากตาราง
        row_data = self.table_model._data[index.row()]
        prisoner_name = f'{row_data[2]} {row_data[3]}'

        # เพิ่มเมนู
        name_action = QAction(prisoner_name, self)
        name_action.setEnabled(False)
        menu.addAction(name_action)
        menu.addSeparator()

        action_detail = QAction('ดูรายละเอียด', self)
        action_add_relative = QAction('เพิ่ม/แก้ไข ญาติ', self)
        action_del_relative = QAction('ลบญาติ', self)
        action_edit_prisoner = QAction('แก้ไขข้อมูลผู้ต้องขัง', self)

        action_detail.triggered.connect(lambda: self.show_detail(index.row()))
        action_add_relative.triggered.connect(lambda: self.add_relative(index.row()))
        action_del_relative.triggered.connect(lambda: self.delete_relative(index.row()))
        action_edit_prisoner.triggered.connect(lambda:print('แก้ไขข้อมูลผู้ต้องขัง'))
        
        menu.addAction(action_detail)
        menu.addSeparator()  # เส้นคั่น
        menu.addAction(action_add_relative)
        menu.addAction(action_del_relative)
        menu.addSeparator()  # เส้นคั่น
        menu.addAction(action_edit_prisoner)

        # ปรับสไตล์เมนู (ตัวอย่าง)
        menu.setStyleSheet("""
            QMenu {
                font-family: 'Sarabun', Arial, sans-serif;
                font-size: 14px;
                background: #FFFFFF;
                border: 1.5px solid #000000;
                color: #222;
                border-radius: 8px;
                padding: 4px;
                min-width: 160px;
            }

            QMenu::item {
                padding: 6px 24px;
                color: #0c5b9c;
                border-radius: 4px;
                background: transparent;
            }

            QMenu::item:selected,
            QMenu::item:hover {
                background-color: #b3d1ff;
                color: #0d47a1;
            }

            QMenu::separator {
                height: 1px;
                background: #b0b0b0;
                margin: 4px 0 4px 0;
                border-radius: 1px;
            }
        """)
        
        menu.exec(self.table_view.viewport().mapToGlobal(position))

    def show_detail(self, row):
        data = self.table_model._data[row]
        dialog = Prisoner_list_popup(self)
        dialog.show_detail(data, title=f'รายละเอียด ราย {data[2]} {data[3]}')
        dialog.exec()

    def add_relative(self, row):
        data = self.table_model._data[row]
        dialog = Prisoner_list_popup(self)
        dialog.show_add_relative_form(data, title=f'เพิ่มข้อมูลญาติ ราย {data[2]} {data[3]}')
        dialog.exec()

    def delete_relative(self, row):
        data = self.table_model._data[row]
        dialog = Prisoner_list_popup(self)
        dialog.show_delete_relative_form(data, title=f'ลบข้อมูลญาติ ราย {data[2]} {data[3]}')
        dialog.exec()





















