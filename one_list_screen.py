from common_imports import *
from ui.telegram_bot import send_telegram_message
from ui.day_task_list import make_add, send_one_task

def open_one_list(self, name):
    self.root.clear_widgets()

    main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    header_layout = BoxLayout(size_hint_y=None, height=40, orientation='horizontal', padding=(10, 0))

    if self.current_theme == self.light_theme:
        self.back_button = ImageButton(source="back_black.png", size_hint=(None, None), size=(32, 32))
    else:
        self.back_button = ImageButton(source="back_white.png", size_hint=(None, None), size=(32, 32))
    self.back_button.bind(on_press=lambda x: self.switch_to_lists())

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

    header_task = MyLabel(text=name,
                          font_size=self.title_size,
                          color=self.current_theme['text_color'],
                          font_name=self.current_font,
                          size_hint_x=0.8,
                          valign='middle')
    header_task.widget_type = 'title'

    send_button = ImageButton(source="telegram.png", size_hint=(None, None), size=(40, 40))
    send_button.pos_hint = {"center_y": 0.5}
    send_button.bind(on_press=lambda instance: self.send_list_to_telegram(name))

    task_header_layout.add_widget(header_task)
    task_header_layout.add_widget(send_button)

    main_layout.add_widget(task_header_layout)

    # Поле ввода + кнопка добавления
    input_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
    self.task_input = TextInput(hint_text="Введите задачу...", multiline=False, font_name=self.current_font)
    add_button = Button(text="Добавить", background_normal='', size_hint_x=None, width=100,
                        font_name=self.current_font, background_color=self.current_theme['button_color'])
    add_button.bind(on_press=lambda instance: self.add_task_for_list(name))
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

    # Кнопка экспорта в PDF
    pdf_button = Button(text="Преобразовать в PDF", background_normal='', size_hint_y=None, height=50,
                        background_color=self.current_theme['button_color'], font_name=self.current_font)
    pdf_button.bind(on_press=lambda instance: self.export_to_pdf(name))
    pdf_button.widget_type = 'const_text'
    main_layout.add_widget(pdf_button)

    self.root.add_widget(main_layout)

    self.load_tasks_for_list(name)

def load_tasks_for_list(self, name):
    self.tasks_layout.clear_widgets()
    if name in self.day_indexes:
        for idx in self.day_indexes[name]:
            make_add(self, name, idx, 0)

def send_list_to_telegram(self, name):
    indexes = self.day_indexes.get(name, [])

    message = f"📝 Список {name}:\n\n"
    if not indexes:
        message += f"В {name} задач нет."
    else:
        pos = 0
        for idx in indexes:
            message += self.send_one_task(idx, pos, 0)
            pos += 1

    self.send_telegram_message(message)