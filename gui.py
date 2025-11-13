import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from core import ReportManager  # ← ИМПОРТИРУЕМ ИЗ CORE
import datetime


class ReportAssistant:  # ← ПРАВИЛЬНОЕ название класса
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Report Assistant")
        self.root.geometry("800x600")

        self.manager = ReportManager()  # ← создаем менеджер

        # ИНИЦИАЛИЗИРУЕМ все атрибуты здесь
        self.notebook = None
        self.tab_today = None
        self.tab_report = None
        self.tab_stats = None
        self.task_entry = None
        self.tasks_list = None
        self.report_display = None
        self.plans_input = None
        self.stats_display = None

        self.create_interface()
        self.load_data()

    def create_interface(self):
        """Создаем интерфейс с тремя вкладками"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Вкладки
        self.tab_today = ttk.Frame(self.notebook)
        self.tab_report = ttk.Frame(self.notebook)
        self.tab_stats = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_today, text="📝 Сегодня")
        self.notebook.add(self.tab_report, text="📊 Отчет")
        self.notebook.add(self.tab_stats, text="📈 Статистика")

        self.setup_tab_today()
        self.setup_tab_report()
        self.setup_tab_stats()

    def setup_tab_today(self):
        """Вкладка - Задачи на сегодня"""
        # Заголовок
        title = tk.Label(self.tab_today, text="Задачи на сегодня", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        # Кнопка загрузки вчерашних планов
        load_btn = tk.Button(self.tab_today, text="📥 Загрузить вчерашние планы",
                             command=self.load_yesterday_plans, bg="#4CAF50", fg="white")
        load_btn.pack(pady=5)

        # Поле для новых задач
        input_frame = tk.Frame(self.tab_today)
        input_frame.pack(fill='x', padx=10, pady=5)

        self.task_entry = tk.Entry(input_frame, font=("Arial", 10))
        self.task_entry.pack(side='left', fill='x', expand=True)
        self.task_entry.bind('<Return>', lambda e: self.add_task())

        add_btn = tk.Button(input_frame, text="➕ Добавить", command=self.add_task)
        add_btn.pack(side='right', padx=5)

        # Список задач
        self.tasks_list = tk.Listbox(self.tab_today, font=("Arial", 10), height=12)
        self.tasks_list.pack(fill='both', expand=True, padx=10, pady=5)

        # Кнопки управления
        btn_frame = tk.Frame(self.tab_today)
        btn_frame.pack(fill='x', padx=10, pady=10)

        complete_btn = tk.Button(btn_frame, text="✅ Выполнено",
                                 command=self.complete_task, bg="#2196F3", fg="white")
        complete_btn.pack(side='left', padx=5)

        delete_btn = tk.Button(btn_frame, text="❌ Удалить",
                               command=self.delete_task, bg="#f44336", fg="white")
        delete_btn.pack(side='left', padx=5)

    def setup_tab_report(self):
        """Вкладка - Отчет и планы"""
        # Отчет за сегодня
        report_label = tk.Label(self.tab_report, text="Отчет за сегодня:", font=("Arial", 12))
        report_label.pack(anchor='w', padx=10, pady=(10, 0))

        self.report_display = scrolledtext.ScrolledText(self.tab_report, height=8, font=("Arial", 10))
        self.report_display.pack(fill='both', expand=True, padx=10, pady=5)

        # Планы на завтра
        plans_label = tk.Label(self.tab_report, text="Планы на завтра:", font=("Arial", 12))
        plans_label.pack(anchor='w', padx=10, pady=(10, 0))

        self.plans_input = scrolledtext.ScrolledText(self.tab_report, height=6, font=("Arial", 10))
        self.plans_input.pack(fill='both', expand=True, padx=10, pady=5)

        # Кнопки отчета
        report_btn_frame = tk.Frame(self.tab_report)
        report_btn_frame.pack(fill='x', padx=10, pady=10)

        update_btn = tk.Button(report_btn_frame, text="🔄 Обновить отчет",
                               command=self.update_report, bg="#FF9800", fg="white")
        update_btn.pack(side='left', padx=5)

        copy_btn = tk.Button(report_btn_frame, text="📋 Копировать отчет",
                             command=self.copy_report, bg="#9C27B0", fg="white")
        copy_btn.pack(side='left', padx=5)

    def setup_tab_stats(self):
        """Вкладка - Статистика"""
        self.stats_display = scrolledtext.ScrolledText(self.tab_stats, height=15, font=("Arial", 10))
        self.stats_display.pack(fill='both', expand=True, padx=10, pady=10)

    # ОСНОВНЫЕ МЕТОДЫ
    def load_data(self):
        """Загрузка данных при запуске"""
        self.update_report()
        self.update_stats()

    def load_yesterday_plans(self):
        """Загрузить вчерашние планы"""
        plans = self.manager.get_yesterday_plans()
        if plans:
            for plan in plans:
                self.tasks_list.insert(tk.END, plan)
            messagebox.showinfo("Успех", f"Загружено {len(plans)} планов!")
        else:
            messagebox.showinfo("Инфо", "Вчерашних планов нет")

    def add_task(self):
        """Добавить новую задачу"""
        task = self.task_entry.get().strip()
        if task:
            self.tasks_list.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def complete_task(self):
        """Отметить задачу выполненной"""
        if self.tasks_list.curselection():
            index = self.tasks_list.curselection()[0]
            task = self.tasks_list.get(index)
            self.manager.add_completed_task(task)
            self.tasks_list.delete(index)
            self.update_report()
        else:
            messagebox.showwarning("Внимание", "Выберите задачу!")

    def delete_task(self):
        """Удалить задачу"""
        if self.tasks_list.curselection():
            index = self.tasks_list.curselection()[0]
            self.tasks_list.delete(index)
        else:
            messagebox.showwarning("Внимание", "Выберите задачу!")

    def update_report(self):
        """Обновить отчет"""
        report = self.manager.get_today_report()
        completed = report.get("completed", [])
        today = datetime.datetime.now().strftime("%d.%m.%y")

        # Очищаем и заполняем отчет
        self.report_display.delete(1.0, tk.END)
        report_text = f"Отчет за {today}:\n"
        for i, task in enumerate(completed, 1):
            report_text += f"{i}. {task}\n"
        self.report_display.insert(1.0, report_text)

        # Сохраняем планы на завтра
        plans_text = self.plans_input.get(1.0, tk.END).strip()
        if plans_text:
            plans = [p.strip() for p in plans_text.split('\n') if p.strip()]
            self.manager.set_tomorrow_plans(plans)

    def copy_report(self):
        """Копировать полный отчет"""
        today = datetime.datetime.now().strftime("%d.%m.%y")
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d.%m.%y")

        report = self.manager.get_today_report()
        completed = report.get("completed", [])
        plans_text = self.plans_input.get(1.0, tk.END).strip()

        full_report = f"Отчет за {today}:\n"
        for i, task in enumerate(completed, 1):
            full_report += f"{i}. {task}\n"

        full_report += f"\nПлан на {tomorrow}:\n"
        if plans_text:
            for i, plan in enumerate(plans_text.split('\n'), 1):
                if plan.strip():
                    full_report += f"{i}. {plan.strip()}\n"

        self.root.clipboard_clear()
        self.root.clipboard_append(full_report)
        messagebox.showinfo("Успех", "Отчет скопирован!")

    def update_stats(self):
        """Обновить статистику"""
        stats = self.manager.get_weekly_stats()
        total = sum(stats.values())

        stats_text = f"📊 Статистика за неделю\n\nВсего задач: {total}\n\nПо дням:\n"
        for day, count in stats.items():
            stats_text += f"{day}: {count} задач\n"

        self.stats_display.delete(1.0, tk.END)
        self.stats_display.insert(1.0, stats_text)