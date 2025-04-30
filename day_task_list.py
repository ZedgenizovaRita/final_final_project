from common_imports import *
from ui.telegram_bot import send_telegram_message
from functools import partial
from kivy.graphics import Color, Rectangle

def open_task_list(self, date_str):
    self.root.clear_widgets()

    self.current_date = datetime.strptime(date_str, "%Y-%m-%d")

    main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    header_layout = BoxLayout(size_hint_y=None, height=40, orientation='horizontal', padding=(10, 0))

    if self.current_theme == self.light_theme:
        self.back_button = ImageButton(source="back_black.png", size_hint=(None, None), size=(32, 32))
    else:
        self.back_button = ImageButton(source="back_white.png", size_hint=(None, None), size=(32, 32))
    self.back_button.bind(on_press=lambda x: self.switch_to_calendar())
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

    task_header_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)

    header_task = MyLabel(text=f"Список дел на {date_str}",
                          font_size=self.title_size,
                          color=self.current_theme['text_color'],
                          font_name=self.current_font,
                          size_hint_x=0.8,
                          valign='middle')
    header_task.widget_type = 'title'

    send_button = ImageButton(source="telegram.png", size_hint=(None, None), size=(40, 40))
    send_button.pos_hint = {"center_y": 0.5}
    send_button.bind(on_press=lambda instance: self.send_tasks_to_telegram(date_str))

    task_header_layout.add_widget(header_task)
    task_header_layout.add_widget(send_button)

    main_layout.add_widget(task_header_layout)

    # Поле ввода + кнопка добавления
    input_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
    self.task_input = TextInput(hint_text="Введите задачу...", multiline=False, font_name=self.current_font)
    add_button = Button(text="Добавить", background_normal='', size_hint_x=None, width=100,
                        font_name=self.current_font, background_color=self.current_theme['button_color'])
    add_button.bind(on_press=self.add_task_for_date)
    add_button.widget_type = 'const_text'
    input_layout.add_widget(self.task_input)
    input_layout.add_widget(add_button)
    main_layout.add_widget(input_layout)

    # Список задач
    self.tasks_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
    self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))

    scroll_view = ScrollView()
    scroll_view.add_widget(self.tasks_layout)
    main_layout.add_widget(scroll_view)

    header_rem = MyLabel(text="Напоминания:",
                         font_size=24,
                         color=self.current_theme['text_color'],
                         font_name=self.current_font,
                         size_hint_y=None,
                         height=60,
                         padding=10,
                         )
    header_rem.widget_type = 'title'
    main_layout.add_widget(header_rem)

    # Поле ввода + кнопка добавления
    input_layout_rem = BoxLayout(size_hint_y=None, height=50, spacing=10)
    self.task_input_rem = TextInput(hint_text="Введите напоминание...", multiline=False,
                                    font_name=self.current_font)
    add_button_rem = Button(text="Добавить", background_normal='', size_hint_x=None, width=100,
                            font_name=self.current_font, background_color=self.current_theme['button_color'])
    add_button_rem.bind(on_press=self.add_rem_for_date)
    add_button_rem.widget_type = 'const_text'
    input_layout_rem.add_widget(self.task_input_rem)
    input_layout_rem.add_widget(add_button_rem)
    main_layout.add_widget(input_layout_rem)

    self.reminders_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
    self.reminders_layout.bind(minimum_height=self.reminders_layout.setter('height'))

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    date_str_without_year = dt.strftime("%d.%m")

    if date_str_without_year in self.birthdays:
        names = ""
        for name in self.birthdays[date_str_without_year]:
            if len(names) > 0:
                names += ", "
            names += name

        birthday_label = Label(text=f"Сегодня День рождения у {names}",
                               size_hint_y=None, height=30,
                               color=(1, 0, 0, 1), font_size=18)
        main_layout.add_widget(birthday_label)

    scroll_view_r = ScrollView()
    scroll_view_r.add_widget(self.reminders_layout)
    main_layout.add_widget(scroll_view_r)

    # Кнопка экспорта в PDF
    pdf_button = Button(text="Преобразовать в PDF", background_normal='', size_hint_y=None, height=50,
                        background_color=self.current_theme['button_color'], font_name=self.current_font)
    pdf_button.bind(on_press=lambda instance: self.export_to_pdf(date_str))
    pdf_button.widget_type = 'const_text'
    main_layout.add_widget(pdf_button)

    self.root.add_widget(main_layout)

    self.load_tasks_for_date(date_str)
    self.load_reminders_for_date(date_str)

def load_tasks_for_date(self, date_str):
    self.tasks_layout.clear_widgets()
    if date_str in self.day_indexes:
        for idx in self.day_indexes[date_str]:
            make_add(self, date_str, idx, 0)

def make_add(self, date_str, idx, depth):
    text, done, ost, subtasks, opens = self.tasks[idx]

    if not ost:
        return

    task_layout = BoxLayout(size_hint_y=None, height=40, spacing=10, padding=(10*depth, 0, 0, 0))

    checkbox = CheckBox(active=done, size_hint_x=None, width=40)
    checkbox.bind(active=lambda cd, val, i=idx: self.toggle_task_done(i, val, date_str))

    label = Label(text=text, halign="left", valign="middle", markup=done,
                  color=self.current_theme['text_color'], font_name=self.current_font,
                  font_size=self.font_size)
    label.bind(size=label.setter('text_size'))

    def on_label_touch(instance, touch, i=idx):
        if instance.collide_point(*touch.pos):
            if not checkbox.collide_point(*touch.pos):
                self.select_subtask_input(i, date_str)
                return True
        return False

    label.bind(on_touch_down=on_label_touch)

    open_sub_button = ImageButton(source="sub.png", size_hint=(None, None), size=(20, 20))
    open_sub_button.bind(on_press=lambda btn, i=idx: self.open_sub(i, date_str))

    delete_button = ImageButton(source="delete.png", size_hint=(None, None), size=(50, 50))
    delete_button.bind(on_press=lambda btn, i=idx: self.delete_task(i, date_str))

    task_layout.add_widget(checkbox)
    task_layout.add_widget(label)
    task_layout.add_widget(open_sub_button)
    task_layout.add_widget(delete_button)
    self.tasks_layout.add_widget(task_layout)

    if opens:
        for idx2 in subtasks:
            make_add(self, date_str, idx2, depth + 1)

