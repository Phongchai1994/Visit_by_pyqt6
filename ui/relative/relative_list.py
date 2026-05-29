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

        self.table_vies = None

        self.filer_options = [

        ]

        self.search_text = ''
        self.create_filter_ui(main_layout)

    def create_filter_ui(self, layout):
        filter_layout = QGridLayout()

        title_list = ["น.ส.","นาย","นาง","นางสาว","เด็กหญิง","เด็กชาย","ด.ญ.","ด.ช.","ว่าที่","พระ","จ.ส.ต." ]

        title_group = QGroupBox('คำนำหน้า')
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

        search_group = QGroupBox("ค้นหาและแสดงผล")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText('ค้นหาด้วย หมายเลขประจำตัว ชื่อหรือสกุล...')
        self.search_box.textChanged.connect(self.apply_filters)
        search_layout = QGridLayout()
        search_layout.addWidget(self.search_box, 0, 0)
        
        label_total = QLabel('จำนวน')
        search_layout.addWidget(label_total, 1, 0)

        search_group.setLayout(search_layout)
        filter_layout.addWidget(search_group, 0, 1)

        layout.addLayout(filter_layout)

    def apply_filters(self):
        print('apply_filters')
        print(self.title_checkbox)









