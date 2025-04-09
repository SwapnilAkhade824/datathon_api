from datetime import datetime

def current_time():
    return datetime.utcnow()

def format_time(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")
