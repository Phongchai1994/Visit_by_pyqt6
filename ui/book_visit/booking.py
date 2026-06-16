from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFrame, QGroupBox, QPushButton,
    QRadioButton, QButtonGroup, QCheckBox, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt,QTimer
from datetime import datetime, timedelta, date

from db.db import POSTGRESQL
from ui.alert_box import AlertBox
from utils.resource import Resource_Helper

import time as t
import json, os


class Booking(QDialog):
    IDX_DATE = 0
    IDX_ROUND = 1
    IDX_FOLLOWERS = 2
    IDX_CHANNEL = 3

    def __init__(self,relative_data, parent = None):
        super().__init__(parent)
        self.setObjectName('Booking')
        self.setWindowTitle("จองเยี่ยม")
        self.setModal(True)
        self.resize(520, 760)

        self.db = POSTGRESQL()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.time_label = QLabel()
        self.update_time_label()

        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time_label)
        self.time_timer.start(1000)

        self.relative_data = relative_data
        self.relative_id = relative_data[0]
        # print(relative_data)
        
        self.relative_fullname = f"{self.relative_data[1]}{self.relative_data[2]} {self.relative_data[3]}"

        self.related_to_prisoners = self.db.get_prisoners_from_relative_id(self.relative_id)
        # print(self.related_to_prisoners)
        try:
            self.allowed_dan_by_dan = self._load_allowed_dan()
        except Exception as e:
            self.allowed_dan_by_dan = None
            AlertBox.error(self,title='แจ้งเตือนการโหลด josn',message=f'ตรวจสอบไฟล์ booking_allowed.json\n{e}')
        # print(self.allowed_dan_by_dan)

        # สถานะ การจองเยี่ยมวันนี้ วันนี้ True 
        self.state_booking_today = None

        # ตัวแปรเก็บข้อมูลไปบันทึกใน db
        self.booking_date_visit = None
        self.booking_prisoner = {}
        self.booking_time_visit = None
        self.booking_relative = {}
        self.booking_channel = None

        self.thai_day = None
        self.data_booking = []
        self.follower_vars = []
        self.count_reserve = 0
        self.current_channel = None
        self.boooking_round = [
            ("รอบที่ 1 เวลา 09.30 - 09.45", "09:30:00", "09:15:00"),
            ("รอบที่ 2 เวลา 10.00 - 10.15", "10:00:00", "09:45:00"),
            ("รอบที่ 3 เวลา 10.30 - 10.45", "10:30:00", "10:15:00"),
            ("รอบที่ 4 เวลา 11.00 - 11.15", "11:00:00", "10:15:00"),
            ("รอบที่ 5 เวลา 13.15 - 13.30", "13:15:00", "13:00:00"),
            ("รอบที่ 6 เวลา 13.45 - 14.00", "13:45:00", "13:15:00"),
            ("รอบที่ 7 เวลา 14.15 - 14.30", "14:15:00", "13:15:00"),
            ("รอบพิเศษ เวลา 12.00 - 13.00", "12:00:00", "12:45:00")
        ]

        self.mode_label = QLabel()
        vbox_mode = QVBoxLayout()
        vbox_mode.addWidget(self.mode_label, stretch=0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.a_mode_bookint_group = QGroupBox('โหมดการจองเยี่ยม')
        self.a_mode_bookint_group.setLayout(vbox_mode)
        self.a_choose_booking_group = QGroupBox('เลือกการจองเยี่ยม')
        self.a_prisoners_group = QGroupBox('เลือกผู้ต้องขัง')
        self.a_round_group = QGroupBox('เลือกรอบเยี่ยม')
        self.a_followers_group = QGroupBox('เลือกผู้ติดตาม')
        self.a_recheck_group = QGroupBox('ตรวจสอบข้อมูล')
        self.a_button_group = QGroupBox('ปุ่มดำเนินการ')

        self.booking_layout = QVBoxLayout(self.a_choose_booking_group)
        self.button_layout = QVBoxLayout(self.a_button_group)
        self.prisoner_layout = QVBoxLayout(self.a_prisoners_group)
        self.round_layout = QVBoxLayout(self.a_round_group)
        self.followers_layout = QVBoxLayout(self.a_followers_group)
        self.recheck_layout = QVBoxLayout(self.a_recheck_group)

        self.a_choose_booking_group.hide()
        self.a_prisoners_group.hide()
        self.a_round_group.hide()
        self.a_followers_group.hide()
        self.a_recheck_group.hide()
        self.a_mode_bookint_group.hide()

        self.main_layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.a_mode_bookint_group)
        self.main_layout.addWidget(self.a_choose_booking_group)
        self.main_layout.addWidget(self.a_prisoners_group)
        self.main_layout.addWidget(self.a_round_group)
        self.main_layout.addWidget(self.a_followers_group)
        self.main_layout.addWidget(self.a_recheck_group)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.a_button_group, stretch=0, alignment=Qt.AlignmentFlag.AlignBottom)
        self.choose_a_booking_page()
        
        # self._build_ui()
        # self.start_flow()

    def choose_a_booking_page(self):
        '''
        หน้าเลือการจองเยี่ยม'''
        # self._test_print_data(self.choose_a_booking_page.__name__)
        self.clear_layout(self.button_layout)
        self.clear_layout(self.booking_layout)
        self.clear_layout(self.prisoner_layout)
        self.clear_layout(self.round_layout)
        self.clear_layout(self.followers_layout)
        self.clear_layout(self.recheck_layout)

        self.a_mode_bookint_group.hide()
        self.a_prisoners_group.hide()
        self.a_choose_booking_group.show()

        btn_book_today = QPushButton('จองเยี่ยมวันนี้')
        btn_book_advance = QPushButton('จองเยี่ยมล่วงหน้า')
        btn_close_window = QPushButton('ยกเลิก')

        self.booking_layout.addWidget(btn_book_today)
        self.booking_layout.addWidget(btn_book_advance)
        self.button_layout.addWidget(btn_close_window)

        btn_book_today.clicked.connect(lambda: self.prepare_booking_date(True))
        btn_book_advance.clicked.connect(lambda: self.prepare_booking_date(False))
        btn_close_window.clicked.connect(self.close)

    def prepare_booking_date(self, today:bool):
        if today:
            # self.booking_date_visit = date.today().isoformat()
            self.booking_date_visit = "2026-06-15"
        else:
            self.booking_date_visit = self._next_non_holiday_date(date.today() + timedelta(days=1))

        self.select_prisoner_booking(today)

    def _next_non_holiday_date(self, current_date:date):
        while current_date.weekday() in (5, 6) or self.db.get_is_holiday(current_date.isoformat()):
            current_date += timedelta(days=1)
        return current_date.isoformat()

    def select_prisoner_booking(self, state_booking_today=bool):
        '''
        หน้าเลือกผู้ต้องขัง'''
        # self._test_print_data(self.select_prisoner_booking.__name__)
        self.state_booking_today = state_booking_today
        thai_date_full_str = self.get_thai_date(self.booking_date_visit)

        self.clear_layout(self.button_layout)
        self.clear_layout(self.booking_layout)
        self.clear_layout(self.prisoner_layout)
        self.clear_layout(self.round_layout)
        self.clear_layout(self.followers_layout)
        self.clear_layout(self.recheck_layout)

        self.a_choose_booking_group.hide()
        self.a_round_group.hide()
        self.a_prisoners_group.show()
        self.a_mode_bookint_group.show()

        if self.state_booking_today:
            self.mode_label.setText(f'จองเยี่ยมวันนี้\n({thai_date_full_str})')
        else:
            self.mode_label.setText(f'จองเยี่ยมล่วงหน้า\n({thai_date_full_str})')

        if self.booking_date_visit:
            dt = datetime.strptime(self.booking_date_visit, "%Y-%m-%d")
        else:
            dt = datetime.now()

        thai_days = ["จันทร์","อังคาร","พุธ","พฤหัสบดี","ศุกร์","เสาร์","อาทิตย์"]
        self.thai_day = thai_days[dt.weekday()]
        if self.allowed_dan_by_dan is None:
            AlertBox.error(self, title='ไฟล์ booking_allowed.json', message='ไม่สามารถโหลดไฟล์ booking_allowed.json ได้')
            return
        allower_dan = (self.allowed_dan_by_dan or {}).get(self.thai_day, [])
        # print(today)
        # print(f'today = {allower_dan}')

        for data in self.related_to_prisoners:
            # print(data)
            if data[5] in allower_dan and data[6] == 'อยู่':
                dis = '' if data[7] is None else str(data[7])
                p_type = 'กักขัง' if data[8] == 'ผู้ต้องกักขัง' else ''
                label = f'{str(data[2])} {str(data[3])[:3]}... ชั้น:{str(data[4])}\nแดน:{str(data[5])} ความสัมพันธ์:{str(data[9])} {dis} {p_type}'
                btn = QPushButton(label)
                if data[7] == 'ผิดวินัย':
                    btn.setDisabled(True)
                btn.clicked.connect(lambda checked=False, row=data: on_next(row))
                self.prisoner_layout.addWidget(btn)

        def on_next(prisoner_data):
            normalized ={
                'prisoner_id': None,
                'gender': None,
                'f_name': None,
                'l_name': None,
                'level': None,
                'dan': None,
                'status': None,
                'dis': None,
                'type': None 
            }
            if isinstance(prisoner_data, dict):
                for k in normalized.keys():
                    # print(k)
                    if k in prisoner_data:
                        normalized[k] = prisoner_data[k]
            elif isinstance(prisoner_data, (list, tuple)):
                mapping = [
                    'prisoner_id',
                    'gender',
                    'f_name',
                    'l_name',
                    'level',
                    'dan',
                    'status',
                    'dis',
                    'type'
                ]
                for i, key in enumerate(mapping):
                    if i < len(prisoner_data):
                        normalized[key] = prisoner_data[i]
            else:
                AlertBox.error(self, title='ข้อมูลผู้ต้องขัง', message='รูปแบบข้อมูลผู้ต้องขังไม่ถูกต้อง')
                return
            # print(normalized)
            if not normalized.get('prisoner_id'):
                AlertBox.error(self, title='ข้อมูลผู้ต้องขัง', message='ID ผู้ต้องขังไม่ถูกต้อง')
                return

            self.booking_prisoner = normalized
            self.choose_a_round()

        btn_go_back = QPushButton('กลับ')
        btn_close = QPushButton('ยกเลิก')
        self.button_layout.addWidget(btn_go_back)
        self.button_layout.addWidget(btn_close)

        btn_go_back.clicked.connect(self.choose_a_booking_page)
        btn_close.clicked.connect(self.close)

    def choose_a_round(self):
        '''
         เลือกรอบเยี่ยม'''
        # Normalize incoming data to dict with safe defaults
        
        prisoner_dan = self.booking_prisoner['dan']
        prisoner_type = self.booking_prisoner['type']

        allowed = self._allowed_round_numbers(prisoner_dan, prisoner_type)
        if allowed is None:
            AlertBox.error(self, title='ตรวจสอบแดน', message=f'ไม่พบแดน :{prisoner_dan}')
            return

        self.clear_layout(self.button_layout)
        self.clear_layout(self.booking_layout)
        self.clear_layout(self.prisoner_layout)
        self.clear_layout(self.round_layout)
        self.clear_layout(self.followers_layout)
        self.clear_layout(self.recheck_layout)

        self.a_prisoners_group.hide()
        self.a_round_group.show()
        self.a_followers_group.hide()

        self.round_group = QButtonGroup(self)
        self.round_group.setExclusive(True)
        now_time = datetime.now().time()

        for round_text, time_start, time_close in self._filter_rounds(self.boooking_round, allowed):
            close_time = datetime.strptime(time_close, "%H:%M:%S").time()
            btn = QPushButton(round_text)
            btn.setCheckable(True)
            btn.setProperty('time_start', time_start)
            btn.clicked.connect(lambda checked, ts=time_start: on_next(ts))
            if now_time > close_time and self.state_booking_today:
                # print('now_time > close_time')
                btn.setDisabled(True)
            self.round_group.addButton(btn)
            self.round_layout.addWidget(btn)

        def on_next(ts):
            self.booking_time_visit = ts
            self.choose_a_follower()


        btn_back = QPushButton('กลับ')
        btn_close = QPushButton('ยกเลิก')

        self.button_layout.addWidget(btn_back)
        self.button_layout.addWidget(btn_close)

        btn_back.clicked.connect(self.select_prisoner_booking)
        btn_close.clicked.connect(self.close)

    def _load_round_rules(self):
        path_booking_json = 'etc/config/booking_round.json'
        path = Resource_Helper.resource_path(path_booking_json)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
        
    def _allowed_round_numbers(self, prisoner_dan:str, prisoner_type:str):
        # โหลดข้อมูลทั้งหมด
        if not hasattr(self, "round_rules_config"):
            self.round_rules_config = self._load_round_rules()
            if self.round_rules_config is None:
                return None
            
        # ของ รจช
        if prisoner_dan == "รจช":
            dan_cfg = self.round_rules_config.get("default_rules", {}).get(
                "รจช"
            )
            if dan_cfg:
                return dan_cfg.get(prisoner_type)  # คืนค่าตามประเภท หรือ None
            return None

        # ดึงโครงสร้างของวันนั้น ๆ ออกมา
        day_cfg = self.round_rules_config.get(self.thai_day)
        if not day_cfg:
            return None
        
        # ดึงโครงสร้างแดน
        dan_cfg = day_cfg.get(prisoner_dan)
        if not dan_cfg:
            return None
        
        # ดังตามประเภทของผู้ต้องขัง
        return dan_cfg.get(prisoner_type)

    def _filter_rounds(self, round_list, allowed_numbers):
        # print(f'round_list = {round_list}')
        # print(f'allowed_numbers = {allowed_numbers}')
        result = []
        for idx, item in enumerate(round_list, start=1):

            if idx in allowed_numbers:
                result.append(item)
        return result

    def choose_a_follower(self):
        '''
        หน้าเลือกผู้ติดตาม'''
        follower = self.db.get_relatives_follower_from_p_id(
            prisoner_id=self.booking_prisoner['prisoner_id']
        )
        # self._test_print_data(self.choose_a_follower.__name__)

        self.clear_layout(self.followers_layout)
        self.clear_layout(self.button_layout)
        self.clear_layout(self.round_layout)
        self.a_round_group.hide()
        self.a_recheck_group.hide()
        self.a_followers_group.show()

        self.follower_checkboxes = []

        def count_selected():
            return sum(1 for cb in self.follower_checkboxes if cb.isChecked())
        
        def on_checkbox_toggled(checked, cb):
            if checked and count_selected() > 5:
                cb.blockSignals(True)
                cb.setChecked(False)
                cb.blockSignals(False)
                AlertBox.warning(self, title='จำกัดจำนวน' ,message='รวมตัวผู้จองแล้ว เลือกได้ไม่เกิน 5 ราย')

        for idx, val in enumerate(follower):
            if str(val) == str(self.relative_id):
                print(val, self.relative_id)
                continue
            display = f'{str(val[1])}{str(val[2])} {str(val[3])}\nความสัมพันธ์ : {str(val[4])}'
            cb = QCheckBox(display)
            cb.setProperty('follower', val)
            cb.toggled.connect(lambda checked, box = cb: on_checkbox_toggled(checked, box))
            self.followers_layout.addWidget(cb)
            self.follower_checkboxes.append(cb)

        btn_next = QPushButton('ถัดไป')
        btn_back = QPushButton('กลับ')
        btn_close = QPushButton('ยกเลิก')

        def on_next():
            selected = {}
            selected[self.relative_data[0]] = {
                'relative_id': self.relative_data[0],
                'title': self.relative_data[1],
                'f_name': self.relative_data[2],
                'l_name': self.relative_data[3],
                'is_booker': False,
            }
            for cb in self.follower_checkboxes:
                if cb.isChecked():
                    val = cb.property('follower')
                    selected[val[0]] = {
                        'relative_id': val[0],
                        'title': val[1],
                        'f_name': val[2],
                        'l_name': val[3],
                        'is_booker': False,
                    }
            if len(selected) > 5:
                AlertBox.warning(self, title='จำกัดจำนวน', message='รวมตัวผู้จองแล้ว เลือกได้ไม่เกิน 5 ราย')
                return
            self.booking_relative = selected
            self.confirm_booking()

        btn_next.clicked.connect(on_next)
        btn_back.clicked.connect(self.choose_a_round)
        btn_close.clicked.connect(self.close)

        self.button_layout.addWidget(btn_next)
        self.button_layout.addWidget(btn_back)
        self.button_layout.addWidget(btn_close)

    def confirm_booking(self):
        self.a_followers_group.hide()
        self.a_recheck_group.show()
        
        self.clear_layout(self.followers_layout)
        self.clear_layout(self.button_layout)

        btn_confirm = QPushButton('ยืนยันข้อมูล')
        btn_back = QPushButton('กลับ')
        btn_close = QPushButton('ยกเลิก')


        self.button_layout.addWidget(btn_confirm)
        self.button_layout.addWidget(btn_back)
        self.button_layout.addWidget(btn_close)

        btn_confirm.clicked.connect(self.insert_booking_to_db)
        btn_back.clicked.connect(self.choose_a_follower)
        btn_close.clicked.connect(self.close)

    def insert_booking_to_db(self):

        print(f'self.booking_date_visit : {self.booking_date_visit}')
        print('--------------------------------------------')
        print(f'self.booking_prisoner : {self.booking_prisoner}')
        print('--------------------------------------------')
        print(f'self.booking_time_visit : {self.booking_time_visit}')
        print('--------------------------------------------')
        print(f'self.booking_relative : {self.booking_relative}')
        print('--------------------------------------------')
        print(f'self.booking_channel : {self.booking_channel}')
        print('--------------------------------------------')
        # query = '''

        #         '''
        # data = ''
        # self.db.insert_booking_to_visits(query = query, data = data)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            child_layout = item.layout()
            if child_layout is not None:
                self.clear_layout(child_layout)

    def _load_allowed_dan(self):
        path = Resource_Helper.resource_path("etc/config/booking_allowed.json")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"โหลด config ล้มเหลว: {path}") from e



    # def _test_print_data(self, function_name):
    #     return
        # print('------------------------------------------')
        # print(f'ชื่อฟังก์ชัน :{function_name}')
        # print(f'วันที่จอง :{self.booking_date_visit}')
        # print(f'ชื่อผู้ต้องขัง :{self.booking_prisoner}')
        # print(f'เวลาจอง :{self.booking_time_visit}')
        # print(f'ชื่อญาติ :{self.booking_relative}')
        # print(f'ชื่อช่อง :{self.booking_channel}')
        # print('------------------------------------------')


    # def _build_ui(self):
    #     layout = QVBoxLayout(self)
    #     layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

    #     title = QLabel("จองเยี่ยม")
    #     layout.addWidget(title)

    #     line = QFrame()
    #     line.setFrameShape(QFrame.Shape.HLine)
    #     layout.addWidget(line)

    #     self.page_round = QGroupBox("เลือกรอบเยี่ยม")
    #     self.page_follower = QGroupBox("เลือกผู้ติดตาม")
    #     self.page_confirm = QGroupBox("ยืนยันข้อมูล")

    #     layout.addWidget(self.page_round)
    #     layout.addWidget(self.page_follower)
    #     layout.addWidget(self.page_confirm)

    #     self._build_round_page()
    #     self._build_follower_page()
    #     self._build_confirm_page()

    #     self.page_follower.hide()
    #     self.page_confirm.hide()

    # def _build_round_page(self):
    #     layout = QVBoxLayout(self.page_round)
    #     self.round_group = QButtonGroup(self)
    #     self.round_group.setExclusive(True)

    #     self.round_hint = QLabel("")
    #     self.round_hint.setWordWrap(True)
    #     layout.addWidget(self.round_hint)

    #     for text, time_value, close_time in self._available_rounds_for_now():
    #         btn = QRadioButton(text)
    #         btn.setProperty("round_time", time_value)
    #         btn.setProperty("close_time", close_time)
    #         self.round_group.addButton(btn)
    #         layout.addWidget(btn)

    #     btn_next = QPushButton("ถัดไป")
    #     btn_next.clicked.connect(self.select_follower)
    #     layout.addWidget(btn_next)

    # def _build_follower_page(self):
    #     layout = QVBoxLayout(self.page_follower)
    #     self.follower_hint = QLabel("")
    #     self.follower_hint.setWordWrap(True)
    #     layout.addWidget(self.follower_hint)

    #     self.follower_box = QGroupBox("รายชื่อผู้ติดตาม")
    #     follower_layout = QVBoxLayout(self.follower_box)
    #     self.follower_vars = []

    #     followers = self.db.get_join_prisoners_and_relatives_not_follower(self.prisoner_id, self.relative_id)
    #     if followers:
    #         for row in followers:
    #             cb = QCheckBox(f"{row[1]}{row[2]} {row[3]}")
    #             cb.setProperty("relative_id", row[0])
    #             self.follower_vars.append((row[0], cb))
    #             follower_layout.addWidget(cb)
    #     else:
    #         follower_layout.addWidget(QLabel("ไม่พบผู้ติดตาม"))

    #     layout.addWidget(self.follower_box)

    #     btn_back = QPushButton("ย้อนกลับ")
    #     btn_back.clicked.connect(self.select_round)
    #     btn_next = QPushButton("ถัดไป")
    #     btn_next.clicked.connect(self.confirm_visit)

    #     layout.addWidget(btn_back)
    #     layout.addWidget(btn_next)

    # def _build_confirm_page(self):
    #     layout = QVBoxLayout(self.page_confirm)
    #     self.confirm_hint = QLabel("")
    #     self.confirm_hint.setWordWrap(True)
    #     layout.addWidget(self.confirm_hint)

    #     self.confirm_detail = QLabel("")
    #     self.confirm_detail.setWordWrap(True)
    #     layout.addWidget(self.confirm_detail)

    #     btn_back = QPushButton("ย้อนกลับ")
    #     btn_back.clicked.connect(self.select_follower)

    #     btn_save = QPushButton("ยืนยันการจองเยี่ยม")
    #     btn_save.clicked.connect(self.save_to_db)

    #     btn_cancel = QPushButton("ยกเลิก")
    #     btn_cancel.clicked.connect(self.reject)

    #     layout.addWidget(btn_back)
    #     layout.addWidget(btn_save)
    #     layout.addWidget(btn_cancel)

    # def start_flow(self):
    #     if not self.check_disciplinary():
    #         return
    #     if not self.check_visit():
    #         return
    #     self.select_round()

    # def check_disciplinary(self):
    #     data_dis = self.db.get_data_check_disciplinary(self.prisoner_id)
    #     if data_dis and data_dis == "ผิดวินัย":
    #         AlertBox.error(self, "จองเยี่ยม", "ผู้ต้องขังรายนี้ผิดวินัย ไม่สามารถจองเยี่ยมได้")
    #         return False
    #     return True

    # def check_visit(self):
    #     check_visit = self.db.get_count_visit(self.prisoner_id, self.today, self.today_month)
    #     self.count_reserve = check_visit[1] if check_visit else 0
    #     return True

    # def _available_rounds_for_now(self):
    #     now = datetime.now().time()
    #     available = []
    #     for text, start, close in self.morning_rounds + self.afternoon_rounds:
    #         if now < datetime.strptime(close, "%H:%M:%S").time():
    #             available.append((text, start, close))
    #     return available

    # def select_round(self):
    #     self.page_follower.hide()
    #     self.page_confirm.hide()
    #     self.page_round.show()
    #     self.round_hint.setText(
    #         f"ผู้ต้องขัง: {self.prisoner_name} {self.prisoner_surname}\n"
    #         f"ญาติผู้จอง: {self.relative_fullname}\n"
    #         f"วันที่เยี่ยม: {self.get_thai_date(self.today)}"
    #     )

    # def select_follower(self):
    #     selected = self.round_group.checkedButton()
    #     if not selected:
    #         AlertBox.warning(self, "จองเยี่ยม", "กรุณาเลือกรอบเยี่ยม")
    #         return

    #     self.data_reserve[self.IDX_ROUND] = selected.property("round_time")
    #     self.data_reserve[self.IDX_DATE] = self.today

    #     self.page_round.hide()
    #     self.page_confirm.hide()
    #     self.page_follower.show()

    #     self.follower_hint.setText(
    #         f"รอบที่เลือก: {selected.text()}\n"
    #         f"วันที่: {self.get_thai_date(self.today)}"
    #     )

    # def confirm_visit(self):
    #     selected_ids = [rid for rid, cb in self.follower_vars if cb.isChecked()]
    #     if len(selected_ids) > 4:
    #         AlertBox.warning(self, "จองเยี่ยม", "เลือกผู้ติดตามได้สูงสุด 4 คน")
    #         return

    #     self.data_reserve[self.IDX_FOLLOWERS] = selected_ids
    #     self.current_channel = self._find_first_available_channel()
    #     self.data_reserve[self.IDX_CHANNEL] = self.current_channel

    #     self.page_round.hide()
    #     self.page_follower.hide()
    #     self.page_confirm.show()

    #     self.confirm_hint.setText(
    #         f"ชื่อผู้ต้องขัง: {self.prisoner_name} {self.prisoner_surname}\n"
    #         f"วันที่: {self.get_thai_date(self.today)}\n"
    #         f"เวลา: {self.data_reserve[self.IDX_ROUND]}\n"
    #         f"ช่องเยี่ยม: {self.current_channel}\n"
    #         f"ญาติผู้จอง: {self.relative_fullname}"
    #     )
    #     self.confirm_detail.setText("ผู้ติดตาม:\n" + "\n".join(f"- {rid}" for rid in selected_ids) if selected_ids else "ผู้ติดตาม:\n-")

    # def _find_first_available_channel(self, max_channel=14):
    #     used_channels = sorted(self.db.get_channel(self.today, self.data_reserve[self.IDX_ROUND]) or [])
    #     for channel in range(1, max_channel + 1):
    #         if channel not in used_channels:
    #             return channel
    #     return None

    # def save_to_db(self):
    #     ok = self.insert_reserve_visit_to_db(
    #         [
    #             self.today,
    #             self.data_reserve[self.IDX_ROUND],
    #             self.prisoner_id,
    #             self.relative_id,
    #             *self.data_reserve[self.IDX_FOLLOWERS]
    #         ],
    #         self.current_channel
    #     )
    #     if ok:
    #         AlertBox.info(self, "จองเยี่ยม", "จองเยี่ยมสำเร็จ")
    #         if self.on_success:
    #             self.on_success()
    #         self.accept()
    #     else:
    #         AlertBox.error(self, "จองเยี่ยม", "บันทึกไม่สำเร็จ")

    # def insert_reserve_visit_to_db(self, prepare_data, channel):
    #     print('self.insert_reserve_visit_to_db')
    #     # if channel is None:
    #     #     return False
    #     # try:
    #     #     return self.db.insert_visit_by_national_id(
    #     #         visit_date=prepare_data[0],
    #     #         time_visit=prepare_data[1],
    #     #         prisoner_id=prepare_data[2],
    #     #         relative_id=prepare_data[3],
    #     #         follower_ids=prepare_data[4:],
    #     #         channel=channel
    #     #     )
    #     # except Exception:
    #     #     return False

    def get_thai_date(self, date_str):
        thai_days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
        thai_months = [
            "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
            "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
        ]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"วัน{thai_days[dt.weekday()]} ที่ {dt.day} {thai_months[dt.month - 1]} {dt.year + 543}"
    
    def update_time_label(self):
        '''
        แสดงเวลาแบบ realtime'''

        days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
        months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
                "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
                "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
        
        current_time = t.localtime()
        day = days[current_time.tm_wday]
        month = months[current_time.tm_mon - 1]

        self.time_label.setText(
            f"วัน {day} ที่ {current_time.tm_mday} {month} "
            f"{current_time.tm_year + 543} เวลา {t.strftime('%H:%M:%S')}"
        )