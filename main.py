import os
import telebot
from openai import OpenAI

# Настройки
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
CHANNEL_ID = "@ВАШ_КАНАЛ"  # <--- ВАЖНО: ЗАМЕНИТЕ НА АДРЕС ВАШЕГО КАНАЛА (например @my_fun_channel)

client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TG_BOT_TOKEN)

def get_joke():
    prompt = "Расскажи смешной, современный анекдот на русском языке. Без вступлений, сразу текст."
    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat.choices[0].message.content

if __name__ == "__main__":
    try:
        joke = get_joke()
        bot.send_message(CHANNEL_ID, joke)
        print("Успех!")
    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1) # Чтобы GitHub понял, что была ошибка
