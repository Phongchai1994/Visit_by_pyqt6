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

class Monthly_Report(QWidget):
    def __init__(self):
        super().__init__()
        self.db = POSTGRESQL()

        self.setObjectName('Monthly_Report')

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 12, 20, 12)

        # หัวข้อ
        title_label = QLabel('รายงานประจำเดือน')
        title_label.setObjectName('Monthly_Report_title_label')
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

        main_layout.addLayout(vbox)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)