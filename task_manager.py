from common_imports import *
from ui.telegram_bot import send_telegram_message

def add_task_for_date(self, instance):
    date_str = self.current_date.strftime("%Y-%m-%d")
    text = self.task_input.text.strip()

    if text:
        idx = len(self.tasks)
        self.tasks.append([text, False, True, [], True])
        self.day_indexes.setdefault(date_str, []).append(idx)
        self.task_input.text = ""
        self.load_tasks_for_date(date_str)

def toggle_task_done(self, index, value, date_str):
    self.tasks[index][1] = value
    self.load_tasks_for_date(date_str)

def delete_task(self, index, date_str):
    self.tasks[index][2] = False
    self.load_tasks_for_date(date_str)

def open_sub(self, index, date_str):
    self.tasks[index][4] = not(self.tasks[index][4])
    self.load_tasks_for_date(date_str)

def add_task_for_list(self, name):
    text = self.task_input.text.strip()

    if text:
        idx = len(self.tasks)
        self.tasks.append([text, False, True, [], True])
        self.day_indexes.setdefault(name, []).append(idx)
        self.task_input.text = ""
        self.load_tasks_for_list(name)