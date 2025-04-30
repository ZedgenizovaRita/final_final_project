from common_imports import *

import inspect
from ui.calendar_screen import *
from ui.all_lists_screen import *
from ui.birthday_manager import *
from ui.telegram_bot import *
from ui.day_task_list import *
from ui.main_screen import *
from ui.one_list_screen import *
from ui.reminder_manager import *
from ui.task_manager import *
from ui.theme_and_settings import *
from ui.time_manager import *

pdfmetrics.registerFont(TTFont('MyFont', 'font1.ttf'))

Window.clearcolor = 'white'
Window.size = (360, 640)

TELEGRAM_BOT_TOKEN = '8000838493:AAFsPmjq0hXVGIcBmkvqpZ8gTNESko8hX9M'
TELEGRAM_CHAT_ID = ''

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Ваш chat_id: {chat_id}")

def run_telegram_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()
    application.idle()

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_telegram_bot())

class TodoApp(App):
    light_theme = {
        'background_color': [1, 1, 1, 1],  # Белый
        'text_color': [0, 0, 0, 1],  # Чёрный
        'button_color': [0.2, 0.6, 0.2, 1],  # Зеленый
    }

    dark_theme = {
        'background_color': (0.1, 0.1, 0.1, 1),  # Тёмно-серый
        'text_color': (1, 1, 1, 1),  # Белый
        'button_color': (0.6, 0.2, 0.2, 1),  # Красный
    }

    fonts = {
        "Шрифт 1": "font1.ttf",
        "Шрифт 2": "font2.ttf",
        "Шрифт 3": "font3.ttf",
        "Шрифт 4": "font4.ttf",
        "Шрифт 5": "font5.ttf",
        "Шрифт 6": "font6.ttf",
    }

    def save_all_data(self):
        data = {
            "tasks": self.tasks,
            "day_indexes": self.day_indexes,
            "current_theme": self.current_theme,
            "current_font": self.current_font,
            "font_size": self.font_size,
            "title_size": self.title_size,
            "cnt_tasks": self.cnt_tasks,
            "reminders": self.reminders,
            "lists": self.lists,
            "birthdays": self.birthdays,
            "telegram_chatid": self.TELEGRAM_CHAT_ID
        }

        with open("tasks_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_all_data(self):
        if os.path.exists("tasks_data.json"):
            with open("tasks_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)

                self.current_theme = data.get("current_theme", self.light_theme)
                self.current_font = data.get("current_font", "font1.ttf")
                self.font_size = data.get("font_size", 18)
                self.title_size = data.get("title_size", 24)
                self.cnt_tasks = data.get("cnt_tasks", {})
                self.day_indexes = data.get("day_indexes", {})
                self.tasks = data.get("tasks", [])
                self.reminders = data.get("reminders", {})
                self.lists = data.get("lists", {})
                self.birthdays = data.get("birthdays", {})
                self.TELEGRAM_CHAT_ID = data.get("telegram_chatid", '')

    def on_stop(self):
        self.save_all_data()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_theme = self.light_theme
        self.current_font = "font1.ttf"
        self.font_size = 18
        self.title_size = 24
        self.current_date = datetime.today()
        self.cnt_tasks = {}
        self.tasks = []
        self.day_indexes = {}
        self.reminders = {}
        self.lists = {}
        self.selected_dates = set()
        self.reminder_mode = False
        self.birthdays = {}
        self.TELEGRAM_CHAT_ID = ''

        self.load_all_data()

        print(self.current_theme)

    def build(self):
        self.load_all_data()

        self.main_layout = FloatLayout()


        first_time_check(self)
        schedule_birthday_check(self)
        build_main_screen(self)
        build_main_screen(self)

        with self.main_layout.canvas.before:
            Color(*self.current_theme['background_color'])
            self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
            self.main_layout.bind(size=self._update_rect, pos=self._update_rect)

        return self.main_layout

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def show_confirmation(self, message):
        popup = Popup(
            title="Статус",
            content=Label(text=message),
            size_hint=(None, None),
            size=(350, 200)
        )
        popup.open()

files_to_import = [
    'ui.calendar_screen',
'ui.all_lists_screen',
'ui.birthday_manager',
'ui.telegram_bot',
'ui.day_task_list',
'ui.main_screen',
'ui.one_list_screen',
'ui.reminder_manager',
'ui.task_manager',
'ui.theme_and_settings',
'ui.time_manager'
]


def bind_all_functions_to_class(class_obj):
    for file in files_to_import:
        module = __import__(file, fromlist=[''])
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj):
                setattr(class_obj, name, obj)

bind_all_functions_to_class(TodoApp)

if __name__ == "__main__":
    bot_thread = Thread(target=start_bot)
    bot_thread.start()

    TodoApp().run()
