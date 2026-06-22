# main.py
from read_pdf import read_pdf, extract_shifts
from calendar_api import get_calendar_service, add_shift , add_salary
from caleculate_money import caleculate_money , caleculate_total_koma

PDF_PATH = "samples/ブース表_6月_merged.pdf"
money_hour = 1500 #時給
year = 2026 
month = 6



tables = read_pdf(PDF_PATH)
shifts = extract_shifts(tables)        # 16件のシフト
service = get_calendar_service()
for shift in shifts:                   # 1件ずつ add_shift に渡す
    add_shift(service, shift)

total_money = caleculate_money(caleculate_total_koma(shifts), money_hour, len(shifts))
add_salary(service, year, month, 25, total_money)