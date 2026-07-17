from datetime import datetime

def get_time():
    now = datetime.now()
    hour = now.strftime("%I").lstrip("0")
    minutes = now.strftime("%M")
    am_pm = now.strftime("%p")
    if minutes == "00":
        return f"It's {hour} {am_pm}."
    else:
        return f"It's {hour} {minutes} {am_pm}."

def get_date():
    now = datetime.now()
    day = now.strftime("%A")
    date = now.strftime("%B %d").replace(" 0", " ")
    return f"Today is {day}, {date}."

def get_time_raw():
    return datetime.now().strftime("%I:%M %p").lstrip("0")

def get_date_raw():
    return datetime.now().strftime("%A, %B %d")