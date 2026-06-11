from datetime import datetime


today_now = datetime.today().date().isoformat()
month_now = today_now[:7]

print(today_now)
print(month_now)