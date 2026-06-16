from db.db import POSTGRESQL

class Database():
    def __init__(self):
        self.db = POSTGRESQL()

    def get_counts(self, date_visit, time_visit):
        used = self.db.get_channel_counts(date_visit=date_visit, time_visit=time_visit)
        return used
    

date_visit = '2026-05-08'
time_visit = '13:45:00'
db = Database()
count = db.get_counts(date_visit=date_visit, time_visit=time_visit)
print(count)
used_channels = sorted(count.keys()) # รายการช่องที่ถูกใช้
print(used_channels)