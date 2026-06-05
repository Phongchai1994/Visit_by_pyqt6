from PyQt6.QtWidgets import (
    QFrame, 
    QVBoxLayout, 
    QApplication, 
    QMainWindow, 
    QWidget, 
    QHBoxLayout, 
    QLabel, 
    QGraphicsDropShadowEffect,
    QMenu,
)
from PyQt6.QtGui import (
    QColor, 
    QIcon, 
    QAction
)
from ui.menu_frame import MENU_FRAME
from ui.dashboard.dashboard_widget import Dashboard_Widget
from ui.prisoner.register_prisoner import Prisoner_register_widget
from ui.prisoner.prisoners_list import Prisoners_list
from ui.relative.relative_list import Relative_list
from ui.relative.regis_fingerprint import Register_Fingerprint
from utils.resource import Resource_Helper

import sys

class MAINWINDOW(QMainWindow):
    def __init__(self,user_role):
        super().__init__()
        self.user_role = user_role
        self.setWindowTitle('MAIN WINDOW')
        self.setGeometry(200, 200, 720, 480)
        self.setWindowIcon(QIcon(Resource_Helper.resource_path('ico.ico')))
        
        self.init_menu()

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        # รับค่าการคลิกปุ่ม
        self.menu = MENU_FRAME(user_role=self.user_role)
        layout.addWidget(self.menu)
        self.menu.btn_summery.clicked.connect(self.show_dashboard)
        self.menu.btn_prisoner_register.clicked.connect(self.show_prisoner_register)
        self.menu.btn_prisoners_list.clicked.connect(self.show_prisoners_list)
        self.menu.btn_relatives_list.clicked.connect(self.show_relatives_list)
        self.menu.btn_register_fingerprint.clicked.connect(self.show_register_fp)
        
        # สร้าง QFrame สำหรับ main content
        self.main_content = QFrame()
        self.main_content.setObjectName("mainContentFrame")
        main_layout = QVBoxLayout(self.main_content)
        main_layout.setContentsMargins(0, 0, 0, 0)  # ชิดขอบใน QFrame
        # main_label = QLabel('main content')
        # main_label.setObjectName("mainContentLabel")
        # main_layout.addWidget(main_label)
        layout.addWidget(self.main_content)

        self.setCentralWidget(central)

        # ใส่เงาให้ main_content
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(60, 60, 60, 40))  # สีเทาอ่อนโปร่งใส
        self.main_content.setGraphicsEffect(shadow)

        self.showMaximized()

    def show_dashboard(self):
        # ลบ widget เดิมใน main_content
        for i in reversed(range(self.main_content.layout().count())):
            widget = self.main_content.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_content.layout().addWidget(Dashboard_Widget())

    def show_prisoner_register(self):
        for i in reversed(range(self.main_content.layout().count())):
            widget = self.main_content.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_content.layout().addWidget(Prisoner_register_widget())

    def show_prisoners_list(self):
        for i in reversed(range(self.main_content.layout().count())):
            widget = self.main_content.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_content.layout().addWidget(Prisoners_list())

    def show_relatives_list(self):
        for i in reversed(range(self.main_content.layout().count())):
            widget = self.main_content.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_content.layout().addWidget(Relative_list())

    def show_register_fp(self):
        for i in reversed(range(self.main_content.layout().count())):
            widget = self.main_content.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_content.layout().addWidget(Register_Fingerprint(user_role = self.user_role))

    def init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('ไฟล์')
        exit_action = QAction('ออก', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        self.setStyleSheet("""
            QMenuBar, QMenu {
                font-size: 11px;
                padding: 2px 8px;
            }
        """)