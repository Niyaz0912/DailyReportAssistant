import json
import datetime
from typing import Dict, List, Tuple


class ReportManager:
    def __init__(self, data_file: str = "data.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self) -> Dict:
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get_date_key(self, date: datetime.datetime = None):
        date = date or datetime.datetime.now()
        return date.strftime("%Y-%m-%d")

    def get_yesterday_plans(self) -> Tuple[List[str], str]:
        """Получить планы с предыдущего рабочего дня (например, с пятницы для понедельника)

        Returns:
            Tuple[List[str], str]: Список планов и ключ даты, откуда они взяты
        """
        today = datetime.datetime.now()
        source_key = ""

        # Если сегодня понедельник, пробуем загрузить планы с пятницы
        if today.weekday() == 0:  # Monday
            friday = today - datetime.timedelta(days=3)
            friday_key = self.get_date_key(friday)
            if friday_key in self.data:
                plans = self.data[friday_key].get("tomorrow_plans", [])
                if plans:
                    return plans, friday_key

        # Во всех остальных случаях берем предыдущий календарный день
        yesterday = today - datetime.timedelta(days=1)
        yesterday_key = self.get_date_key(yesterday)
        source_key = yesterday_key

        if yesterday_key in self.data:
            return self.data[yesterday_key].get("tomorrow_plans", []), yesterday_key
        return [], ""

    def get_next_workday(self, date: datetime.datetime = None) -> datetime.datetime:
        """Получить следующий рабочий день (если пятница - возвращает понедельник)"""
        date = date or datetime.datetime.now()
        next_day = date + datetime.timedelta(days=1)
        
        # Если следующий день - суббота (weekday=5), пропускаем до понедельника
        if next_day.weekday() == 5:  # Суббота
            next_day += datetime.timedelta(days=2)  # Понедельник
        # Если следующий день - воскресенье (weekday=6), пропускаем до понедельника
        elif next_day.weekday() == 6:  # Воскресенье
            next_day += datetime.timedelta(days=1)  # Понедельник
        
        return next_day

    def set_tomorrow_plans(self, plans: List[str]):
        today_key = self.get_date_key()
        if today_key not in self.data:
            self.data[today_key] = {"completed": [], "tomorrow_plans": []}

        self.data[today_key]["tomorrow_plans"] = plans
        self.save_data()

    def add_completed_task(self, task: str):
        today_key = self.get_date_key()
        if today_key not in self.data:
            self.data[today_key] = {"completed": [], "tomorrow_plans": []}

        self.data[today_key]["completed"].append(task)
        self.save_data()

    def get_today_report(self) -> Dict:
        today_key = self.get_date_key()
        return self.data.get(today_key, {"completed": [], "tomorrow_plans": []})

    def get_weekly_stats(self) -> Dict:
        stats = {}
        for i in range(7):
            date = datetime.datetime.now() - datetime.timedelta(days=i)
            date_key = self.get_date_key(date)
            day_name = date.strftime("%a")

            if date_key in self.data:
                stats[day_name] = len(self.data[date_key].get("completed", []))
            else:
                stats[day_name] = 0
        return stats

    