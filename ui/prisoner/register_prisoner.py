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

class Prisoner_register_widget(QWidget):
    def __init__(self):
        super().__init__()

        self.db = POSTGRESQL()

        self.setObjectName("main_prisoner_widget")
        main_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        form = QFormLayout()
        form.setVerticalSpacing(24)
        form.setHorizontalSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        form.setFormAlignment(Qt.AlignmentFlag.AlignCenter)

        register_label = QLabel('ลงทะเบียนผู้ต้องขัง')
        register_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        register_label.setStyleSheet('''
                                     font-size: 22px;
                                     font-weight: bold;
                                     color: #000000;
                                     margin-bottom: 1px;
                                     margin-top: 10px;
        ''')

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

        self.setStyleSheet('''
            #main_prisoner_widget {
                background: #fff;
                border: 1.5px solid #e0e0e0;
                border-radius: 10px;
                margin: 10px 10px 10px 1px;
            }
            QWidget {
                background: #fff;
                color: #222;
                font-family: 'Sarabun', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #333;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background: #f5f6fa;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 6px;
                color: #222;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1.5px solid #5e81f4;
                background: #fff;
            }
            QPushButton#btn_submit {
                background-color: #5e81f4;
                color: #fff;
                border: none;
                border-radius: 6px;
                padding: 8px 0;
                font-weight: bold;
            }            
            QPushButton#btn_clear {
                background-color: #e0e0e0;
                color: #333;  /* สีเทาเข้มหรือดำ อ่านง่ายบนพื้นเทา */
                border: none;
                border-radius: 6px;
                padding: 8px 0;
                font-weight: bold;
            }
            QPushButton#btn_submit:hover {
                background-color: #4666c9;
            }
            QPushButton#btn_clear:hover {
                background-color: #b0bec5;
            }
            QComboBox {
                    background: #f5f6fa;
                    border: 1.5px solid #e0e0e0;
                    border-radius: 6px;
                    padding: 6px 30px 6px 10px;
                    color: #222;
                    font-size: 14px;
            }
            QComboBox:focus {
                border: 1.5px solid #5e81f4;
                background: #fff;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border-left: 1px solid #e0e0e0;
                background: #e0e0e0;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QComboBox::down-arrow {
                image: url(:/qt-project.org/styles/commonstyle/images/arrowdown-16.png);
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                background: #fff;
                border: 1px solid #e0e0e0;
                selection-background-color: #5e81f4;
                selection-color: #fff;
                font-size: 14px;
            }
            QLineEdit, QComboBox, QTextEdit {
                background: #f5f6fa;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 6px;
                color: #222;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1.5px solid #5e81f4;
                background: #fff;
            }
            QTextEdit {
                background: #f5f6fa;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 6px;
                color: #222;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1.5px solid #5e81f4;
                background: #fff;
            }
            /* ตกแต่ง scrollbar ของ QTextEdit */
            QTextEdit QScrollBar:vertical {
                background: #e0e0e0;
                width: 12px;
                margin: 2px 0 2px 0;
                border-radius: 6px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background: #b0bec5;
                min-height: 20px;
                border-radius: 6px;
            }
            QTextEdit QScrollBar::handle:vertical:hover {
                background: #5e81f4;
            }
            QTextEdit QScrollBar::add-line:vertical, QTextEdit QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QTextEdit QScrollBar::add-page:vertical, QTextEdit QScrollBar::sub-page:vertical {
                background: none;
            }
        ''')

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
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle('กรอกข้อมูลไม่ครบ')
            msg.setText('กรุณากรอกข้อมูลให้ครบทุกช่อง')
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f6fa;
                    font-family: 'Sarabun', Arial, sans-serif;
                    font-size: 16px;
                }
                QLabel {
                    color: #333;
                }
                QPushButton {
                    background-color: #5e81f4;
                    color: #fff;
                    border-radius: 6px;
                    padding: 6px 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4666c9;
                }
            """)
            msg.exec()
        result = self.db.insert_prisoner(id, gender, f_name, l_name, lawsuit, level, dan, p_type, status)
        if result:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle('บันทึกข้อมูล')
            msg.setText(f'บันทึกข้อมูล {id} สำเร็จ')
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f6fa;
                    font-family: 'Sarabun', Arial, sans-serif;
                    font-size: 16px;
                }
                QLabel {
                    color: #333;
                }
                QPushButton {
                    background-color: #5e81f4;
                    color: #fff;
                    border-radius: 6px;
                    padding: 6px 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4666c9;
                }
            """)
            msg.exec()
            self.clear_data()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle('บันทึกข้อมูล')
            msg.setText(f'บันทึกข้อมูลไม่สำเร็จ')
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f6fa;
                    font-family: 'Sarabun', Arial, sans-serif;
                    font-size: 16px;
                }
                QLabel {
                    color: #333;
                }
                QPushButton {
                    background-color: #5e81f4;
                    color: #fff;
                    border-radius: 6px;
                    padding: 6px 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4666c9;
                }
            """)
            msg.exec()
