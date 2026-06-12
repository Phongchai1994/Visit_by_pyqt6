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
        
        self.relative_fullname = f"{self.relative_data[1]}{self.relative_data[2]} {self.relative_data[3]}"

        self.related_to_prisoners = self.db.get_prisoners_from_relative_id(self.relative_id)
        # print(self.related_to_prisoners)
        try:
            self.allowed_dan_by_dan = self._load_allowed_dan()
        except Exception as e:
            self.allowed_dan_by_dan = None
            AlertBox.error(self,title='แจ้งเตือนการโหลด josn',message=f'ตรวจสอบไฟล์ booking_allowed.json\n{e}')
        # print(self.allowed_dan_by_dan)

        # ตัวแปรเก็บข้อมูลไปบันทึกใน db
        self.booking_date_visit = None
        self.booking_time_visit = None
        self.booking_prisoner = {}
        self.booking_relative = {}
        self.booking_channel = None

        self.thai_day = None
        self.data_booking = []
        self.follower_vars = []
        self.count_reserve = 0
        self.current_channel = None
        self.morning_rounds = [
            ("รอบที่ 1 เวลา 09.30 - 09.45", "09:30:00", "09:15:00"),
            ("รอบที่ 2 เวลา 10.00 - 10.15", "10:00:00", "09:45:00"),
            ("รอบที่ 3 เวลา 10.30 - 10.45", "10:30:00", "10:15:00"),
            ("รอบที่ 4 เวลา 11.00 - 11.15", "11:00:00", "10:15:00"),
        ]
        self.afternoon_rounds = [
            ("รอบที่ 5 เวลา 13.15 - 13.30", "13:15:00", "13:00:00"),
            ("รอบที่ 6 เวลา 13.45 - 14.00", "13:45:00", "13:15:00"),
            ("รอบที่ 7 เวลา 14.15 - 14.30", "14:15:00", "13:15:00"),
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
            self.booking_date_visit = date.today().isoformat()
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

        if state_booking_today:
            self.mode_label.setText(f'จองเยี่ยมวันนี้\n({thai_date_full_str})')
        else:
            self.mode_label.setText(f'จองเยี่ยมล่วงหน้า\n({thai_date_full_str})')

        if self.booking_date_visit:
            dt = datetime.strptime(self.booking_date_visit, "%Y-%m-%d")
        else:
            dt = datetime.now()

        thai_days = ["จันทร์","อังคาร","พุธ","พฤหัสบดี","ศุกร์","เสาร์","อาทิตย์"]
        self.thai_day = thai_days[dt.weekday()]
        allower_dan = (self.allowed_dan_by_dan or {}).get(self.thai_day, [])
        # print(today)
        # print(f'today = {allower_dan}')

        for data in self.related_to_prisoners:
            # print(data)
            if data[5] in allower_dan and data[6] == 'อยู่':
                dis = '' if data[7] is None else str(data[7])
                p_type = 'กักขัง' if data[8] is 'ผู้ต้องกักขัง' else ''
                label = f'{str(data[2])} {str(data[3])[:3]}... ชั้น:{str(data[4])}\nแดน:{str(data[5])} ความสัมพันธ์:{str(data[9])} {dis} {p_type}'
                btn = QPushButton(label)
                if data[7] == 'ผิดวินัย':
                    btn.setDisabled(True)
                btn.clicked.connect(lambda checked=False, row=data: self.choose_a_round_and_followers(row))
                self.prisoner_layout.addWidget(btn)

        btn_go_back = QPushButton('กลับ')
        btn_close = QPushButton('ยกเลิก')
        self.button_layout.addWidget(btn_go_back)
        self.button_layout.addWidget(btn_close)

        btn_go_back.clicked.connect(self.choose_a_booking_page)
        btn_close.clicked.connect(self.close)

    def choose_a_round_and_followers(self, prisoner_data):
        '''
        เลือกรอบเยี่ยม และผู้ติดตาม'''
        # print(prisoner_data)
        prisoner_type = prisoner_data[8]
        allowed = self._allowed_round_numbers(prisoner_type)
        self.booking_prisoner = {
            'prisoner_id' : prisoner_data[0],
            'gender' : prisoner_data[1],
            'f_name' : prisoner_data[2],
            'l_name' : prisoner_data[3],
            'level' : prisoner_data[4],
            'dan' : prisoner_data[5],
            'status' : prisoner_data[6],
            'dis' : prisoner_data[7]
        }
        # print(f'self.booking_prisoner = {self.booking_prisoner}')

        self.clear_layout(self.button_layout)
        self.clear_layout(self.booking_layout)
        self.clear_layout(self.prisoner_layout)
        self.clear_layout(self.round_layout)
        self.clear_layout(self.followers_layout)
        self.clear_layout(self.recheck_layout)

        self.a_prisoners_group.hide()
        self.a_round_group.show()

        self.round_group = QButtonGroup(self)
        self.round_group.setExclusive(True)


        for round_text, time_start, time_close in self._filter_rounds(self.morning_rounds, allowed["morning"]):
            btn = QRadioButton(round_text)
            btn.setProperty('time_start', time_start)
            btn.setProperty('time_close', time_close)
            btn.clicked.connect(lambda checked=False, time_start=time_start: self.choose_a_follower(time_start))
            self.round_group.addButton(btn)
            self.round_layout.addWidget(btn)

        for round_text, time_start, time_close in self._filter_rounds(self.afternoon_rounds, allowed["afternoon"]):
            btn = QRadioButton(round_text)
            btn.setProperty('time_start', time_start)
            btn.setProperty('time_close', time_close)
            btn.clicked.connect(lambda checked=False, time_start=time_start: self.choose_a_follower(time_start))
            self.round_group.addButton(btn)
            self.round_layout.addWidget(btn)

        btn_back = QPushButton('กลับ')
        btn_close = QPushButton('ยกเลิก')

        self.button_layout.addWidget(btn_back)
        self.button_layout.addWidget(btn_close)

        btn_back.clicked.connect(self.select_prisoner_booking)
        btn_close.clicked.connect(self.close)

    def _allowed_round_numbers(self, prisoner_type: str):
        if self.thai_day == "จันทร์":
            return {"morning": [1, 2, 3, 4], "afternoon": [5, 6, 7]}

        if self.thai_day == "อังคาร":
            return {"morning": [1, 2, 3, 4], "afternoon": [5, 6, 7]}

        if self.thai_day == "พุธ":
            if prisoner_type == "ผู้ต้องกักขัง":
                return {"morning": [4], "afternoon": [7]}
            return {"morning": [1], "afternoon": [2, 3, 4, 7]}

        if self.thai_day == "พฤหัสบดี":
            return {"morning": [1, 2, 3, 4], "afternoon": [5, 6, 7]}

        if self.thai_day == "ศุกร์":
            if prisoner_type == "ผู้ต้องกักขัง":
                return {"morning": [1], "afternoon": [7]}
            return {"morning": [1], "afternoon": [2, 3, 4, 7]}

        return {"morning": [1, 2, 3, 4], "afternoon": [5, 6, 7]}

    def _filter_rounds(self, round_list, allowed_numbers):
        result = []
        for idx, item in enumerate(round_list, start=1):
            if idx in allowed_numbers:
                result.append(item)
        return result

    def choose_a_follower(self, time_start):
        # follower = self.db.get_relatives_follower_from_p_id(prisoner_id=)
        self.clear_layout(self.button_layout)
        self.clear_layout(self.round_layout)
        self.a_round_group.hide()
        self.a_followers_group.show()
        print(time_start)
        pass

    def confirm_booking(self):
        pass

    def insert_booking_to_db(self):

        query = '''

                '''
        data = ''
        self.db.insert_booking_to_visits(query = query, data = data)

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