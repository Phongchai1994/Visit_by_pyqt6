import sys
import os

class Resource_Helper:
    @staticmethod
    def resource_path(relative_path):
        '''คืน path ที่ถูกต้องสำหรับ .py และ .exe'''
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)