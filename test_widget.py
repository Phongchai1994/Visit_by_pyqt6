from PyQt6.QtWidgets import QApplication, QMainWindow, QRadioButton, QVBoxLayout
import sys
from datetime import datetime, date, timedelta

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('ทดสอบ Widget')

        btn = QRadioButton('ทดสอบ')
        btn.setProperty('time_start', True)
        btn.setDisabled(True)

        self.setCentralWidget(btn)

        time_now = datetime.now().time()
        time_str = "13:00:00"
        time_srt_conv = datetime.strptime(time_str, "%H:%M:%S").time()

        print(time_now)
        print(time_srt_conv)
        print(time_now > time_srt_conv)

app = QApplication(sys.argv)

window = Main_Window()
window.show()

app.exec()