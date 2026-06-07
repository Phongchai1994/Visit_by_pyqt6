from datetime import datetime

def date_convers(date_input):
    dt = datetime.strptime(str(date_input).split('.')[0], "%Y-%m-%d %H:%M:%S")
    months = [
        "", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    day = dt.day
    month = months[dt.month]
    year = dt.year
    hour = dt.hour
    minute = dt.minute
    value = f"{day} {month} {year} เวลา {hour:02d}:{minute:02d} น."
    return value