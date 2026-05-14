import sys

from user.login import LOGIN
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LOGIN()
    window.show()
    sys.exit(app.exec())
