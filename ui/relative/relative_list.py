from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableView,
    QSpacerItem,
    QSizePolicy,
    QHeaderView,
    QGroupBox,
    QCheckBox,
    QGridLayout,
    QLineEdit,
    QMenu
)

from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QBrush, QColor, QAction

from db.db import POSTGRESQL
from db.db import log_db_exceptions
from ui.alert_box import AlertBox
from ui.list_popup import List_popup
from ui.responsive_table import ResponsiveTableView

class RelativesTabelModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent = None):
        return len(self._data)
    
    def columnCount(self, parent = None):
        return len(self._headers)
    
    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        row = self._data[index.row()]
        val = row[index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            # ตรวจสอบ fingerprint
            if index.column() == 6:
                return 'ลงทะเบียนแล้ว' if val else 'ไม่ลงทะเบียน'
            return '' if val is None else str(val)
        
        if role == Qt.ItemDataRole.ForegroundRole:
            # ถ้า is_active อยู่ index 7 ให้แสดงเป็นสีเทาถ้าไม่ active
            is_active = row[7] if len(row) > 7 else True
            fp = row[6] if len(row) > 6 else True
            if not is_active:
                return QBrush(QColor("#b0b0b0"))
            if not fp:
                return QBrush(QColor("#140F55"))

        return None
    def headerData(self, section, orientation, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            else:
                return section + 1
        return None

class Relative_list(QWidget):
    def __init__(self):
        super().__init__()
        self.db = POSTGRESQL()

        self.setObjectName('main_relative_list_widget')
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 12, 20, 12)

        # หัวข้อ
        title_label = QLabel("รายชื่อญาติ")
        title_label.setObjectName('relative_list_title_label')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # layout
        vbox = QVBoxLayout()
        vbox.addItem(QSpacerItem(0, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        vbox.addWidget(title_label)

        main_layout.addLayout(vbox)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.proportions = [

        ]

        self.table_view = None

        self.filer_options = [

        ]
        self.create_filter_ui(main_layout)

        self.load_relatives()

    def create_filter_ui(self, layout):
        filter_layout = QGridLayout()

        title_list = ["ชาย","หญิง","อื่น ๆ" ]

        title_group = QGroupBox('คำนำหน้าตามเพศ')
        self.title_checkbox = []
        title_layout = QGridLayout()
        title_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for i, title in enumerate(title_list):
            cb = QCheckBox(title)
            cb.stateChanged.connect(self.apply_filters)
            self.title_checkbox.append(cb)
            title_layout.addWidget(cb, i, 0)
        title_group.setLayout(title_layout)
        filter_layout.addWidget(title_group, 0, 0)

        fp_group = QGroupBox('ลายนิ้วมือ')
        fp_list = ['ลงทะเบียนแล้ว', 'ไม่ลงทะเบียน']
        self.fp_checkbox = []
        fp_layout = QGridLayout()
        fp_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for i, fp in enumerate(fp_list):
            cb = QCheckBox(fp)
            cb.stateChanged.connect(self.apply_filters)
            self.fp_checkbox.append(cb)
            fp_layout.addWidget(cb, i, 0)
        fp_group.setLayout(fp_layout)
        filter_layout.addWidget(fp_group, 0, 1)

        search_group = QGroupBox("ค้นหาและแสดงผล")
        self.search_text = QLineEdit()
        self.search_text.setPlaceholderText('ค้นหาด้วย หมายเลขประจำตัว ชื่อหรือสกุล...')
        self.search_text.textChanged.connect(self.apply_filters)
        search_layout = QGridLayout()
        search_layout.addWidget(self.search_text, 0, 0)
        
        self.label_total = QLabel()
        self.label_total.setText("จำนวนทั้งหมด : 0 ราย")
        search_layout.addWidget(self.label_total, 1, 0)

        search_group.setLayout(search_layout)
        filter_layout.addWidget(search_group, 0, 2)

        layout.addLayout(filter_layout)

    def apply_filters(self):
        # ดึงค่าจาก search text และ checkbox
        title_male = ["เด็กชาย", "ด.ช.", "นาย"]
        title_female = ["เด็กหญิง", "ด.ญ.", "น.ส.", "นาง", "นางสาว"]

        search_text = self.search_text.text().strip().lower()
        titles = [cb.text() for cb in self.title_checkbox if cb.isChecked()]
        select_fp = [cb.text() for cb in self.fp_checkbox if cb.isChecked()]
        filtered = []
        for row in self.all_relatives:
            title = str(row[1]).strip() if row[1] is not None else ''

            if search_text and (search_text not in str(row[0]).lower() and search_text not in row[2].lower() and search_text not in row[3].lower()):
                continue
            
            if titles:
                match_title = False
                if 'ชาย' in titles and title in title_male:
                    match_title = True
                
                if 'หญิง' in titles and title in title_female:
                    match_title = True
                
                if "อื่น ๆ" in titles and title not in title_male and title not in title_female:
                    match_title = True

                if not match_title:
                    continue

            if select_fp:
                fp_text = "ลงทะเบียนแล้ว" if row[6] else "ไม่ลงทะเบียน"
                if fp_text not in select_fp:
                    continue


            filtered.append(row)

        self.table_model.beginResetModel()
        self.table_model._data = filtered
        self.table_model.endResetModel()

        self.label_total.setText(f'จำนวนทั้งหมด : {len(filtered)} ราย')


    def load_relatives(self):
        # ลบ view เก่าถ้ามี
        if getattr(self, 'table_view', None) is not None:
            try:
                self.layout().removeWidget(self.table_vies)
                self.table_vies.deleteLater()
            except Exception:
                pass

        relatives = self.db.get_all_relatives_list()
        if not relatives:
            AlertBox.error(self, 'load relative', 'ดึงข้อมูลไม่สำเร็จ')
            return
        
        self.all_relatives = relatives
        headers = ['รหัส', 'คำนำหน้า', 'ชื่อ', 'สกุล', 'ที่อยู่', 'เบอร์โทร', 'ลายนิ้วมือ', 'สถานะ']
        proportions = [0.08, 0.08, 0.12, 0.12, 0.30, 0.12, 0.10, 0.08]

        self.table_model = RelativesTabelModel(relatives, headers)
        self.table_view = ResponsiveTableView(proportions=proportions)
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

        self.layout().addWidget(self.table_view)
        self.table_view.apply_column_widths()
        self.apply_filters()








