from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableView,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QHeaderView
)
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QBrush, QColor

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
        self.load_prisoners()

    def load_prisoners(self):
        prisoners = self.db.get_all_prisoners_list()
        if not prisoners:
            AlertBox.error(self, 'load prisoner', 'ดึงข้อมูลผู้ต้องขังไม่สำเร็จ')
            return

        headers = ['รหัสประจำตัว', 'เพศ', 'ชื่อ', 'สกุล', 'คดี', 'ชั้น', 'แดน', 'ประเภท', 'สถานะ', 'วินัย']

        self.table_model = PrisonersTableModel(prisoners, headers)
        self.table_view = ResponsiveTableView(self.proportions)
        self.table_view.setModel(self.table_model)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.verticalHeader().setVisible(False)

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        header.setStretchLastSection(False)

        self.layout().addWidget(self.table_view)

        self.table_view.apply_column_widths()