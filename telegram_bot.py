from common_imports import *

TELEGRAM_BOT_TOKEN = '8000838493:AAFsPmjq0hXVGIcBmkvqpZ8gTNESko8hX9M'
#TELEGRAM_CHAT_ID = ''

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Ваш chat_id: {chat_id}")

def send_telegram_message(self, text):
    #print(TELEGRAM_CHAT_ID)
    if self.TELEGRAM_CHAT_ID == '':
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": self.TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Ошибка при отправке: {e}")

def save_chat_id(self, chat_id):
    self.TELEGRAM_CHAT_ID = chat_id
    '''with open("../chat_id.txt", "w") as f:
        f.write(chat_id)'''

def show_confirmation(self, message):
    popup = Popup(
        title="Статус",
        content=Label(text=message),
        size_hint=(None, None),
        size=(350, 200)
    )
    popup.open()

def send_reminder_to_telegram(self, text):
    self.send_telegram_message(text)