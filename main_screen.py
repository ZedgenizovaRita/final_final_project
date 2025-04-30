import ui.calendar_screen
from common_imports import *
from ui.theme_and_settings import on_theme_switch
from ui.calendar_screen import build_cal_0

def build_main_screen(self):
    self.main_layout.clear_widgets()

    theme_layout = BoxLayout(size_hint_y=None, height=40, orientation='horizontal', padding=(10, 0),
                             pos_hint={"center_x": 0.5, "top": 1.0})

    if self.current_theme == self.light_theme:
        theme_switch = Switch(active=False)
    else:
        theme_switch = Switch(active=True)
    theme_switch.bind(active=lambda instance, value: on_theme_switch(self, instance, value))
    theme_layout.add_widget(theme_switch)

    self.main_layout.add_widget(theme_layout)

    print(self.current_theme['text_color'])
    title = Label(text="Главная страница", font_size=32, size_hint=(None, None), size=(300, 60),
                  pos_hint={"center_x": 0.5, "top": 0.8}, font_name=self.current_font,
                  color=self.current_theme['text_color'])

    button_calendar = Button(text="Календарь", size_hint=(None, None), size=(200, 50),
                             pos_hint={"center_x": 0.5, "y": 0.4},
                             background_normal='', background_color=self.current_theme['button_color'])
    button_lists = Button(text="Списки", size_hint=(None, None), size=(200, 50),
                          pos_hint={"center_x": 0.5, "y": 0.3},
                          background_normal='', background_color=self.current_theme['button_color'])

    bind_button = Button(text="Привязать Telegram", size_hint=(None, None), size=(200, 50),
                         pos_hint={"center_x": 0.5, "y": 0.1},
                         background_normal='', background_color=self.current_theme['button_color'])

    def show_instructions(instance):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        instruction = Label(
            text="1. Перейдите в @max_reminder_bot\n2. Отправьте /start\n3. Введите полученный chat_id", color='white')

        self.chat_id_input = TextInput(multiline=False, hint_text="chat_id", size_hint=(1, None),
                                       height=35)

        buttons_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        ok_button = Button(text="ОК", background_color=(0.1, 0.7, 0.1, 1))
        cancel_button = Button(text="Отмена", background_color=(0.5, 0.5, 0.5, 1))

        buttons_layout.add_widget(cancel_button)
        buttons_layout.add_widget(ok_button)

        layout.add_widget(instruction)
        layout.add_widget(self.chat_id_input)
        layout.add_widget(buttons_layout)

        popup = Popup(title="Инструкция",
                      content=layout,
                      size_hint=(None, None), size=(350, 250),
                      auto_dismiss=False)

        def on_ok(instance):
            chat_id = self.chat_id_input.text.strip()

            if chat_id:
                self.save_chat_id(chat_id)

                popup.dismiss()

                self.show_confirmation("Телеграм аккаунт успешно привязан!")

            else:
                self.show_confirmation("Пожалуйста, введите правильный chat_id.")

        ok_button.bind(on_press=on_ok)
        cancel_button.bind(on_press=popup.dismiss)

        popup.open()

    button_calendar.bind(on_press=lambda instance: self.build_cal_0())
    button_lists.bind(on_press=lambda instance: self.build_lists_0())
    bind_button.bind(on_press=show_instructions)

    button_calendar.widget_type = 'const_text'
    button_lists.widget_type = 'const_text'
    bind_button.widget_type = 'const_text'

    self.main_layout.add_widget(title)
    self.main_layout.add_widget(button_calendar)
    self.main_layout.add_widget(button_lists)
    self.main_layout.add_widget(bind_button)

    return self.main_layout

def switch_to_main(self, instance):
    self.build_main_screen()