import sys
from user.login import LOGIN
from utils.resource import Resource_Helper
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import (
    QFontDatabase, 
    QFont, 
    QIcon,
    QPalette,
    QColor
)
from PyQt6.QtCore import Qt, QCoreApplication

if __name__ == '__main__':
    try: 
        app = QApplication(sys.argv)
        app.setStyle("Windows")
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        app.setPalette(palette)

        app.setStyleSheet("""
        QTableView {
            background-color: #ffffff;
            alternate-background-color: #e3f2fd; /* สีฟ้าอ่อน */
        }
        QTableView::indicator:checked {
            background-color: #1976d2; /* สี checkbox ที่ติ๊ก */
            border: 1px solid #1976d2;
        }
        QTableView::indicator:unchecked {
            background-color: #ffffff;
            border: 1px solid #1976d2;
        }
        """)
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
    except Exception as e:
        import traceback
        print("Exception:", e)
        print(traceback.format_exc())
        input("Press Enter to exit...")