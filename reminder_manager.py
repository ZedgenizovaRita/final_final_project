from common_imports import *
from ui.telegram_bot import send_telegram_message

def cancel_reminder_date_selection(self, instance):
    self.reminder_controls_layout.opacity = 0
    self.reminder_controls_layout.disabled = True
    self.reminder_mode = False
    self.selected_dates.clear()
    self.load_days_for_month()

def activate_reminder_mode(self, instance):
    self.reminder_mode = True
    self.selected_dates.clear()
    self.load_days_for_month()

def cancel_reminder_time_selection(self, popup):
    popup.dismiss()

    self.reminder_controls_layout.opacity = 0
    self.reminder_controls_layout.disabled = True
    self.reminder_mode = False
    self.selected_dates.clear()
    self.load_days_for_month()

def finalize_reminders(self, time_str, text_str, popup):
    try:
        hours, minutes = map(int, time_str.split(":"))
        if not (0 <= hours < 24) or not (0 <= minutes < 60):
            print("Неверный формат времени")
            return
    except ValueError:
        print("Неверный формат времени")
        return

    for date in self.selected_dates:
        if date not in self.reminders:
            self.reminders[date] = []
        self.reminders[date].append({
            'time': time_str,
            'text': text_str.strip(),
            'triggered': False
        })

    popup.dismiss()
    self.reminder_mode = False
    self.selected_dates.clear()
    self.load_days_for_month()
    self.reminder_controls_layout.opacity = 0
    self.reminder_controls_layout.disabled = True

def proceed_to_time_popup(self, instance):
    if not self.selected_dates:
        print("Выберите хотя бы одну дату")
        return

    self.reminder_controls_layout.opacity = 0
    self.reminder_controls_layout.disabled = True

    layout = BoxLayout(orientation='vertical', spacing=20, padding=10)

    time_input = TextInput(
        hint_text="Часы:Минуты",
        size_hint=(1, None),
        height=40,
        background_normal='',
        background_active='',
        background_color=(1, 1, 1, 1),
    )

    text_input = TextInput(
        hint_text="Текст напоминания",
        size_hint=(1, None),
        height=40,
        background_normal='',
        background_active='',
        background_color=(1, 1, 1, 1),
    )

    time_popup = Popup(title="Новое напоминание", content=layout, size_hint=(None, None), size=(420, 420))
    ok_btn = Button(text="ОК", size_hint_y=None, height=40, background_normal='',
                    background_color='green', color='white')
    cancel_btn = Button(text="Отмена", size_hint_y=None, height=40, background_normal='',
                        background_color='grey', color='white')
    ok_btn.bind(on_press=lambda x: self.finalize_reminders(time_input.text, text_input.text, time_popup))
    cancel_btn.bind(on_press=lambda x: self.cancel_reminder_time_selection(time_popup))

    time_label = Label(text="Введите время (например, 14:30):", size_hint_y=None, height=30)
    time_label.bind(size=lambda l, s: l.setter('text_size')(l, s))

    text_label = Label(text="Введите текст напоминания:", size_hint_y=None, height=30)
    text_label.bind(size=lambda l, s: l.setter('text_size')(l, s))

    layout.add_widget(time_label)
    layout.add_widget(time_input)
    layout.add_widget(text_label)
    layout.add_widget(text_input)
    layout.add_widget(ok_btn)
    layout.add_widget(cancel_btn)

    time_popup.open()

def handle_add_reminder(self, instance):
    self.reminder_mode = True
    self.selected_dates.clear()
    self.load_days_for_month()

    self.reminder_controls_layout.opacity = 1
    self.reminder_controls_layout.disabled = False

def toggle_reminder_date(self, date_str, button):
    if date_str in self.selected_dates:
        self.selected_dates.remove(date_str)
        button.background_color = (1, 1, 1, 1)
    else:
        self.selected_dates.add(date_str)
        button.background_color = 'green'

def save_reminders(self, time_str, popup):
    if not self.selected_dates or time_str in ['Часы:Минуты', ':']:
        print("Ошибка: выберите даты и время.")
        return

    for date in self.selected_dates:
        print(f"Сохраняю напоминание: {date} в {time_str}")
        # Тут можно сохранить в БД или файл

    # Очистка и выход из режима
    self.reminder_mode = False
    self.selected_dates.clear()
    self.load_days_for_month()
    popup.dismiss()

def check_reminders(self, dt):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")

    if current_date in self.reminders:
        for reminder in self.reminders[current_date]:
            if reminder.get("time") == current_time and not reminder.get("triggered"):
                self.show_reminder_popup(reminder.get("text"))
                self.send_telegram_message(reminder.get("text"))
                reminder["triggered"] = True

def show_reminder_popup(self, text):
    layout = BoxLayout(orientation='vertical', padding=10)
    layout.add_widget(Label(text=f"Напоминание:\n{text}", font_size=20))

    popup = Popup(title="Напоминание", content=layout, size_hint=(None, None), size=(300, 200))
    popup.open()

    sound = SoundLoader.load('alarm.ogg')
    sound.play()

def delete_reminder(self, date_str, index, layout_to_remove):
    if date_str in self.reminders:
        if 0 <= index < len(self.reminders[date_str]):
            del self.reminders[date_str][index]

            if not self.reminders[date_str]:
                del self.reminders[date_str]

    self.load_reminders_for_date(date_str)

def add_rem_for_date(self, instance):
    date_str = self.current_date.strftime("%Y-%m-%d")
    text = self.task_input_rem.text.strip()

    if text:
        self.open_time_popup_for_reminder(date_str, text)

def open_time_popup_for_reminder(self, date_str, reminder_text):
    layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    time_input = TextInput(
        hint_text="Часы:Минуты",
        size_hint=(1, None),
        height=44,
        background_color='white',
    )

    confirm_btn = Button(
        text="Добавить",
        size_hint_y=None,
        height=40,
        background_color=(0, 0.6, 0, 1),
        color='white'
    )

    cancel_btn = Button(
        text="Отмена",
        size_hint_y=None,
        height=40,
        background_color=(0.5, 0.5, 0.5, 1),
        color=(1, 1, 1, 1)
    )

    popup = Popup(title="Время напоминания", content=layout, size_hint=(None, None), size=(300, 300))

    confirm_btn.bind(
        on_press=lambda x: self.save_reminder_with_time(date_str, reminder_text, time_input.text, popup)
    )
    cancel_btn.bind(on_press=popup.dismiss)

    layout.add_widget(Label(text="Введите время (например, 09:30):", size_hint_y=None, height=30))
    layout.add_widget(time_input)
    layout.add_widget(confirm_btn)
    layout.add_widget(cancel_btn)

    popup.open()

def save_reminder_with_time(self, date_str, text, time_str, popup):
    try:
        hours, minutes = map(int, time_str.strip().split(":"))
        if not (0 <= hours < 24 and 0 <= minutes < 60):
            raise ValueError
    except Exception:
        print("Неверный формат времени")
        return

    self.reminders.setdefault(date_str, []).append({
        'time': f"{hours:02}:{minutes:02}",
        'text': text,
        'triggered': False})

    popup.dismiss()
    self.task_input_rem.text = ""

    self.load_reminders_for_date(date_str)