def select_subtask_input(self, idx, date_str):
    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    date_label = Label(text="Введите подзадачу:")
    self.subtask_input = TextInput(multiline=False, hint_text="...", size_hint=(1, None),
                                         height=30)

    buttons_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
    ok_button = Button(text="ОК", background_color=(0.1, 0.7, 0.1, 1))
    cancel_button = Button(text="Отмена", background_color=(0.5, 0.5, 0.5, 1))

    buttons_layout.add_widget(cancel_button)
    buttons_layout.add_widget(ok_button)

    layout.add_widget(date_label)
    layout.add_widget(self.subtask_input)
    layout.add_widget(buttons_layout)

    popup = Popup(title="Добавить подзадачу",
                  content=layout,
                  size_hint=(None, None), size=(350, 250),
                  auto_dismiss=False)

    def save_subtask(instance):
        text = self.subtask_input.text.strip()
        if text:
            new_idx = len(self.tasks)
            self.tasks.append([text, False, True, [], True])
            self.tasks[idx][3].append(new_idx)
            popup.dismiss()
            self.load_tasks_for_date(date_str)

    ok_button.bind(on_press=save_subtask)
    cancel_button.bind(on_press=popup.dismiss)
    popup.open()

def load_reminders_for_date(self, date_str):
    self.reminders_layout.clear_widgets()

    if date_str in self.reminders and self.reminders[date_str]:
        self.reminders[date_str].sort(key=lambda r: [int(x) for x in r['time'].split(':')])
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')

        for index, reminder in enumerate(self.reminders[date_str]):
            rem_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)

            has_passed = not ((date_str > current_date or (
                    date_str == current_date and reminder['time'] > current_time.strftime('%H:%M'))))

            rem_color = self.current_theme['text_color']

            if has_passed:
                rem_color = [rem_color[0], rem_color[1], rem_color[2], 0.5]
            else:
                rem_color = [rem_color[0], rem_color[1], rem_color[2], 1]

            reminder_text = f"{reminder['time']} — {reminder['text']}"
            reminder_label = Label(text=reminder_text, halign="left", valign="middle",
                                   color=rem_color, font_size=self.font_size,
                                   font_name=self.current_font)
            reminder_label.bind(size=reminder_label.setter('text_size'))

            rem_layout.add_widget(reminder_label)

            if not has_passed:
                delete_button = ImageButton(source="delete.png", size_hint=(None, None), size=(50, 50))
                delete_button.bind(
                    on_press=lambda btn, d=date_str, i=index, rl=rem_layout: self.delete_reminder(d, i, rl))
                rem_layout.add_widget(delete_button)

            self.reminders_layout.add_widget(rem_layout)

def pdf_one_task(self, c, idx, pos, depth, y):
    width, height = A4
    text, done, ost, subtasks, opens = self.tasks[idx]

    if not ost:
        return y

    c.rect(50 + 20 * depth, y - 4, 10, 10)

    if done:
        c.drawString(52 + 20 * depth, y - 2, "✓")

    c.drawString(70 + 20 * depth, y, f"{text}")
    y -= 25

    if y < 50:
        c.showPage()
        y = height - 50

    pos2 = 0
    for idx2 in subtasks:
        y = self.pdf_one_task(c, idx2, pos2, depth + 1, y)
        pos2 += 1
    return y

def export_to_pdf(self, date_str):
    filename = f"todo_{date_str}.pdf"
    print(filename)
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("MyFont", 14)
    c.drawString(50, height - 50, f"Список задач {date_str}:")

    y = height - 80

    indexes = self.day_indexes.get(date_str, [])

    if not indexes:
        c.drawString(70, y, "Пусто")
    else:
        pos = 0
        for idx in indexes:
            y = self.pdf_one_task(c, idx, pos, 0, y)

    c.save()
    print(f"PDF-файл сохранен как: {filename}")
    open_pdf_file(filename)

def open_pdf_file(filepath):
    system = platform.system()
    if system == 'Windows':
        os.startfile(filepath)
    elif system == 'Darwin':
        subprocess.run(['open', filepath])
    else:
        subprocess.run(['xdg-open', filepath])

def send_one_task(self, idx, pos, depth):
    text, done, ost, subtasks, opens = self.tasks[idx]

    if not ost:
        return ""
    status = "✅" if done else "🔲"
    message = "   " * depth + f"{pos + 1}. {status} {text}\n"
    pos2 = 0
    for idx2 in subtasks:
        message += self.send_one_task(idx2, pos2, depth + 1)
        pos2 += 1
    return message

def send_tasks_to_telegram(self, date_str):
    indexes = self.day_indexes.get(date_str, [])

    message = f"📝 Список дел на {date_str}:\n\n"
    if not indexes:
        message += f"На {date_str} задач нет."
    else:
        pos = 0
        for idx in indexes:
            message += self.send_one_task(idx, pos, 0)
            pos += 1

    self.send_telegram_message(message)