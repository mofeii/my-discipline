from fastapi import FastAPI
from pydantic import BaseModel
import calendar
from datetime import datetime

app = FastAPI()

class DatesRequest(BaseModel):
    dates: list[str]

@app.post("/calendar")
def get_calendar(request: DatesRequest):
    # Парсим входные строки в datetime и забираем год/месяц из первой даты
    date_objs = [datetime.strptime(d, "%d-%m-%Y") for d in request.dates]
    if not date_objs:
        return {"calendar": "Нет дат для обработки"}

    year, month = date_objs[0].year, date_objs[0].month
    # Множество дней, которые нужно отметить
    mark_days = {dt.day for dt in date_objs if dt.year == year and dt.month == month}

    # Генерируем матрицу недель: каждая неделя — список из 7 чисел (0 — если день не в этом месяце)
    cal = calendar.Calendar(firstweekday=0)  # 0 = понедельник
    weeks = cal.monthdayscalendar(year, month)

    # Собираем текст по строкам
    lines = []
    for week in weeks:
        cells = []
        for day in week:
            if day == 0:
                cell = ""           # пусто
            elif day in mark_days:
                cell = "✅"         # эмодзи вместо числа
            else:
                cell = str(day)     # обычный номер
            cells.append(cell)
        # Выравниваем каждую ячейку по правому краю в ширине 2 символа
        row = " ".join(f"{cell:>2}" for cell in cells)
        lines.append(row)

    header = "Пн Вт Ср Чт Пт Сб Вс"
    title = f"Календарь активностей для {year}-{month:02d}:"
    calendar_text = "\n".join([title, header] + lines)

    return {"calendar": calendar_text}
