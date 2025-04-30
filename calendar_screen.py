from common_imports import *

def build_cal_0(self):
    self.main_layout.clear_widgets()

    calendar_view = self.build_calendar()
    self.main_layout.add_widget(calendar_view)

def build_calendar(self):
    today = datetime.today()
    year, month = today.year, today.month

    main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    header_layout = BoxLayout(size_hint_y=None, height=40, orientation='horizontal', padding=(10, 0))

    if self.current_theme == self.light_theme:
        self.back_button = ImageButton(source="back_black.png", size_hint=(None, None), size=(32, 32))
    else:
        self.back_button = ImageButton(source="back_white.png", size_hint=(None, None), size=(32, 32))
    self.back_button.bind(on_press=self.switch_to_main)
    header_layout.add_widget(self.back_button)

    if self.current_theme == self.light_theme:
        theme_switch = Switch(active=False)
    else:
        theme_switch = Switch(active=True)
    theme_switch.bind(active=self.on_theme_switch)
    header_layout.add_widget(theme_switch)

    if self.current_theme == self.light_theme:
        self.settings_button = ImageButton(source="setting_black.png", size_hint=(None, None), size=(32, 32))
    else:
        self.settings_button = ImageButton(source="setting_white.png", size_hint=(None, None), size=(32, 32))
    self.settings_button.bind(on_release=self.open_settings_menu)
    header_layout.add_widget(self.settings_button)
    main_layout.add_widget(header_layout)

    title_layout = BoxLayout(size_hint_y=None, height=40, orientation='horizontal', padding=(10, 0))
    # Кнопка "Назад"
    prev_button = Button(text='<', font_size=self.title_size, color=self.current_theme['text_color'],
                         background_normal='', background_color=self.current_theme['background_color'],
                         on_press=self.prev_month)
    prev_button.widget_type = 'nextprev'
    title_layout.add_widget(prev_button)

    # Название месяца
    self.month_label = Label(text=self.current_date.strftime('%B %Y'), size_hint_x=None, width=250,
                             color=self.current_theme['text_color'], font_size=self.title_size, font_name=self.current_font)
    self.month_label.widget_type = 'header'
    title_layout.add_widget(self.month_label)

    # Кнопка "Вперед"
    next_button = Button(text='>', font_size=self.title_size, color=self.current_theme['text_color'],
                         background_normal='', background_color=self.current_theme['background_color'],
                         on_press=self.next_month)
    next_button.widget_type = 'nextprev'
    title_layout.add_widget(next_button)

    main_layout.add_widget(title_layout)

    # Дни недели
    days_layout = GridLayout(cols=7, size_hint_y=None, height=30)
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        one_day = Label(text=day, color=self.current_theme['text_color'],
                        font_name = self.current_font, font_size=16)
        one_day.widget_type = 'calendar'
        days_layout.add_widget(one_day)
    main_layout.add_widget(days_layout)

    # Сетка дней месяца
    self.days_layout = GridLayout(cols=7, spacing=5, size_hint_y=None)
    self.days_layout.bind(minimum_height=self.days_layout.setter('height'))
    main_layout.add_widget(self.days_layout)
    self.load_days_for_month()

    # Блок для надписи и кнопки "ОК"
    self.reminder_controls_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=5)
    self.reminder_controls_layout.opacity = 0
    self.reminder_label = Label(text="Выберите даты", color=self.current_theme['text_color'],
                                size_hint_y=None, height=30, font_name="font1.ttf", font_size=22)
    self.reminder_controls_layout.add_widget(self.reminder_label)

    self.ok_dates_button = Button(text="ОК", background_normal='', background_color='green',
                                  size_hint_y=None, size_hint_x=None, height=40, width=80)
    self.ok_dates_button.bind(on_press=self.proceed_to_time_popup)
    ok_button_wrapper = BoxLayout(size_hint_y=None, height=40)
    ok_button_wrapper.add_widget(Widget())
    ok_button_wrapper.add_widget(self.ok_dates_button)
    ok_button_wrapper.add_widget(Widget())

    self.reminder_controls_layout.add_widget(ok_button_wrapper)

    self.cancel_dates_button = Button(text="Отмена", background_normal='', background_color='gray',
                                      size_hint_y=None, size_hint_x=None, height=40, width=80)
    self.cancel_dates_button.bind(on_press=self.cancel_reminder_date_selection)

    cancel_button_wrapper = BoxLayout(size_hint_y=None, height=40)
    cancel_button_wrapper.add_widget(Widget())
    cancel_button_wrapper.add_widget(self.cancel_dates_button)
    cancel_button_wrapper.add_widget(Widget())
    self.reminder_controls_layout.add_widget(cancel_button_wrapper)

    main_layout.add_widget(self.reminder_controls_layout)

    main_layout.add_widget(Widget())

    # Кнопка "Добавить напоминание"
    self.add_reminder_button = Button(text="Добавить напоминание", color='white',
                                      background_normal='', background_color='green',
                                      size_hint_y=None, height=40)
    self.add_reminder_button.bind(on_press=self.handle_add_reminder)
    self.add_reminder_button.widget_type = 'calendar'
    main_layout.add_widget(self.add_reminder_button)

    birthday_buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)

    self.add_birthday_button = Button(text="Добавить ДР", color='white',
                                      background_normal='', background_color='green')
    self.add_birthday_button.bind(on_press=self.select_birthday_date)
    self.add_birthday_button.widget_type = 'calendar'

    self.delete_birthday_button = Button(text="Удалить ДР", color='white',
                                         background_normal='', background_color='red')
    self.delete_birthday_button.bind(on_press=self.select_birthday_date_for_delete)
    self.delete_birthday_button.widget_type = 'calendar'

    birthday_buttons_layout.add_widget(self.add_birthday_button)
    birthday_buttons_layout.add_widget(self.delete_birthday_button)

    main_layout.add_widget(birthday_buttons_layout)

    return main_layout

def load_days_for_month(self):
    self.days_layout.clear_widgets()

    today_str = datetime.today().strftime("%Y-%m-%d")
    year = self.current_date.year
    month = self.current_date.month
    month_calendar = calendar.monthcalendar(year, month)

    for week in month_calendar:
        for day in week:
            if day == 0:
                self.days_layout.add_widget(Label(text=""))
            else:
                date_str = f"{year}-{month:02}-{day:02}"
                btn = Button(text=str(day), color='black', background_normal='',
                             font_name = self.current_font, size_hint_y=None, height=40)

                if date_str in self.selected_dates:
                    btn.background_color = 'green'

                if self.reminder_mode:
                    if date_str < today_str:
                        btn.disabled = True
                        btn.background_color = (0.8, 0.8, 0.8, 1)
                    else:
                        btn.bind(on_press=lambda inst, d=date_str, b=btn: self.toggle_reminder_date(d, b))
                else:
                    btn.bind(on_press=lambda inst, d=date_str: self.open_task_list(d))

                btn.widget_type = 'calendar'
                self.days_layout.add_widget(btn)

def update_month_label(self):
    self.month_label.text = self.current_date.strftime('%B %Y')

def prev_month(self, instance):
    if self.current_date.month == 1:
        self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
    else:
        self.current_date = self.current_date.replace(month=self.current_date.month - 1)

    self.update_month_label()
    self.load_days_for_month()

def next_month(self, instance):
    if self.current_date.month == 12:
        self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
    else:
        self.current_date = self.current_date.replace(month=self.current_date.month + 1)

    self.update_month_label()
    self.load_days_for_month()

def switch_to_calendar(self):
    self.root.clear_widgets()
    self.root.add_widget(self.build_calendar())