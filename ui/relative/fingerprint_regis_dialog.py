from PyQt6.QtWidgets import(
    QDialog, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QTextEdit, QFrame
)
from PyQt6.QtCore import Qt
from db.db import POSTGRESQL
from ui.alert_box import AlertBox
from devices.regis_fp import Fingerprint_Worker

class Fingerprint_Register_Dialog(QDialog):
    def __init__(self, relative_data, relative_fp ,parent = None):
        super().__init__(parent)
        self.setObjectName('Fingerprint_Register_Dialog')
        self.db = POSTGRESQL()
        self.relative_data = relative_data
        self.relative_fp = relative_fp
        fp_name = self.relative_fp[0][0]
        # print(f'fingerprint = {self.relative_fp}',fp_name)
        self.template_bytes = None
        self.worker = None

        self.setModal(True)
        self.setMinimumWidth(520)
        self.setWindowTitle("ลงทะเบียนลายนิ้วมือ")

        layout = QVBoxLayout(self)

        header = QLabel("ลงทะเบียนลายนิ้วมือญาติ")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(line)

        form = QFormLayout()
        self.lbl_relative_id = QLabel(str(relative_data[0]))
        self.lbl_name = QLabel(f"{relative_data[1]}{relative_data[2]} {relative_data[3]}")
        self.lbl_fp_status = QLabel(f'ลงทะเบียนนิ้ว "{fp_name}"' if relative_data[6] else "ไม่ลงทะเบียน")

        self.finger_name = QComboBox()
        self.finger_name.addItems([
            "นิ้วโป้งซ้าย", "ชี้ซ้าย", "กลางซ้าย", "นางซ้าย", "ก้อยซ้าย",
            "นิ้วโป้งขวา", "ชี้ขวา", "กลางขวา", "นางขวา", "ก้อยขวา"
        ])
        self.finger_name.setCurrentText(fp_name)
        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)
        self.status_box.setFixedHeight(120)

        form.addRow("รหัสญาติ", self.lbl_relative_id)
        form.addRow("ชื่อ-สกุล", self.lbl_name)
        form.addRow("สถานะเดิม", self.lbl_fp_status)
        form.addRow("นิ้วที่ลงทะเบียน", self.finger_name)
        form.addRow("สถานะ", self.status_box)
        layout.addLayout(form)

        btn_row = QHBoxLayout()
        self.btn_start = QPushButton("เริ่มจับลายนิ้วมือ")
        self.btn_stop = QPushButton("หยุด")
        self.btn_save = QPushButton("บันทึก")
        self.btn_close = QPushButton("ปิด")

        self.btn_start.clicked.connect(self.start_capture)
        self.btn_stop.clicked.connect(self.stop_capture)
        self.btn_save.clicked.connect(self.save_fingerprint)
        self.btn_close.clicked.connect(self.reject)

        btn_row.addWidget(self.btn_start)
        btn_row.addWidget(self.btn_stop)
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_close)
        layout.addLayout(btn_row)

    def append_status(self, text):
            self.status_box.append(text)

    def start_capture(self):
        if self.worker and self.worker.isRunning():
            AlertBox.warning(self, "คำเตือน", "กำลังจับลายนิ้วมืออยู่")
            return

        self.worker = Fingerprint_Worker(
            relative_id=self.relative_data[0],
            db=self.db,
            parent=self
        )
        self.worker.status_changed.connect(self.append_status)
        self.worker.failed.connect(self.on_failed)
        self.worker.finished_ok.connect(self.on_finished_ok)
        self.worker.start()

    def stop_capture(self):
        if self.worker:
            self.worker.stop()
            self.worker = None
            self.append_status("หยุดการทำงานแล้ว")

    def on_failed(self, message):
        self.append_status(f"ผิดพลาด: {message}")
        AlertBox.error(self, "ลงทะเบียนลายนิ้วมือ", message)

    def on_finished_ok(self, template_bytes):
        self.template_bytes = template_bytes
        self.append_status("จับลายนิ้วมือสำเร็จ")

    def save_fingerprint(self):
        if not self.template_bytes:
            AlertBox.warning(self, "ลงทะเบียนลายนิ้วมือ", "ยังไม่มีข้อมูลลายนิ้วมือ")
            return

        relative_id = self.relative_data[0]
        finger_name = self.finger_name.currentText()

        ok = self.db.upsert_relative_fingerprint(
            relative_id=relative_id,
            finger_name=finger_name,
            fingerprint_bytes=self.template_bytes,
            is_active=True
        )
        if ok:
            AlertBox.info(self, "ลงทะเบียนลายนิ้วมือ", "บันทึกสำเร็จ")
            self.accept()
        else:
            AlertBox.error(self, "ลงทะเบียนลายนิ้วมือ", "บันทึกไม่สำเร็จ")