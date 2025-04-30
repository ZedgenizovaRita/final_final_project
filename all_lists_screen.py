from common_imports import *
from ui.telegram_bot import send_telegram_message
from ui.one_list_screen import send_list_to_telegram

def build_lists_0(self):
    self.main_layout.clear_widgets()

    lists = self.build_lists()
    self.main_layout.add_widget(lists)

def build_lists(self):
    self.main_layout.clear_widgets()

    layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

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
    layout.add_widget(header_layout)

    # Заголовок
    title_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)

    title = MyLabel(
        text="   Списки:",
        font_size=self.title_size,
        color=self.current_theme['text_color'],
        font_name=self.current_font,
        size_hint_x=1,
        valign='middle',
        halign='left'
    )
    title.text_size = (None, 60)
    title.widget_type = 'title'

    send_button = ImageButton(source="telegram.png", size_hint=(None, None), size=(40, 40))
    send_button.pos_hint = {"center_y": 0.5}
    send_button.bind(on_press=lambda instance: self.send_all_lists_to_telegram())

    title_layout.add_widget(title)
    title_layout.add_widget(send_button)

    layout.add_widget(title_layout)

    for name in self.lists:
        row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        list_button = Button(
            text=name,
            size_hint_x=0.85,
            background_color='white',
            color=self.current_theme['text_color'],
            background_normal='',
            font_name=self.current_font,
            font_size=self.font_size
        )
        list_button.widget_type = 'nextprev'
        list_button.bind(on_press=lambda inst, d=name: self.open_one_list(d))

        delete_button = ImageButton(source="delete.png", size_hint=(None, None), size=(50, 50))
        delete_button.bind(on_press=lambda inst, d=name: self.delete_list(d))

        row_layout.add_widget(list_button)
        row_layout.add_widget(delete_button)

        layout.add_widget(row_layout)

    add_button = Button(text="+ Добавить список", size_hint_y=None, height=50,
                        background_normal='',
                        background_color=self.current_theme['button_color'], color=(1, 1, 1, 1))
    add_button.bind(on_press=self.add_new_list)
    add_button.widget_type = 'const_text'

    layout.add_widget(Widget())

    layout.add_widget(add_button)

    return layout

def add_new_list(self, instance):
    content = BoxLayout(orientation='vertical', spacing=10, padding=10)

    input_label = Label(text="Введите название списка:")
    input_field = TextInput(multiline=False, size_hint=(1, None), height=30)

    buttons_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
    ok_button = Button(text="ОК", background_color=(0.1, 0.7, 0.1, 1))
    cancel_button = Button(text="Отмена", background_color=(0.5, 0.5, 0.5, 1))

    buttons_layout.add_widget(cancel_button)
    buttons_layout.add_widget(ok_button)

    content.add_widget(input_label)
    content.add_widget(input_field)
    content.add_widget(buttons_layout)

    popup = Popup(title="Новый список", content=content,
                  size_hint=(None, None), size=(300, 200), auto_dismiss=False)

    cancel_button.bind(on_press=popup.dismiss)

    def on_ok(instance):
        new_name = input_field.text.strip()
        if new_name:
            self.lists[new_name] = True
            popup.dismiss()
            self.switch_to_lists()

    ok_button.bind(on_press=on_ok)

    popup.open()

def delete_list(self, list_name):
    del self.lists[list_name]
    self.switch_to_lists()

def switch_to_lists(self):
    self.root.clear_widgets()
    self.root.add_widget(self.build_lists())

def send_all_lists_to_telegram(self):
    for list_name in self.lists:
        self.send_list_to_telegram(list_name)
        '''tasks = self.tasks.get(list_name, [])
        message = f"📋 *{list_name}*"

        message += "\n"
        ind = 0
        if tasks:
            for text, done in tasks:
                ind += 1
                checkbox = "✅" if done else "🔲"
                message += f"\n{ind}\n{checkbox} {text}"
        else:
            message += "\n(пусто)"

        send_telegram_message(message)'''