from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableView, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QAbstractTableModel
from db.db import POSTGRESQL
from ui.alert_box import AlertBox

class PrisonerTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None

class Prisoners_list(QWidget):
    def __init__(self):
        super().__init__()
        self.db = POSTGRESQL()
        self.setObjectName('main_prisoner_list_widget')

        main_layout = QVBoxLayout(self)
        h_layout = QHBoxLayout()

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

        # ตาราง
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(title_label)
        vbox.addWidget(self.table)
        vbox.addItem(QSpacerItem(0, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        h_layout.addStretch(1)
        h_layout.addLayout(vbox)
        h_layout.addStretch(1)

        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 12, 20, 12)
        main_layout.addLayout(h_layout)

        self.setLayout(main_layout)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet('''
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
            }
            QTableView {
                background: #f5f6fa;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                color: #222;
                font-size: 14px;
            }
            QHeaderView::section {
                background: #e0e0e0;
                color: #222;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 6px;
            }
        ''')

        self.load_prisoners()

    def load_prisoners(self):
        prisoners = self.db.get_all_prisoners_list()
        if not prisoners:
            AlertBox.error(self, 'load prisoner', 'ดึงข้อมูลผู้ต้องขังไม่สำเร็จ')
            return

        headers = ['รหัสประจำตัว', 'เพศ', 'ชื่อ', 'สกุล', 'คดี', 'ชั้น', 'แดน', 'ประเภท', 'สถานะ', 'วินัย']
        # แปลง prisoners เป็น list of list (ถ้าเป็น tuple)
        prisoners = [list(row) for row in prisoners]
        # ถ้าข้อมูลแต่ละแถวมีไม่ครบ 10 ช่อง ให้เติม "" ให้ครบ
        for row in prisoners:
            while len(row) < len(headers):
                row.append("")
                print(row)
        model = PrisonerTableModel(prisoners, headers)
        self.table.setModel(model)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()