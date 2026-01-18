import os
import time
import telebot
import re
import requests

# Загрузка настроек
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHANNEL_ID = os.environ.get("TG_CHANNEL_ID")

bot = telebot.TeleBot(TG_BOT_TOKEN)

def generate_joke():
    # Список эндпоинтов для проверки (Гугл капризничает с версиями)
    endpoints = [
        f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GOOGLE_API_KEY}"
    ]
    
    prompt = (
        "Напиши один очень смешной анекдот в стиле диалога на русском языке. \n\n"
        "⚠️ ПРАВИЛА:\n"
        "1. Каждая реплика начинается с '— '.\n"
        "2. БЕЗ слов автора ('сказал', 'ответила'). Только прямая речь.\n"
        "3. ГРАММАТИКА: строго следи за родом (жена сказала, муж ответил).\n"
        "4. ЭМОДЗИ: не более 4 штук.\n"
        "5. СТИЛЬ: дерзко, на грани фола, БЕЗ МАТА.\n"
        "6. ТАБУ: никакой политики, СВО, армии, религии.\n\n"
        "ФОРМАТ HTML:\n"
        "<b>Заголовок</b>\n"
        "Текст анекдота\n"
        "<tg-spoiler>Панчлайн</tg-spoiler>\n\n"
        "#юмор #анекдот #жиза"
    )

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    for url in endpoints:
        try:
            print(f"Пробую запрос к: {url.split('/models/')[1].split(':')[0]}...")
            response = requests.post(url, json=payload, timeout=30)
            data = response.json()
            
            if "candidates" in data:
                print("✅ Ответ получен!")
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"⚠️ Мимо (код {response.status_code})")
                continue
        except Exception as e:
            print(f"❌ Ошибка запроса: {e}")
            continue
            
    return None

def safe_send(text):
    if not text: return False
    try:
        bot.send_message(CHANNEL_ID, text, parse_mode="HTML")
        return True
    except Exception as e:
        print(f"Ошибка HTML: {e}. Шлю текстом.")
        clean_text = re.sub('<[^<]+?>', '', text)
        try:
            bot.send_message(CHANNEL_ID, clean_text)
            return True
        except: return False

if __name__ == "__main__":
    print("--- СТАРТ ---")
    for i in range(2):
        print(f"Попытка №{i+1}...")
        joke_text = generate_joke()
        if safe_send(joke_text):
            print("✅ Опубликовано!")
        if i == 0: time.sleep(10)
    print("--- КОНЕЦ ---")
