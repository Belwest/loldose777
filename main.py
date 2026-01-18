import os
import telebot
import re
import time
import google.generativeai as genai

# Загрузка секретов
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHANNEL_ID = "@loldose777"

# Настройка
genai.configure(api_key=GOOGLE_API_KEY)
bot = telebot.TeleBot(TG_BOT_TOKEN)

def generate_joke():
    # ИСПОЛЬЗУЕМ FLASH - она 100% бесплатная и доступная
    model = genai.GenerativeModel('gemini-1.5-flash')
    
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
        "<b>Заголовок-байт</b>\n"
        "Текст анекдота\n"
        "<tg-spoiler>Панчлайн</tg-spoiler>\n"
        "\n"
        "#юмор #анекдот #жиза"
    )

    try:
        print("Запрашиваю анекдот у Gemini 1.5 Flash...")
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
    except Exception as e:
        print(f"❌ Ошибка генерации: {e}")
    return None

if __name__ == "__main__":
    print("--- СТАРТ ---")
    
    for i in range(2):
        print(f"Попытка №{i+1}...")
        joke = generate_joke()
        
        if joke:
            try:
                bot.send_message(CHANNEL_ID, joke, parse_mode="HTML")
                print("✅ ОТПРАВЛЕНО")
            except Exception as e:
                print(f"⚠️ Ошибка HTML: {e}. Шлю текстом.")
                clean_joke = re.sub('<[^<]+?>', '', joke)
                bot.send_message(CHANNEL_ID, clean_joke)
        else:
            print("❌ Не удалось получить текст.")
        
        if i == 0:
            time.sleep(10)

    print("--- КОНЕЦ ---")
