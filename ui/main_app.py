from PyQt6.QtWidgets import (
    QFrame, 
    QVBoxLayout, 
    QMainWindow, 
    QWidget, 
    QHBoxLayout, 
    QGraphicsDropShadowEffect,
    QScrollArea
)
from PyQt6.QtGui import (
    QColor, 
    QIcon, 
    QAction
)
from PyQt6.QtCore import Qt
from ui.menu_frame import MENU_FRAME
from ui.dashboard.dashboard_widget import Dashboard_Widget
from ui.prisoner.register_prisoner import Prisoner_register_widget
from ui.prisoner.prisoners_list import Prisoners_list
from ui.relative.relative_list import Relative_list
from ui.relative.regis_fingerprint import Register_Fingerprint
from ui.book_visit.booking_by_id import Book_By_National_ID
from ui.book_visit.booking_by_fp import Book_By_Fingerprint
from ui.report.daily_report import Dialy_Report
from ui.report.monthly_report import Monthly_Report
from ui.report.spacial_report import Spacial_Report

from utils.resource import Resource_Helper

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
        self.menu.btn_book_by_id_card.clicked.connect(self.show_book_by_id)
        self.menu.btn_book_by_fp.clicked.connect(self.show_book_by_fp)
        self.menu.btn_daily_report.clicked.connect(self.show_dialy_report)
        self.menu.btn_monthly_report.clicked.connect(self.show_monthly_report)
        self.menu.btn_special_report.clicked.connect(self.show_special_report)
        
        # สร้าง QFrame สำหรับ main content
        self.main_content = QFrame()
        self.main_content.setObjectName("mainContentFrame")
        main_layout = QVBoxLayout(self.main_content)
        main_layout.setContentsMargins(0, 0, 0, 0)  # ชิดขอบใน QFrame

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.main_content)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        layout.addWidget(self.scroll_area)

        self.setCentralWidget(central)

        # ใส่เงาให้ main_content
        # shadow = QGraphicsDropShadowEffect(self)
        # shadow.setBlurRadius(16)
        # shadow.setOffset(0, 2)
        # shadow.setColor(QColor(60, 60, 60, 40))  # สีเทาอ่อนโปร่งใส
        # self.main_content.setGraphicsEffect(shadow)

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

    def show_book_by_id(self):
        for i in reversed(range(self.main_content.layout().count())):
            widget = self.main_content.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_content.layout().addWidget(Book_By_National_ID())

    def show_book_by_fp(self):
        for i in reversed(range(self.main_content.layout().count())):
            widget = self.main_content.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_content.layout().addWidget(Book_By_Fingerprint())

    def show_dialy_report(self):
        
        for i in reversed(range(self.main_content.layout().count())):
            widget = self.main_content.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_content.layout().addWidget(Dialy_Report())

    def show_monthly_report(self):
        for i in reversed(range(self.main_content.layout().count())):
            widget = self.main_content.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_content.layout().addWidget(Monthly_Report())

    def show_special_report(self):
        for i in reversed(range(self.main_content.layout().count())):
            widget = self.main_content.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_content.layout().addWidget(Spacial_Report())

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