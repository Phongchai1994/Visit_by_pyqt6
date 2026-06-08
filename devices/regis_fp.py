
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal
)
from pyzkfp import ZKFP2
from PyQt6.QtCore import QThread, pyqtSignal

class Fingerprint_Worker(QThread):
    status_changed = pyqtSignal(str)
    failed = pyqtSignal(str)
    finished_ok = pyqtSignal(bytes)

    def __init__(self, relative_id, db, parent=None):
        super().__init__(parent)
        self.zkfp2 = ZKFP2()
        self.relative_id = relative_id
        self.db = db
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        try:
            self.status_changed.emit("กำลังเชื่อมต่อเครื่องสแกน...")
            self.zkfp2.Init()
            self.zkfp2.OpenDevice(0)

            self.status_changed.emit("เครื่องพร้อม กรุณาวางนิ้วมือ")
            template_list = []

            for i in range(3):
                if not self._running:
                    return

                while self._running:
                    capture = self.zkfp2.AcquireFingerprint()
                    if capture:
                        tmp, img = capture
                        template_list.append(tmp)
                        self.status_changed.emit(f"จับครั้งที่ {i + 1} สำเร็จ")
                        break

            if len(template_list) < 3:
                raise RuntimeError("จับลายนิ้วมือไม่ครบ 3 ครั้ง")

            reg_temp, reg_temp_len = self.zkfp2.DBMerge(*template_list)
            if not reg_temp:
                raise RuntimeError("รวม template ไม่สำเร็จ")

            self.finished_ok.emit(bytes(reg_temp))

        except Exception as e:
            import sys
            func_name = sys._getframe().f_code.co_name
            self.db.log_error(
                function_name=f"devices.regis_fp::{func_name}",
                error_message=str(e),
                extra_info=None
            )
            self.failed.emit(str(e))
        finally:
            try:
                self.zkfp2.CloseDevice()
            except Exception:
                pass
















