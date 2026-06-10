from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFrame, QGroupBox, QPushButton,
    QRadioButton, QButtonGroup, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import datetime

from db.db import POSTGRESQL
from ui.alert_box import AlertBox


class Booking(QDialog):
    IDX_DATE = 0
    IDX_ROUND = 1
    IDX_FOLLOWERS = 2
    IDX_CHANNEL = 3

    def __init__(self, prisoner_data, relative_data, reserve_now=True, today=None, today_month=None, parent=None, on_success=None):
        super().__init__(parent)
        self.setWindowTitle("จองเยี่ยม")
        self.setModal(True)
        self.resize(520, 760)

        self.db = POSTGRESQL()
        self.prisoner_data = prisoner_data
        self.relative_data = relative_data
        self.reserve_now = reserve_now
        self.on_success = on_success

        self.id = self.prisoner_data[0]
        self.name = self.prisoner_data[1]
        self.surname = self.prisoner_data[2]
        self.level = self.prisoner_data[3]
        self.dan = self.prisoner_data[4]
        self.type = self.prisoner_data[7]

        self.relative_id = self.relative_data[0]
        self.relative_fullname = f"{self.relative_data[1]}{self.relative_data[2]} {self.relative_data[3]}"

        self.today = today or datetime.now().strftime("%Y-%m-%d")
        self.today_month = today_month or datetime.now().strftime("%Y-%m")

        self.data_reserve = ["", "", [], None]
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

        self._build_ui()
        self.start_flow()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("จองเยี่ยม")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(line)

        self.page_round = QGroupBox("เลือกรอบเยี่ยม")
        self.page_follower = QGroupBox("เลือกผู้ติดตาม")
        self.page_confirm = QGroupBox("ยืนยันข้อมูล")

        layout.addWidget(self.page_round)
        layout.addWidget(self.page_follower)
        layout.addWidget(self.page_confirm)

        self._build_round_page()
        self._build_follower_page()
        self._build_confirm_page()

        self.page_follower.hide()
        self.page_confirm.hide()

    def _build_round_page(self):
        layout = QVBoxLayout(self.page_round)
        self.round_group = QButtonGroup(self)
        self.round_group.setExclusive(True)

        self.round_hint = QLabel("")
        self.round_hint.setWordWrap(True)
        layout.addWidget(self.round_hint)

        for text, time_value, close_time in self._available_rounds_for_now():
            btn = QRadioButton(text)
            btn.setProperty("round_time", time_value)
            btn.setProperty("close_time", close_time)
            self.round_group.addButton(btn)
            layout.addWidget(btn)

        btn_next = QPushButton("ถัดไป")
        btn_next.clicked.connect(self.select_follower)
        layout.addWidget(btn_next)

    def _build_follower_page(self):
        layout = QVBoxLayout(self.page_follower)
        self.follower_hint = QLabel("")
        self.follower_hint.setWordWrap(True)
        layout.addWidget(self.follower_hint)

        self.follower_box = QGroupBox("รายชื่อผู้ติดตาม")
        follower_layout = QVBoxLayout(self.follower_box)
        self.follower_vars = []

        followers = self.db.get_join_prisoners_and_relatives_not_follower(self.id, self.relative_id)
        if followers:
            for row in followers:
                cb = QCheckBox(f"{row[1]}{row[2]} {row[3]}")
                cb.setProperty("relative_id", row[0])
                self.follower_vars.append((row[0], cb))
                follower_layout.addWidget(cb)
        else:
            follower_layout.addWidget(QLabel("ไม่พบผู้ติดตาม"))

        layout.addWidget(self.follower_box)

        btn_back = QPushButton("ย้อนกลับ")
        btn_back.clicked.connect(self.select_round)
        btn_next = QPushButton("ถัดไป")
        btn_next.clicked.connect(self.confirm_visit)

        layout.addWidget(btn_back)
        layout.addWidget(btn_next)

    def _build_confirm_page(self):
        layout = QVBoxLayout(self.page_confirm)
        self.confirm_hint = QLabel("")
        self.confirm_hint.setWordWrap(True)
        layout.addWidget(self.confirm_hint)

        self.confirm_detail = QLabel("")
        self.confirm_detail.setWordWrap(True)
        layout.addWidget(self.confirm_detail)

        btn_back = QPushButton("ย้อนกลับ")
        btn_back.clicked.connect(self.select_follower)

        btn_save = QPushButton("ยืนยันการจองเยี่ยม")
        btn_save.clicked.connect(self.save_to_db)

        btn_cancel = QPushButton("ยกเลิก")
        btn_cancel.clicked.connect(self.reject)

        layout.addWidget(btn_back)
        layout.addWidget(btn_save)
        layout.addWidget(btn_cancel)

    def start_flow(self):
        if not self.check_disciplinary():
            return
        if not self.check_visit():
            return
        self.select_round()

    def check_disciplinary(self):
        data = self.db.get_data_one(self.id)
        if data and data[9] == "ผิดวินัย":
            AlertBox.error(self, "จองเยี่ยม", "ผู้ต้องขังรายนี้ผิดวินัย ไม่สามารถจองเยี่ยมได้")
            return False
        return True

    def check_visit(self):
        check_visit = self.db.get_count_visit(self.id, self.today, self.today_month)
        self.count_reserve = check_visit[1] if check_visit else 0
        return True

    def _available_rounds_for_now(self):
        now = datetime.now().time()
        available = []
        for text, start, close in self.morning_rounds + self.afternoon_rounds:
            if now < datetime.strptime(close, "%H:%M:%S").time():
                available.append((text, start, close))
        return available

    def select_round(self):
        self.page_follower.hide()
        self.page_confirm.hide()
        self.page_round.show()
        self.round_hint.setText(
            f"ผู้ต้องขัง: {self.name} {self.surname}\n"
            f"ญาติผู้จอง: {self.relative_fullname}\n"
            f"วันที่เยี่ยม: {self.get_thai_date(self.today)}"
        )

    def select_follower(self):
        selected = self.round_group.checkedButton()
        if not selected:
            AlertBox.warning(self, "จองเยี่ยม", "กรุณาเลือกรอบเยี่ยม")
            return

        self.data_reserve[self.IDX_ROUND] = selected.property("round_time")
        self.data_reserve[self.IDX_DATE] = self.today

        self.page_round.hide()
        self.page_confirm.hide()
        self.page_follower.show()

        self.follower_hint.setText(
            f"รอบที่เลือก: {selected.text()}\n"
            f"วันที่: {self.get_thai_date(self.today)}"
        )

    def confirm_visit(self):
        selected_ids = [rid for rid, cb in self.follower_vars if cb.isChecked()]
        if len(selected_ids) > 4:
            AlertBox.warning(self, "จองเยี่ยม", "เลือกผู้ติดตามได้สูงสุด 4 คน")
            return

        self.data_reserve[self.IDX_FOLLOWERS] = selected_ids
        self.current_channel = self._find_first_available_channel()
        self.data_reserve[self.IDX_CHANNEL] = self.current_channel

        self.page_round.hide()
        self.page_follower.hide()
        self.page_confirm.show()

        self.confirm_hint.setText(
            f"ชื่อผู้ต้องขัง: {self.name} {self.surname}\n"
            f"วันที่: {self.get_thai_date(self.today)}\n"
            f"เวลา: {self.data_reserve[self.IDX_ROUND]}\n"
            f"ช่องเยี่ยม: {self.current_channel}\n"
            f"ญาติผู้จอง: {self.relative_fullname}"
        )
        self.confirm_detail.setText("ผู้ติดตาม:\n" + "\n".join(f"- {rid}" for rid in selected_ids) if selected_ids else "ผู้ติดตาม:\n-")

    def _find_first_available_channel(self, max_channel=14):
        used_channels = sorted(self.db.get_channel(self.today, self.data_reserve[self.IDX_ROUND]) or [])
        for channel in range(1, max_channel + 1):
            if channel not in used_channels:
                return channel
        return None

    def save_to_db(self):
        ok = self.insert_reserve_visit_to_db(
            [
                self.today,
                self.data_reserve[self.IDX_ROUND],
                self.id,
                self.relative_id,
                *self.data_reserve[self.IDX_FOLLOWERS]
            ],
            self.current_channel
        )
        if ok:
            AlertBox.info(self, "จองเยี่ยม", "จองเยี่ยมสำเร็จ")
            if self.on_success:
                self.on_success()
            self.accept()
        else:
            AlertBox.error(self, "จองเยี่ยม", "บันทึกไม่สำเร็จ")

    def insert_reserve_visit_to_db(self, prepare_data, channel):
        if channel is None:
            return False
        try:
            return self.db.insert_visit_by_national_id(
                visit_date=prepare_data[0],
                time_visit=prepare_data[1],
                prisoner_id=prepare_data[2],
                relative_id=prepare_data[3],
                follower_ids=prepare_data[4:],
                channel=channel
            )
        except Exception:
            return False

    def get_thai_date(self, date_str):
        thai_days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
        thai_months = [
            "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
            "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
        ]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"วัน{thai_days[dt.weekday()]} ที่ {dt.day} {thai_months[dt.month - 1]} {dt.year + 543}"