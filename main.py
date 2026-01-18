import os
import telebot
from openai import OpenAI

# 1. Настройки (ключи берутся из секретов GitHub, их добавим позже)
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# !!! ВАЖНО: ВПИШИ СЮДА ЮЗЕРНЕЙМ ТВОЕГО КАНАЛА !!!
CHANNEL_ID = "@loldose777" 
# Например: CHANNEL_ID = "@anekdoty_test_123"

# 2. Подключение к Groq
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TG_BOT_TOKEN)

# 3. Функция генерации
def generate_joke():
    prompt = (
        "Придумай смешной, свежий анекдот на русском языке. "
        "Темы: работа, жизнь, технологии, коты, ирония. "
        "Никаких вступлений, сразу текст шутки."
    )
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 4. Запуск
if __name__ == "__main__":
    try:
        joke_text = generate_joke()
        bot.send_message(CHANNEL_ID, joke_text)
        print("Анекдот отправлен!")
    except Exception as e:
        print(f"ОШИБКА: {e}")
