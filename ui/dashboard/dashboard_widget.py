from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class Dashboard_Widget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('แดชบอร์ดสรุปผลข้อมูล')
        layout.addWidget(label)
        self.setLayout(layout)