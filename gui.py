import customtkinter as ctk
from tkinter import messagebox
from core import ReportManager
import datetime
import json
import os

# Настройка темы по умолчанию
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ReportAssistant:
    def __init__(self, root):
        self.root = root
        self.styles = self.load_styles()
        
        # Применяем настройки из JSON
        self.root.title(self.styles["texts"]["app_title"])
        self.root.geometry(self.styles["app"]["window_size"])
        
        # Устанавливаем тему приложения
        ctk.set_appearance_mode(self.styles["app"]["theme"])
        ctk.set_default_color_theme(self.styles["app"]["color_theme"])
        
        self.manager = ReportManager()
        self.loaded_plans_key = None
        
        self.create_interface()

    def load_styles(self):
        """Загрузка стилей из JSON файла"""
        try:
            if os.path.exists("styles.json"):
                with open("styles.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # Создаем файл со стилями по умолчанию
                default_styles = {
                    "app": {
                        "window_size": "800x600",
                        "theme": "System",
                        "color_theme": "blue"
                    },
                    "colors": {
                        "primary": "#3B8ED0",
                        "primary_hover": "#36719D",
                        "danger": "#E74C3C",
                        "danger_hover": "#C0392B",
                        "accent": "#FF6B35",
                        "accent_hover": "#E55A2B",
                        "background": "transparent",
                        "tab_hover_dark": "#2B2B2B",
                        "tab_hover_light": "#F0F0F0"
                    },
                    "fonts": {
                        "title": {"size": 20, "weight": "bold"},
                        "tabs": {"size": 16, "weight": "bold"},
                        "buttons": {"size": 14, "weight": "normal"},
                        "input": {"size": 12, "weight": "normal"},
                        "content": {"size": 12, "weight": "normal"}
                    },
                    "sizes": {
                        "tab_button_height": 50,
                        "standard_button_height": 35,
                        "large_button_height": 40,
                        "add_button_width": 100,
                        "tabs_frame_width": 180,
                        "report_text_height": 150,
                        "plans_text_height": 120
                    },
                    "padding": {
                        "main_frame": 10,
                        "header_pady": 15,
                        "standard_pady": 10,
                        "small_pady": 5,
                        "button_padx": 10,
                        "tabs_padx": 10
                    },
                    "icons": {
                        "app_icon": "✏️",
                        "tasks_tab": "📝",
                        "report_tab": "📄",
                        "stats_tab": "📈",
                        "load_icon": "📥",
                        "add_icon": "➕",
                        "complete_icon": "✅",
                        "delete_icon": "🗑️",
                        "update_icon": "🔄",
                        "plans_icon": "🎯"
                    },
                    "texts": {
                        "app_title": "Планы и отчеты",
                        "tasks_tab": "Задачи",
                        "report_tab": "Отчет",
                        "stats_tab": "Статистика",
                        "load_button": "Загрузить вчерашние планы",
                        "add_button": "Добавить",
                        "complete_button": "Отметить выполненными",
                        "delete_button": "Удалить выделенное",
                        "update_button": "Обновить и скопировать отчет",
                        "task_placeholder": "Введите новую задачу...",
                        "tasks_label": "Текущие задачи:",
                        "report_label": "Отчет за сегодня:",
                        "stats_label": "Статистика за неделю"
                    }
                }
                with open("styles.json", "w", encoding="utf-8") as f:
                    json.dump(default_styles, f, ensure_ascii=False, indent=2)
                return default_styles
        except Exception as e:
            print(f"Ошибка загрузки стилей: {e}")
            # Возвращаем стили по умолчанию в случае ошибки
            return self.get_default_styles()

    def get_default_styles(self):
        """Стили по умолчанию на случай ошибки"""
        return {
            "app": {"window_size": "800x600", "theme": "System", "color_theme": "blue"},
            "colors": {
                "primary": "#3B8ED0", "primary_hover": "#36719D",
                "danger": "#E74C3C", "danger_hover": "#C0392B",
                "accent": "#FF6B35", "accent_hover": "#E55A2B",
                "background": "transparent"
            },
            "fonts": {
                "title": {"size": 20, "weight": "bold"},
                "tabs": {"size": 16, "weight": "bold"},
                "buttons": {"size": 14, "weight": "normal"},
                "input": {"size": 12, "weight": "normal"}
            },
            "sizes": {
                "tab_button_height": 50, "standard_button_height": 35,
                "large_button_height": 40, "tabs_frame_width": 180
            }
        }

    def create_interface(self):
        """Создаем интерфейс с использованием стилей из JSON"""
        # Основной контейнер без рамок
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.styles["colors"]["background"])
        self.main_frame.pack(fill="both", expand=True, padx=self.styles["padding"]["main_frame"], pady=self.styles["padding"]["main_frame"])
        
        # Заголовок
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=self.styles["colors"]["background"])
        header_frame.pack(fill="x", pady=(0, self.styles["padding"]["header_pady"]))
        
        self.title_label = ctk.CTkLabel(
            header_frame, 
            text=f"{self.styles['icons']['app_icon']} {self.styles['texts']['app_title']}",
            font=ctk.CTkFont(
                size=self.styles["fonts"]["title"]["size"], 
                weight=self.styles["fonts"]["title"]["weight"]
            )
        )
        self.title_label.pack(side="left")
        
        # Основной контент
        content_frame = ctk.CTkFrame(self.main_frame, fg_color=self.styles["colors"]["background"])
        content_frame.pack(fill="both", expand=True)
        
        # Вкладки слева
        self.tabs_frame = ctk.CTkFrame(content_frame, width=self.styles["sizes"]["tabs_frame_width"])
        self.tabs_frame.pack(side="left", fill="y", padx=(0, self.styles["padding"]["tabs_padx"]))
        
        # Область контента
        self.content_area = ctk.CTkFrame(content_frame, fg_color=self.styles["colors"]["background"])
        self.content_area.pack(side="right", fill="both", expand=True)
        
        self.setup_tabs()
        self.setup_tab_today()

    def setup_tabs(self):
        """Настройка вкладок с использованием стилей из JSON"""
        tab_font = ctk.CTkFont(
            size=self.styles["fonts"]["tabs"]["size"], 
            weight=self.styles["fonts"]["tabs"]["weight"]
        )
        
        # Определяем цвет для неактивных вкладок
        hover_color = (
            self.styles["colors"]["tab_hover_dark"] 
            if ctk.get_appearance_mode() == "Dark" 
            else self.styles["colors"]["tab_hover_light"]
        )
        
        # Вкладка Задачи
        self.tab_tasks_btn = ctk.CTkButton(
            self.tabs_frame,
            text=f"{self.styles['icons']['tasks_tab']} {self.styles['texts']['tasks_tab']}",
            font=tab_font,
            height=self.styles["sizes"]["tab_button_height"],
            fg_color=self.styles["colors"]["primary"],
            hover_color=self.styles["colors"]["primary_hover"],
            command=self.show_tasks_tab
        )
        self.tab_tasks_btn.pack(fill="x", pady=(0, self.styles["padding"]["small_pady"]))
        
        # Вкладка Отчет
        self.tab_report_btn = ctk.CTkButton(
            self.tabs_frame,
            text=f"{self.styles['icons']['report_tab']} {self.styles['texts']['report_tab']}",
            font=tab_font,
            height=self.styles["sizes"]["tab_button_height"],
            fg_color=self.styles["colors"]["background"],
            hover_color=hover_color,
            command=self.show_report_tab
        )
        self.tab_report_btn.pack(fill="x", pady=self.styles["padding"]["small_pady"])
        
        # Вкладка Статистика
        self.tab_stats_btn = ctk.CTkButton(
            self.tabs_frame,
            text=f"{self.styles['icons']['stats_tab']} {self.styles['texts']['stats_tab']}",
            font=tab_font,
            height=self.styles["sizes"]["tab_button_height"],
            fg_color=self.styles["colors"]["background"],
            hover_color=hover_color,
            command=self.show_stats_tab
        )
        self.tab_stats_btn.pack(fill="x", pady=self.styles["padding"]["small_pady"])
        
        self.current_tab = "tasks"

    def setup_tab_today(self):
        """Вкладка задач"""
        # Кнопка загрузки планов
        self.load_btn = ctk.CTkButton(
            self.content_area,
            text=f"{self.styles['icons']['load_icon']} {self.styles['texts']['load_button']}",
            command=self.load_yesterday_plans,
            font=ctk.CTkFont(size=self.styles["fonts"]["buttons"]["size"]),
            height=self.styles["sizes"]["standard_button_height"]
        )
        self.load_btn.pack(fill="x", pady=(0, self.styles["padding"]["standard_pady"]))
        
        # Поле ввода
        input_frame = ctk.CTkFrame(self.content_area, fg_color=self.styles["colors"]["background"])
        input_frame.pack(fill="x", pady=self.styles["padding"]["standard_pady"])
        
        self.task_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text=self.styles["texts"]["task_placeholder"],
            font=ctk.CTkFont(size=self.styles["fonts"]["input"]["size"]),
            height=self.styles["sizes"]["standard_button_height"]
        )
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, self.styles["padding"]["button_padx"]))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        self.add_btn = ctk.CTkButton(
            input_frame,
            text=f"{self.styles['icons']['add_icon']} {self.styles['texts']['add_button']}",
            command=self.add_task,
            width=self.styles["sizes"]["add_button_width"],
            height=self.styles["sizes"]["standard_button_height"]
        )
        self.add_btn.pack(side="right")
        
        # Список задач
        tasks_label = ctk.CTkLabel(
            self.content_area,
            text=self.styles["texts"]["tasks_label"],
            font=ctk.CTkFont(size=self.styles["fonts"]["buttons"]["size"], weight="bold")
        )
        tasks_label.pack(anchor="w", pady=(self.styles["padding"]["standard_pady"], self.styles["padding"]["small_pady"]))
        
        self.tasks_list = ctk.CTkTextbox(
            self.content_area,
            font=ctk.CTkFont(size=self.styles["fonts"]["content"]["size"]),
            wrap="word"
        )
        self.tasks_list.pack(fill="both", expand=True, pady=self.styles["padding"]["small_pady"])
        
        # Кнопки управления
        btn_frame = ctk.CTkFrame(self.content_area, fg_color=self.styles["colors"]["background"])
        btn_frame.pack(fill="x", pady=self.styles["padding"]["standard_pady"])
        
        self.complete_btn = ctk.CTkButton(
            btn_frame,
            text=f"{self.styles['icons']['complete_icon']} {self.styles['texts']['complete_button']}",
            command=self.complete_selected,
            font=ctk.CTkFont(size=self.styles["fonts"]["buttons"]["size"]),
            height=self.styles["sizes"]["standard_button_height"]
        )
        self.complete_btn.pack(side="left", padx=(0, self.styles["padding"]["button_padx"]))
        
        self.delete_btn = ctk.CTkButton(
            btn_frame,
            text=f"{self.styles['icons']['delete_icon']} {self.styles['texts']['delete_button']}",
            command=self.delete_selected,
            font=ctk.CTkFont(size=self.styles["fonts"]["buttons"]["size"]),
            fg_color=self.styles["colors"]["danger"],
            hover_color=self.styles["colors"]["danger_hover"],
            height=self.styles["sizes"]["standard_button_height"]
        )
        self.delete_btn.pack(side="left")

    def setup_tab_report(self):
        """Вкладка отчета"""
        # Отчет за сегодня
        report_label = ctk.CTkLabel(
            self.content_area,
            text=f"{self.styles['icons']['report_tab']} {self.styles['texts']['report_label']}",
            font=ctk.CTkFont(size=self.styles["fonts"]["buttons"]["size"], weight="bold")
        )
        report_label.pack(anchor="w", pady=(0, self.styles["padding"]["small_pady"]))
        
        self.report_display = ctk.CTkTextbox(
            self.content_area,
            font=ctk.CTkFont(size=self.styles["fonts"]["content"]["size"]),
            height=self.styles["sizes"]["report_text_height"]
        )
        self.report_display.pack(fill="x", pady=(0, self.styles["padding"]["standard_pady"]))
        
        # Планы на завтра
        self.plans_label = ctk.CTkLabel(
            self.content_area,
            text="",
            font=ctk.CTkFont(size=self.styles["fonts"]["buttons"]["size"], weight="bold")
        )
        self.plans_label.pack(anchor="w", pady=(0, self.styles["padding"]["small_pady"]))
        self.update_plans_label()
        
        self.plans_input = ctk.CTkTextbox(
            self.content_area,
            font=ctk.CTkFont(size=self.styles["fonts"]["content"]["size"]),
            height=self.styles["sizes"]["plans_text_height"]
        )
        self.plans_input.pack(fill="x", pady=(0, self.styles["padding"]["standard_pady"]))
        
        # Кнопка обновления
        self.update_btn = ctk.CTkButton(
            self.content_area,
            text=f"{self.styles['icons']['update_icon']} {self.styles['texts']['update_button']}",
            command=self.update_and_save_report,
            font=ctk.CTkFont(size=self.styles["fonts"]["buttons"]["size"]),
            height=self.styles["sizes"]["large_button_height"],
            fg_color=self.styles["colors"]["accent"],
            hover_color=self.styles["colors"]["accent_hover"]
        )
        self.update_btn.pack(fill="x")

    def setup_tab_stats(self):
        """Вкладка статистики"""
        stats_label = ctk.CTkLabel(
            self.content_area,
            text=f"{self.styles['icons']['stats_tab']} {self.styles['texts']['stats_label']}",
            font=ctk.CTkFont(size=self.styles["fonts"]["buttons"]["size"], weight="bold")
        )
        stats_label.pack(anchor="w", pady=(0, self.styles["padding"]["standard_pady"]))
        
        self.stats_display = ctk.CTkTextbox(
            self.content_area,
            font=ctk.CTkFont(size=self.styles["fonts"]["content"]["size"])
        )
        self.stats_display.pack(fill="both", expand=True)

    # Остальные методы остаются без изменений (load_yesterday_plans, add_task, complete_selected, и т.д.)
    # ... [все остальные методы из предыдущей версии] ...

    def show_tasks_tab(self):
        """Показать вкладку задач"""
        self.current_tab = "tasks"
        self.update_tab_buttons()
        self.clear_content_area()
        self.setup_tab_today()

    def show_report_tab(self):
        """Показать вкладку отчета"""
        self.current_tab = "report"
        self.update_tab_buttons()
        self.clear_content_area()
        self.setup_tab_report()
        self.update_report()

    def show_stats_tab(self):
        """Показать вкладку статистики"""
        self.current_tab = "stats"
        self.update_tab_buttons()
        self.clear_content_area()
        self.setup_tab_stats()
        self.update_stats()

    def update_tab_buttons(self):
        """Обновить стиль кнопок вкладок"""
        hover_color = (
            self.styles["colors"]["tab_hover_dark"] 
            if ctk.get_appearance_mode() == "Dark" 
            else self.styles["colors"]["tab_hover_light"]
        )
        
        self.tab_tasks_btn.configure(
            fg_color=self.styles["colors"]["primary"] if self.current_tab == "tasks" else self.styles["colors"]["background"],
            hover_color=self.styles["colors"]["primary_hover"] if self.current_tab == "tasks" else hover_color
        )
        self.tab_report_btn.configure(
            fg_color=self.styles["colors"]["primary"] if self.current_tab == "report" else self.styles["colors"]["background"],
            hover_color=self.styles["colors"]["primary_hover"] if self.current_tab == "report" else hover_color
        )
        self.tab_stats_btn.configure(
            fg_color=self.styles["colors"]["primary"] if self.current_tab == "stats" else self.styles["colors"]["background"],
            hover_color=self.styles["colors"]["primary_hover"] if self.current_tab == "stats" else hover_color
        )

    def clear_content_area(self):
        """Очистить область контента"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def load_yesterday_plans(self):
        """Загрузка планов"""
        plans, source_key = self.manager.get_yesterday_plans()
        if not plans:
            messagebox.showinfo("Инфо", "Актуальных планов нет")
            return
        
        if self.loaded_plans_key == source_key:
            messagebox.showinfo("Инфо", "Планы уже загружены")
            return
        
        current_text = self.tasks_list.get("1.0", "end-1c")
        new_plans = [plan for plan in plans if plan not in current_text]
        
        if not new_plans:
            messagebox.showinfo("Инфо", "Все планы уже добавлены")
            self.loaded_plans_key = source_key
            return
        
        for plan in new_plans:
            self.tasks_list.insert("end", f"• {plan}\n")
        
        self.loaded_plans_key = source_key
        messagebox.showinfo("Успех", f"Загружено {len(new_plans)} планов!")

    def add_task(self):
        """Добавление задачи"""
        task = self.task_entry.get().strip()
        if task:
            self.tasks_list.insert("end", f"• {task}\n")
            self.task_entry.delete(0, "end")

    def complete_selected(self):
        """Отметка выполненных задач"""
        try:
            selected_text = self.tasks_list.get("sel.first", "sel.last")
            if selected_text:
                tasks = [line.strip('• \n') for line in selected_text.split('\n') if line.strip()]
                for task in tasks:
                    if task:
                        self.manager.add_completed_task(task)
                
                # Удаляем выделенный текст
                self.tasks_list.delete("sel.first", "sel.last")
                self.update_report()
                messagebox.showinfo("Успех", f"Отмечено {len(tasks)} задач!")
        except:
            messagebox.showwarning("Внимание", "Выделите задачи для отметки!")

    def delete_selected(self):
        """Удаление выделенных задач"""
        try:
            if self.tasks_list.tag_ranges("sel"):
                if messagebox.askyesno("Подтверждение", "Удалить выделенные задачи?"):
                    self.tasks_list.delete("sel.first", "sel.last")
        except:
            messagebox.showwarning("Внимание", "Выделите задачи для удаления!")

    def update_plans_label(self):
        """Обновление метки планов"""
        try:
            next_workday = self.manager.get_next_workday()
            next_workday_str = next_workday.strftime("%d.%m.%y")
            day_name = next_workday.strftime("%A")
            days_ru = {
                'Monday': 'понедельник', 'Tuesday': 'вторник', 'Wednesday': 'среда',
                'Thursday': 'четверг', 'Friday': 'пятница'
            }
            day_ru = days_ru.get(day_name, day_name)
            if hasattr(self, 'plans_label'):
                self.plans_label.configure(text=f"{self.styles['icons']['plans_icon']} Планы на {day_ru} ({next_workday_str}):")
        except Exception as e:
            print(f"Ошибка при обновлении метки планов: {e}")

    def update_report(self):
        """Обновление отчета"""
        try:
            report = self.manager.get_today_report()
            completed = report.get("completed", [])
            today = datetime.datetime.now().strftime("%d.%m.%y")
            
            report_text = f"Отчет за {today}:\n"
            for i, task in enumerate(completed, 1):
                report_text += f"{i}. {task}\n"
            
            if hasattr(self, 'report_display'):
                self.report_display.delete("1.0", "end")
                self.report_display.insert("1.0", report_text)
        except Exception as e:
            print(f"Ошибка при обновлении отчета: {e}")

    def update_and_save_report(self):
        """Сохранение и копирование отчета"""
        try:
            today = datetime.datetime.now().strftime("%d.%m.%y")
            next_workday = self.manager.get_next_workday()
            next_workday_str = next_workday.strftime("%d.%m.%y")
            
            report = self.manager.get_today_report()
            completed = report.get("completed", [])
            plans_text = self.plans_input.get("1.0", "end-1c").strip()
            
            # Формируем полный отчет
            full_report = f"Отчет за {today}:\n"
            for i, task in enumerate(completed, 1):
                full_report += f"{i}. {task}\n"
            
            full_report += f"\nПлан на {next_workday_str}:\n"
            if plans_text:
                plans = [p.strip() for p in plans_text.split('\n') if p.strip()]
                for i, plan in enumerate(plans, 1):
                    full_report += f"{i}. {plan}\n"
            else:
                full_report += "(планов нет)\n"
            
            # Сохраняем планы
            if plans_text:
                plans = [p.strip() for p in plans_text.split('\n') if p.strip()]
                self.manager.set_tomorrow_plans(plans)
            
            # Копируем в буфер
            self.root.clipboard_clear()
            self.root.clipboard_append(full_report)
            
            # Очищаем поля
            self.plans_input.delete("1.0", "end")
            
            messagebox.showinfo("Успех", "Отчет скопирован и сохранен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить отчет: {e}")

    def update_stats(self):
        """Обновление статистики"""
        try:
            stats = self.manager.get_weekly_stats()
            total = sum(stats.values())
            
            stats_text = f"📊 Статистика за неделю\n\nВсего задач: {total}\n\nПо дням:\n"
            for day, count in stats.items():
                stats_text += f"{day}: {count} задач\n"
            
            if hasattr(self, 'stats_display'):
                self.stats_display.delete("1.0", "end")
                self.stats_display.insert("1.0", stats_text)
        except Exception as e:
            print(f"Ошибка при обновлении статистики: {e}")