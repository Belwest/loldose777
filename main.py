import os
import time
import telebot
import re
import requests

# --- КЛЮЧИ ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHANNEL_ID = "@loldose777"

bot = telebot.TeleBot(TG_BOT_TOKEN)

def generate_joke():
    # Прямой URL к API Google (версия v1 - самая стабильная)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    
    prompt = (
        "Напиши один очень смешной анекдот диалогом на русском. \n"
        "ПРАВИЛА:\n"
        "1. Каждая реплика начинается с '— '.\n"
        "2. БЕЗ слов автора ('сказал', 'ответила'). Только прямая речь.\n"
        "3. Женщина говорит в женском роде, мужчина — в мужском.\n"
        "4. Максимум 4 эмодзи.\n"
        "5. БЕЗ МАТА.\n"
        "6. ТАБУ: политика, СВО, армия, религия.\n"
        "\n"
        "ФОРМАТ HTML:\n"
        "<b>Заголовок</b>\n"
        "Текст анекдота\n"
        "<tg-spoiler>Панчлайн</tg-spoiler>\n"
        "\n"
        "#юмор #анекдот #жиза"
    )

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        print("Отправляю прямой запрос в Google API...")
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        
        if "candidates" in data:
            joke_text = data["candidates"][0]["content"]["parts"][0]["text"]
            return joke_text
        else:
            print(f"❌ Ошибка API: {data}")
            return None
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")
        return None

if __name__ == "__main__":
    print("--- СТАРТ ---")
    
    for i in range(2):
        print(f"Попытка №{i+1}...")
        joke = generate_joke()
        
        if joke:
            try:
                bot.send_message(CHANNEL_ID, joke, parse_mode="HTML")
                print("✅ ОТПРАВЛЕНО В ТЕЛЕГРАМ")
            except Exception as e:
                print(f"⚠️ Ошибка HTML: {e}. Шлю чистым текстом.")
                clean_joke = re.sub('<[^<]+?>', '', joke)
                bot.send_message(CHANNEL_ID, clean_joke)
        else:
            print("❌ Не удалось получить ответ от Google.")
        
        if i == 0:
            print("Ждем 10 секунд...")
            time.sleep(10)

    print("--- КОНЕЦ ---")
