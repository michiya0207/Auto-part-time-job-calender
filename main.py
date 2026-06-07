# main.py
from read_pdf import read_pdf, extract_shifts
from calendar_api import get_calendar_service, add_shift

tables = read_pdf()
shifts = extract_shifts(tables)        # 16件のシフト
service = get_calendar_service()
for shift in shifts:                   # 1件ずつ add_shift に渡す
    add_shift(service, shift)
