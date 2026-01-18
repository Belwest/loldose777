import os
import time
import telebot
import re
import requests

# Загрузка настроек из секретов GitHub
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHANNEL_ID = os.environ.get("TG_CHANNEL_ID")

bot = telebot.TeleBot(TG_BOT_TOKEN)

def generate_joke():
    # Прямой адрес API Google Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    
    prompt = (
        "Напиши один очень смешной анекдот в стиле диалога на русском языке. \n\n"
        "⚠️ ПРАВИЛА ОФОРМЛЕНИЯ:\n"
        "1. Каждая реплика начинается строго с символа '— '.\n"
        "2. БЕЗ слов автора ('сказал', 'ответила', 'спросил'). Только прямая речь.\n"
        "3. ГЕРОИ: если нужно, пиши 'Муж:', 'Врач:' перед тире.\n"
        "4. ГРАММАТИКА: строго следи за родом (жена сказала, муж ответил).\n"
        "5. ЭМОДЗИ: используй не более 4 штук на весь текст.\n"
        "6. СТИЛЬ: дерзко, на грани фола, НО БЕЗ МАТА.\n"
        "7. ТАБУ: никакой политики, СВО, армии, религии.\n\n"
        "ОБЯЗАТЕЛЬНЫЙ ФОРМАТ HTML:\n"
        "<b>Жирный заголовок-байт</b>\n"
        "Текст анекдота через тире\n"
        "<tg-spoiler>Скрытый панчлайн (финальная шутка)</tg-spoiler>\n\n"
        "#юмор #анекдот #жиза"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        print("Запрос к Google API...")
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        
        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Ошибка API: {data}")
            return None
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return None

def safe_send(text):
    if not text:
        return False
    try:
        # Пробуем отправить с HTML разметкой
        bot.send_message(CHANNEL_ID, text, parse_mode="HTML")
        return True
    except Exception as e:
        print(f"Ошибка разметки: {e}. Шлю чистый текст.")
        # Если HTML сломан, очищаем от тегов и шлем просто так
        clean_text = re.sub('<[^<]+?>', '', text)
        try:
            bot.send_message(CHANNEL_ID, clean_text)
            return True
        except Exception as e2:
            print(f"Ошибка отправки: {e2}")
            return False

if __name__ == "__main__":
    print("--- СТАРТ ---")
    for i in range(2):
        print(f"Попытка №{i+1}...")
        joke_text = generate_joke()
        if safe_send(joke_text):
            print("✅ Успешно!")
        
        if i == 0:
            time.sleep(10)
    print("--- КОНЕЦ ---")
