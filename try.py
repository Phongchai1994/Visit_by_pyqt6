# from db.db import POSTGRESQL

# class Database():
#     def __init__(self):
#         self.db = POSTGRESQL()

#     def get_counts(self, date_visit, time_visit):
#         used = self.db.get_channel_counts(date_visit=date_visit, time_visit=time_visit)
#         return used
    
#     def get_slot(self, date_visit, time_visit):
#         result = self.db.get_avialable_slot(date_visit, time_visit)
#         return result
    
#     def get_all_available(self, date_visit, all_rounds):
#         result = self.db.get_all_available_slots_by_date(date_visit, all_rounds)
#         return result
    
# booking_round = [
#     ("รอบที่ 1 เวลา 09.30 - 09.45", "09:30:00", "09:15:00"),
#     ("รอบที่ 2 เวลา 10.00 - 10.15", "10:00:00", "09:45:00"),
#     ("รอบที่ 3 เวลา 10.30 - 10.45", "10:30:00", "10:15:00"),
#     ("รอบที่ 4 เวลา 11.00 - 11.15", "11:00:00", "10:15:00"),
#     ("รอบที่ 5 เวลา 13.15 - 13.30", "13:15:00", "13:00:00"),
#     ("รอบที่ 6 เวลา 13.45 - 14.00", "13:45:00", "13:15:00"),
#     ("รอบที่ 7 เวลา 14.15 - 14.30", "14:15:00", "13:15:00"),
#     ("รอบพิเศษ เวลา 12.00 - 13.00", "12:00:00", "12:45:00")
# ]
# # date_visit = '2026-05-08'
# # time_visit = '13:15:00'
# # db = Database()
# # # count = db.get_counts(date_visit=date_visit, time_visit=time_visit)
# # # print(count)
# # # used_channels = sorted(count.keys()) # รายการช่องที่ถูกใช้
# # # print(used_channels)
# # slot = db.get_all_available(date_visit, booking_round)
# # print(slot)

# booking_relative = {
#     1560100345135:{
#         'relative_id': 1560100345135, 
#         'title': 'นาย', 
#         'f_name': 'พงษ์ชัย', 
#         'l_name': 'เผ่ากันทะ', 
#         'is_booker': True}, 
#     3220100069242:{
#         'relative_id': 3220100069242, 
#         'title': 'นางสาว', 
#         'f_name': 'อัญชลี', 
#         'l_name': 'จงดี', 
#         'is_booker': False},
#     3220500011802:{
#         'relative_id': 3220500011802, 
#         'title': 'นางสาว', 
#         'f_name': 'เสาวภา', 
#         'l_name': 'ตระการสาธิต', 
#         'is_booker': False}}

# for id, val in booking_relative.items():
#     title = val['title']
#     f_name = val['f_name']
#     l_name = val['l_name']
#     print(f'{title}{f_name} {l_name}')

import os
from utils import config_env

connection_params = {
        "host": os.getenv("PG_HOST"),
        "port": os.getenv("PG_PORT"),
        "dbname": os.getenv("PG_NAME"),
        "user": os.getenv("PG_USER"),
        "password": os.getenv("PG_PASS")
    }

print(f"Database User: {connection_params}")