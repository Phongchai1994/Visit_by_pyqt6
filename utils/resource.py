import sys
import os

class Resource_Helper:
    @staticmethod
    def resource_path(relative_path):
        '''คืน path ที่ถูกต้องสำหรับ .py และ .exe'''
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    def get_env_path():
        """ดึง Path ที่ถูกต้องสำหรับไฟล์ .env ทั้งแบบ .py และ .exe"""
        if getattr(sys, 'frozen', False):
            # กรณีที่รันเป็น .exe (PyInstaller จะเซ็ต sys.frozen เป็น True)
            # sys.executable จะคืนค่าที่อยู่ของไฟล์ .exe ปัจจุบัน
            base_path = os.path.dirname(sys.executable)
        else:
            # กรณีที่รันเป็นสคริปต์ .py ปกติ
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        # วิ่งย้อนกลับไป 1 โฟลเดอร์ (..) แล้วหาไฟล์ .env
        return os.path.join(base_path, '..', '.env')