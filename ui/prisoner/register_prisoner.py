from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QFormLayout, 
    QMessageBox, 
    QComboBox, 
    QTextEdit, 
    QSpacerItem, 
    QSizePolicy
)
from PyQt6.QtCore import (
    Qt,
    QRegularExpression
)
from PyQt6.QtGui import (
    QColor, 
    QIntValidator,
    QRegularExpressionValidator
)
from db.db import POSTGRESQL
from ui.alert_box import AlertBox


class Prisoner_register_widget(QWidget):
    def __init__(self):
        super().__init__()

        self.db = POSTGRESQL()

        self.setObjectName("prisoner_register_widget")
        main_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        form = QFormLayout()
        form.setVerticalSpacing(24)
        form.setHorizontalSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        form.setFormAlignment(Qt.AlignmentFlag.AlignCenter)

        register_label = QLabel('ลงทะเบียนผู้ต้องขัง')
        register_label.setObjectName('register_label')
        register_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # สร้าง input
        self.input_id = QLineEdit()
        self.input_id.setValidator(QIntValidator()) # ป้อนได้แค่ตัวเลข
        self.input_gender = QComboBox()
        self.input_f_name = QLineEdit()
        self.input_l_name = QLineEdit()
        self.input_lawsuit = QTextEdit()
        self.input_level = QComboBox()
        self.input_dan = QComboBox()
        self.input_type = QComboBox()
        self.input_status = QComboBox()
        self.btn_submit = QPushButton('บันทึกข้อมูล')
        self.btn_submit.setObjectName('btn_submit')
        self.btn_clear = QPushButton('ล้างค่า')
        self.btn_clear.setObjectName('btn_clear')

        # ไม่ให้ป้อนค่าว่าง
        no_space_validator = QRegularExpressionValidator(QRegularExpression(r"^[^\s]+$"))
        self.input_f_name.setValidator(no_space_validator)
        self.input_l_name.setValidator(no_space_validator)

        # ใส่ข้อมูลให้ combobox
        self.input_gender.addItems(['ชาย','หญิง'])
        self.input_level.addItems(['ระหว่างพิจารณาคดี','เยี่ยม','ดีมาก','ดี','กลาง','ปรับปรุง','ปรับปรุงมาก'])
        self.input_dan.addItems(['รจช','7','6','5','4','3','2'])
        self.input_type.addItems(['ผู้ต้องขัง','ผู้ต้องกักขัง'])
        self.input_status.addItems(['อยู่', 'ไม่อยู่'])
        self.input_status.setDisabled(True)
        self.input_dan.setCurrentText('7') # ค่าเริ่มต้นเป็น 7

        # ขนาด field
        field_width = 300
        self.input_id.setFixedWidth(field_width)
        self.input_gender.setFixedWidth(field_width)
        self.input_f_name.setFixedWidth(field_width)
        self.input_l_name.setFixedWidth(field_width)
        self.input_lawsuit.setFixedHeight(62)
        self.input_lawsuit.setFixedWidth(field_width)
        self.input_level.setFixedWidth(field_width)
        self.input_dan.setFixedWidth(field_width)
        self.input_type.setFixedWidth(field_width)
        self.input_status.setFixedWidth(field_width)
        self.btn_submit.setFixedWidth(200)
        self.btn_clear.setFixedWidth(200)

        # form
        form.addItem(QSpacerItem(0,12))
        form.addRow(register_label)
        form.addRow('รหัสประจำตัว :', self.input_id)
        form.addRow('เพศ :', self.input_gender)
        form.addRow('ชื่อ : ', self.input_f_name)
        form.addRow('สกุล : ', self.input_l_name)
        form.addRow('คดี : ', self.input_lawsuit)
        form.addRow('ชั้น : ', self.input_level)
        form.addRow('แดน : ', self.input_dan)
        form.addRow('ประเภท : ', self.input_type)
        form.addRow('สถานะ : ', self.input_status)

        # ปุ่มกึ่งกลาง
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(20, 0, 20, 0)
        btn_layout.setSpacing(24)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch(1)
        form.addRow(btn_layout)
        form.addItem(QSpacerItem(0, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        h_layout.addStretch(1)
        h_layout.addLayout(form)
        h_layout.addStretch(1)

        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 12, 20, 12) 
        main_layout.addLayout(h_layout)

        self.setLayout(main_layout)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.input_gender.currentTextChanged.connect(self.update_dan_options)
        self.btn_submit.clicked.connect(self.save_data)
        self.btn_clear.clicked.connect(self.clear_data)


    def update_dan_options(self):
        gender = self.input_gender.currentText()
        if gender == 'หญิง':
            self.input_dan.clear()
            self.input_dan.addItems(['1'])
        else:
            self.input_dan.clear()
            self.input_dan.addItems(['รจช','7','6','5','4','3','2'])
            self.input_dan.setCurrentText('7')

    def clear_data(self):
        self.input_id.clear()
        self.input_gender.setCurrentIndex(0)
        self.input_f_name.clear()
        self.input_l_name.clear()
        self.input_lawsuit.clear()
        self.input_level.setCurrentIndex(0)
        self.input_dan.setCurrentIndex(1)
        self.input_type.setCurrentIndex(0)
        self.input_status.setCurrentIndex(0)

    def save_data(self):
        id = self.input_id.text().strip()
        gender = self.input_gender.currentText().strip()
        f_name = self.input_f_name.text().strip()
        l_name = self.input_l_name.text().strip()
        lawsuit = self.input_lawsuit.toPlainText()
        level = self.input_level.currentText().strip()
        dan = self.input_dan.currentText().strip()
        p_type = self.input_type.currentText().strip()
        status = self.input_status.currentText().strip()
        
        if not all([id, gender, f_name, l_name, lawsuit, level, dan, p_type, status]):
            AlertBox.warning(self, 'กรอกข้อมูลไม่ครบ', 'กรุณากรอกข้อมูลให้ครบทุกช่อง')
            return
        result = self.db.insert_and_update_prisoner(id, gender, f_name, l_name, lawsuit, level, dan, p_type, status)
        if result:
            AlertBox.info(self, 'บันทึกข้อมูล', f'บันทึกข้อมูล {id} สำเร็จ')
            self.clear_data()
        else:
            AlertBox.warning(self, 'บันทึกข้อมูล', 'บันทึกข้อมูลไม่สำเร็จ')
