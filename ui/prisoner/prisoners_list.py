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
    QPushButton
)

from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QBrush, QColor ,QAction

from db.db import POSTGRESQL
from ui.alert_box import AlertBox

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
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #1a237e; margin-bottom: 8px;")
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

        # เส้นคั่น
        line = QLabel()
        line.setFixedHeight(2)
        line.setStyleSheet("background: #b0bec5; margin-bottom: 8px;")
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
            lbl_key = QLabel(label + " :")
            lbl_key.setStyleSheet("color: #37474f; font-weight: bold;")
            lbl_val = QLabel(value)
            lbl_val.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            lbl_val.setStyleSheet("color: #263238;")
            form.addRow(lbl_key, lbl_val)

        rel_header = QLabel('ข้อมูลญาติ')
        rel_header.setStyleSheet('font-size: 16px; font-weight: bold; color: #1565c0; margin-top: 12px;')
        form.addRow(rel_header, QLabel(''))
        
        if data_relatives:
            for idx, rel in enumerate(data_relatives, 1):
                try:
                    rel_text = f"{idx}. {rel[1]} {rel[2]} {rel[3]} โทร {rel[4]}\n ความสัมพันธ์ : {rel[5]}"
                except Exception as e:
                    rel_text = f"ข้อมูลผิดปกติ: {rel} ({e})"
                lbl_rel = QLabel(rel_text)
                lbl_rel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
                lbl_rel.setStyleSheet("color: #37474f; margin-bottom: 2px;")
                form.addRow(QLabel(''), lbl_rel)
        else:
            lbl_none = QLabel("ไม่มีข้อมูลญาติ")
            lbl_none.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            lbl_none.setStyleSheet("color: #b71c1c;")
            form.addRow(QLabel(""), lbl_none)

        layout.addLayout(form)

        btn_close = QPushButton('ปิด')
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: #fff;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0d47a1;
            }
        """)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)

    def add_reltive(self, prisoner, title):
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        data = self.db.get_relatives(prisoner_id=prisoner[0])
        if not data:
            form.addRow(QLabel('ไม่มีข้อมูลญาติ'), QLabel(''))
        else:
            for rel in data:
                name = f'{rel[1]} {rel[2]} {rel[3]}'
                info = f'{rel[4]} - {rel[5]}'
                form.addRow(QLabel(name), QLabel(info))
        layout.addLayout(form)
        btn_close = QPushButton('ปิด')
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)

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
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet('''
            font-size: 22px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 1px;
            margin-top: 10px;
        ''')

        # Layout
        vbox = QVBoxLayout()
        vbox.addItem(QSpacerItem(0, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        vbox.addWidget(title_label)

        main_layout.addLayout(vbox)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
                    #main_prisoner_list_widget {
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
                        font-family: 'Sarabun', Arial, sans-serif;
                           
                    }
                    QTableView {
                        background: #f5f6fa;
                        border: 1px solid #e0e0e0;
                        border-radius: 6px;
                        color: #222;
                        font-size: 14px;
                        gridline-color: #e8e8e8;
                        selection-background-color: #d9e8ff;
                        selection-color: #111;
                    }
                    QHeaderView::section {
                        background: #e0e0e0;
                        color: #222;
                        font-weight: bold;
                        border: none;
                        border-radius: 6px;
                        padding: 6px;
                    }
                    QScrollBar:vertical {
                        background: #f0f0f0;
                        width: 10px;
                        margin: 2px 2px 2px 2px;
                        border-radius: 5px;
                    }
                    QScrollBar::handle:vertical {
                        background: #b8c0cc;
                        min-height: 30px;
                        border-radius: 5px;
                    }
                    QScrollBar::handle:vertical:hover {
                        background: #9da9b7;
                    }
                    QScrollBar::add-line:vertical,
                    QScrollBar::sub-line:vertical {
                        height: 0px;
                        background: none;
                    }
                    QScrollBar:horizontal {
                        background: #f0f0f0;
                        height: 10px;
                        margin: 2px 2px 2px 2px;
                        border-radius: 5px;
                    }
                    QScrollBar::handle:horizontal {
                        background: #b8c0cc;
                        min-width: 30px;
                        border-radius: 5px;
                    }
                    QScrollBar::handle:horizontal:hover {
                        background: #9da9b7;
                    }
                    QScrollBar::add-line:horizontal,
                    QScrollBar::sub-line:horizontal {
                        width: 0px;
                        background: none;
                    }
                    QLineEdit {
                        background: #f5f6fa;
                        border: 1px solid #e0e0e0;
                        border-radius: 6px;
                        padding: 6px;
                        color: #222;
                    }
                    QLineEdit:focus {
                        border: 1.5px solid #5e81f4;
                        background: #fff;
                    }    
                    QCheckBox {
                        spacing: 8px;
                        font-size: 14px;
                        color: #222;
                        padding: 2px 0 2px 4px;
                    }
                    QCheckBox::indicator {
                        width: 18px;
                        height: 18px;
                        border-radius: 4px;
                        border: 1.5px solid #5e81f4;
                        background: #fff;
                    }
                    QCheckBox::indicator:checked {
                        background: #5e81f4;
                        border: 1.5px solid #4666c9;
                    }
                    QCheckBox::indicator:unchecked {
                        background: #fff;
                        border: 1.5px solid #b0b0b0;
                    }
                    QCheckBox::indicator:disabled {
                        background: #e0e0e0;
                        border: 1.5px solid #b0b0b0;
                    }
                """)
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
        self.search_box.setPlaceholderText('ค้นหาด้วยชื่อหรือสกุล...')
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
            if search_text and (search_text not in row[2].lower() and search_text not in row[3].lower()):
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

        # ดึงชื่อ - สกุลจากตาราง
        row_data = self.table_model._data[index.row()]
        prisoner_name = f'{row_data[2]} {row_data[3]}'

        # เพิ่มเมนู
        name_action = QAction(prisoner_name, self)
        name_action.setEnabled(False)
        menu.addAction(name_action)
        menu.addSeparator()

        action_detail = QAction('ดูรายละเอียด', self)
        action_add_relative = QAction('เพิ่มญาติ', self)
        action_del_relative = QAction('ลบญาติ', self)
        action_edit_prisoner = QAction('แก้ไขข้อมูลผู้ต้องขัง', self)

        action_detail.triggered.connect(lambda: self.show_detail(index.row()))
        action_add_relative.triggered.connect(lambda: self.add_relative(index.row()))
        action_del_relative.triggered.connect(lambda:print('ลบญาติ'))
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
            }
            QMenu::item {
                padding: 6px 24px 6px 24px;
                color: #0c5b9c
            }
            QMenu::item:selected {
                background-color: #d9e8ff;
                color: #12344f;
            }
            QMenu::separator {
                height: 1px;
                background: #b0b0b0;
                margin: 4px 0 4px 0;
            }
        """)
        
        menu.exec(self.table_view.viewport().mapToGlobal(position))

    def show_detail(self, row):
        # ตัวอย่าง: แสดงข้อมูลแถวที่เลือก
        data = self.table_model._data[row]
        # คุณสามารถแสดง popup หรือ dialog ตามต้องการ

        dialog = Prisoner_list_popup(self)
        dialog.show_detail(data, title='รายละเอียด')
        dialog.exec()



    def add_relative(self, row):
        data = self.table_model._data[row]
        dialog = Prisoner_list_popup(self)
        dialog.add_reltive(data, title='เพิ่มข้อมูลญาติ')
        dialog.exec()






















