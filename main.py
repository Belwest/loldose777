import os
import telebot
import re
import time
import google.generativeai as genai

# Загрузка секретов
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHANNEL_ID = "@loldose777"

# Настройка Google
genai.configure(api_key=GOOGLE_API_KEY)
bot = telebot.TeleBot(TG_BOT_TOKEN)

def get_available_model():
    """Автоматически находит доступную модель для твоего ключа"""
    print("Проверка доступных моделей...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Нам нужны модели flash или pro
                if '1.5-flash' in m.name or '1.5-pro' in m.name or 'gemini-pro' in m.name:
                    print(f"✅ Найдена рабочая модель: {m.name}")
                    return m.name
    except Exception as e:
        print(f"❌ Не удалось получить список моделей: {e}")
    return None

def generate_joke():
    model_name = get_available_model()
    if not model_name:
        return None
    
    model = genai.GenerativeModel(model_name)
    
    prompt = (
        "Напиши один очень смешной анекдот. \n"
        "ПРАВИЛА ОФОРМЛЕНИЯ:\n"
        "1. Формат диалога: каждая реплика начинается строго с символа '— '.\n"
        "2. Категорически без слов автора ('сказал', 'ответила', 'спросил'). Только прямая речь.\n"
        "3. Строго следи за родом (если персонаж женщина — 'пошла', 'забыла').\n"
        "4. Максимум 4 эмодзи на весь текст.\n"
        "5. БЕЗ МАТА.\n"
        "6. ТАБУ: политика, СВО, армия, религия.\n"
        "\n"
        "ОБЯЗАТЕЛЬНЫЙ ФОРМАТ HTML:\n"
        "<b>Тут жирный заголовок-байт</b>\n"
        "Тут тело анекдота диалогом\n"
        "<tg-spoiler>Тут скрытая развязка (панчлайн)</tg-spoiler>\n"
        "\n"
        "#юмор #анекдот #жиза"
    )

    try:
        print(f"Запрашиваю генерацию у {model_name}...")
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
    except Exception as e:
        print(f"❌ Ошибка генерации: {e}")
    return None

if __name__ == "__main__":
    print("--- ЗАПУСК СКРИПТА ---")
    
    for i in range(2):
        print(f"\nАнекдот №{i+1}:")
        joke = generate_joke()
        
        if joke:
            try:
                bot.send_message(CHANNEL_ID, joke, parse_mode="HTML")
                print("✅ ОТПРАВЛЕНО В ТЕЛЕГРАМ")
            except Exception as e:
                print(f"⚠️ Ошибка HTML разметки: {e}. Шлю текстом...")
                clean_joke = re.sub('<[^<]+?>', '', joke)
                try:
                    bot.send_message(CHANNEL_ID, clean_joke)
                    print("✅ ОТПРАВЛЕНО (без разметки)")
                except Exception as e2:
                    print(f"‼️ ОШИБКА ОТПРАВКИ: {e2}")
        else:
            print("❌ Не удалось получить анекдот.")
        
        if i == 0:
            print("Пауза 10 секунд...")
            time.sleep(10)

    print("\n--- КОНЕЦ ---")
