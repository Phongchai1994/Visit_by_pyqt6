import sys
import os
from user.login import LOGIN
from utils.resource import Resource_Helper
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import (
    QFontDatabase, 
    QFont, 
    QIcon,
    QGuiApplication
)
from PyQt6.QtCore import Qt

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    font_path = Resource_Helper.resource_path('etc/font/Sarabun/Sarabun-Regular.ttf')
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        print("Loaded font family:", font_family)
        app.setFont(QFont(font_family, 14))
    else:
        print('font load failed:', font_path)
    
    window = LOGIN()
    window.setWindowIcon(QIcon(Resource_Helper.resource_path('ico.ico')))
    window.show()
    sys.exit(app.exec())
