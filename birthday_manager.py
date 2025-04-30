from common_imports import *
from ui.telegram_bot import send_telegram_message

def start_daily_birthday_loop(self, dt):
    self.send_daily_birthdays_to_telegram()
    Clock.schedule_interval(lambda dt: self.send_daily_birthdays_to_telegram(), 24 * 60 * 60)

def schedule_birthday_check(self):
    now = datetime.now()
    target = now.replace(hour=10, minute=0, second=0, microsecond=0)
    if now > target:
        target += timedelta(days=1)
    delay = (target - now).total_seconds()
    Clock.schedule_once(self.start_daily_birthday_loop, delay)

def select_birthday_date(self, instance):
    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    date_label = Label(text="Введите дату (ДД.ММ):")
    self.birthday_date_input = TextInput(multiline=False, hint_text="Например: 27.04", size_hint=(1, None),
                                         height=30)

    name_label = Label(text="Введите имя:")
    self.birthday_name_input = TextInput(multiline=False, hint_text="Имя человека", size_hint=(1, None), height=30)

    buttons_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
    ok_button = Button(text="ОК", background_color=(0.1, 0.7, 0.1, 1))
    cancel_button = Button(text="Отмена", background_color=(0.5, 0.5, 0.5, 1))

    buttons_layout.add_widget(cancel_button)
    buttons_layout.add_widget(ok_button)

    layout.add_widget(date_label)
    layout.add_widget(self.birthday_date_input)
    layout.add_widget(name_label)
    layout.add_widget(self.birthday_name_input)
    layout.add_widget(buttons_layout)

    popup = Popup(title="Добавить День рождения",
                  content=layout,
                  size_hint=(None, None), size=(350, 250),
                  auto_dismiss=False)

    def save_birthday(instance):
        date_text = self.birthday_date_input.text.strip()
        name_text = self.birthday_name_input.text.strip()

        try:
            if date_text:
                if len(date_text.split('.')) == 2:
                    dt = datetime.strptime(date_text, "%d.%m")
                    date_str = dt.strftime("%d.%m")

                    if name_text:
                        if date_str in self.birthdays:
                            self.birthdays[date_str].append(name_text)
                        else:
                            self.birthdays[date_str] = [name_text]
                        popup.dismiss()
                        self.load_days_for_month()
                    else:
                        self.birthday_name_input.text = "Имя не может быть пустым"
                else:
                    self.birthday_date_input.text = "Неверный формат даты"
            else:
                self.birthday_date_input.text = "Дата не может быть пустой"

        except ValueError:
            self.birthday_date_input.text = "Неверный формат"

    ok_button.bind(on_press=save_birthday)
    cancel_button.bind(on_press=popup.dismiss)
    popup.open()

def select_birthday_date_for_delete(self, instance):
    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    date_label = Label(text="Введите дату (ДД.ММ):")
    self.birthday_date_input = TextInput(multiline=False, hint_text="Например: 27.04", size_hint=(1, None),
                                         height=30)

    buttons_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
    ok_button = Button(text="ОК", background_color=(0.1, 0.7, 0.1, 1))
    cancel_button = Button(text="Отмена", background_color=(0.5, 0.5, 0.5, 1))

    buttons_layout.add_widget(cancel_button)
    buttons_layout.add_widget(ok_button)

    layout.add_widget(date_label)
    layout.add_widget(self.birthday_date_input)
    layout.add_widget(buttons_layout)

    popup = Popup(title="Удалить День рождения",
                  content=layout,
                  size_hint=(None, None), size=(350, 250),
                  auto_dismiss=False)

    def on_ok(instance):
        date_str = self.birthday_date_input.text.strip()
        popup.dismiss()
        self.show_birthdays_to_delete(date_str)

    ok_button.bind(on_press=on_ok)
    cancel_button.bind(on_press=popup.dismiss)
    popup.open()

def show_birthdays_to_delete(self, date_str):
    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    label = Label(text=f"Дни рождения {date_str}:", size_hint_y=None, height=30)
    layout.add_widget(label)

    if date_str in self.birthdays:
        people = self.birthdays.get(date_str, [])

        for name in people:
            row = BoxLayout(size_hint_y=None, height=40)
            name_label = Label(text=name)

            del_btn = ImageButton(source="delete.png", size_hint=(None, None), size=(50, 50))
            row.add_widget(name_label)
            row.add_widget(del_btn)

            def make_delete_callback(n):
                def callback(inst):
                    self.birthdays[date_str].remove(n)
                    if not self.birthdays[date_str]:
                        del self.birthdays[date_str]
                    popup.dismiss()
                    self.show_birthdays_to_delete(date_str)

                return callback

            del_btn.bind(on_press=make_delete_callback(name))
            layout.add_widget(row)

    layout.add_widget(Widget())

    close_btn = Button(text="Отмена", size_hint_y=None, height=40)
    layout.add_widget(close_btn)

    popup = Popup(title="Удалить имя", content=layout, size_hint=(None, None), size=(350, 400))
    close_btn.bind(on_press=popup.dismiss)
    popup.open()

def send_daily_birthdays_to_telegram(self):
    today = datetime.now().strftime("%d.%m")
    if today in self.birthdays:
        names = self.birthdays[today]
        names_str = ', '.join(names)
        message = f"🎉 Сегодня День рождения у: {names_str}"
        send_telegram_message(message)