from common_imports import *

def open_settings_menu(self, instance):
    main_dropdown = DropDown(auto_width=False, width=150)

    font_dropdown = DropDown(auto_width=False, width=150)
    for name, font in self.fonts.items():
        color = (0, 0, 1, 1) if font == self.current_font else (0, 0, 0, 1)

        btn = Button(text=name, size_hint=(None, None), size=(100, 50), font_name=font, font_size=20,
                     background_color=color)
        btn.bind(on_release=lambda btn_instance, f=font: self.set_font(f, font_dropdown))
        font_dropdown.add_widget(btn)

    size_dropdown = DropDown(auto_width=False, width=150)
    sizes = {"Маленький": 16, "Средний": 18, "Большой": 20}

    for name, size in sizes.items():
        color = (0, 0, 1, 1) if size == self.font_size else (0, 0, 0, 1)

        btn = Button(text=name, size_hint_y=None, height=40, background_color=color)
        btn.bind(on_release=lambda btn_instance, s=size: self.set_font_size(s, size_dropdown))
        size_dropdown.add_widget(btn)

    font_btn = Button(text="Шрифт", size_hint_y=None, height=40)
    font_btn.bind(on_release=lambda btn: font_dropdown.open(font_btn))

    size_btn = Button(text="Размер шрифта", size_hint_y=None, height=40)
    size_btn.bind(on_release=lambda btn: size_dropdown.open(size_btn))

    main_dropdown.add_widget(font_btn)
    main_dropdown.add_widget(size_btn)

    main_dropdown.open(instance)

def set_font(self, font_name, dropdown):
    self.current_font = font_name
    dropdown.dismiss()
    self.update_fonts()

def set_font_size(self, size, dropdown):
    self.font_size = size
    self.title_size = size + 6
    dropdown.dismiss()
    self.update_fonts()

def switch_theme(self, is_dark, dropdown):
    dropdown.dismiss()
    self.current_theme = self.dark_theme if is_dark else self.light_theme
    Window.clearcolor = self.current_theme['background_color']
    self.update_theme()

def update_theme(self):
    for widget in self.root.walk():
        if hasattr(widget, 'widget_type'):
            if widget.widget_type == 'nextprev':
                widget.background_color = self.current_theme['background_color']
                widget.color = self.current_theme['text_color']
                continue
            if widget.widget_type == 'calendar':
                continue
            if widget.widget_type == 'const_text':
                widget.background_color = self.current_theme['button_color']
                continue
        if isinstance(widget, Label):
            widget.color = self.current_theme['text_color']
        if isinstance(widget, Button):
            widget.background_color = self.current_theme['button_color']
        if isinstance(widget, TextInput):
            widget.background_color = self.current_theme['background_color']
            widget.foreground_color = self.current_theme['text_color']

    #self.root.background_color = self.current_theme['background_color']
    with self.main_layout.canvas.before:
        Color(*self.current_theme['background_color'])
        self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self._update_rect, pos=self._update_rect)

    if hasattr(self, 'settings_button'):
        if self.current_theme == self.dark_theme:
            self.settings_button.source = "setting_white.png"
        else:
            self.settings_button.source = "setting_black.png"

    if hasattr(self, 'back_button'):
        if self.current_theme == self.dark_theme:
            self.back_button.source = "back_white.png"
        else:
            self.back_button.source = "back_black.png"

def update_fonts(self):
    for widget in self.root.walk():
        if hasattr(widget, 'font_name'):
            widget.font_name = self.current_font
        if hasattr(widget, 'font_size'):
            if isinstance(widget, Button):
                continue
            elif hasattr(widget, 'widget_type'):
                if widget.widget_type == 'header':
                    widget.font_size = self.title_size
            else:
                widget.font_size = self.font_size

def on_theme_switch(self, switch_instance, value):
    if value:
        self.current_theme = self.dark_theme
    else:
        self.current_theme = self.light_theme

    Window.clearcolor = self.current_theme['background_color']
    self.update_theme()