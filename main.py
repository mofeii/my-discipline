from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import calendar
from datetime import datetime

app = FastAPI()


class DateList(BaseModel):
    dates: List[str]  # Формат: ["14-03-2025", "20-03-2025"]


@app.post("/calendar")
def generate_calendar(date_list: DateList):
    # Преобразуем строки в datetime format
    parsed_dates = [datetime.strptime(d, "%d-%m-%Y") for d in date_list.dates]
    if not parsed_dates:
        return {"error": "No dates provided"}

    # Предполагаем, что все даты относятся к одному месяцу
    target_year = parsed_dates[0].year
    target_month = parsed_dates[0].month

    # Создаем календарь месяца
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(target_year, target_month)

    # Создаем множество дней с галочкой
    check_days = set(d.day for d in parsed_dates)

    # Строка заголовка
    result = f"Календарь активностей для {target_year}-{str(target_month).zfill(2)}:\n"
    result += "Пн Вт Ср Чт Пт Сб Вс\n"

    # Формируем строки с днями
    for week in month_days:
        for day in week:
            if day == 0:
                result += "   "
            elif day in check_days:
                result += "✅ "
            elif day < 10:
                result += f" {day} "
            else:
                result += f"{day} "
        result += "\n"

    return {"calendar": result}
