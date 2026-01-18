import os
import telebot
import re
import time
import google.generativeai as genai

# Загрузка секретов
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHANNEL_ID = "@loldose777"

# Проверка наличия ключей в системе
if not GOOGLE_API_KEY:
    print("ОШИБКА: Секрет GOOGLE_API_KEY не найден!")
if not TG_BOT_TOKEN:
    print("ОШИБКА: Секрет TG_BOT_TOKEN не найден!")

# Настройка
genai.configure(api_key=GOOGLE_API_KEY)
bot = telebot.TeleBot(TG_BOT_TOKEN)

def get_joke():
    # Список моделей от самой новой к старым
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    prompt = (
        "Напиши ОЧЕНЬ СМЕШНОЙ анекдот в стиле короткого диалога. \n"
        "ПРАВИЛА:\n"
        "1. Реплики начинаются с '— '.\n"
        "2. БЕЗ слов 'сказал/ответил'. Только прямая речь.\n"
        "3. Женщина говорит в женском роде, мужчина — в мужском.\n"
        "4. Максимум 4 эмодзи на весь текст.\n"
        "5. БЕЗ МАТА.\n"
        "6. ТАБУ: политика, СВО, армия, религия.\n"
        "\n"
        "ФОРМАТ HTML (ОБЯЗАТЕЛЬНО):\n"
        "<b>Заголовок</b>\n"
        "Тело анекдота\n"
        "<tg-spoiler>Панчлайн</tg-spoiler>\n"
        "#юмор #анекдот #жиза"
    )

    for m_name in models_to_try:
        try:
            print(f"Запрос к модели: {m_name}...")
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(prompt)
            
            if response and response.text:
                print(f"✅ Модель {m_name} успешно сгенерировала текст.")
                return response.text
            else:
                print(f"⚠️ Модель {m_name} вернула пустой ответ.")
        except Exception as e:
            print(f"❌ Ошибка модели {m_name}: {e}")
            continue
    return None

if __name__ == "__main__":
    print("--- СТАРТ РАБОТЫ СКРИПТА ---")
    
    for i in range(2):
        print(f"\nОбработка анекдота №{i+1}:")
        joke = get_joke()
        
        if joke:
            print(f"Текст для отправки:\n{joke[:100]}...") # Печатаем начало для проверки
            try:
                print(f"Попытка отправки в канал {CHANNEL_ID}...")
                bot.send_message(CHANNEL_ID, joke, parse_mode="HTML")
                print("✅ СООБЩЕНИЕ УСПЕШНО ОТПРАВЛЕНО В ТЕЛЕГРАМ.")
            except Exception as e:
                print(f"⚠️ Ошибка при отправке HTML: {e}")
                # Если Телеграм ругается на HTML-теги, пробуем отправить голый текст
                try:
                    print("Пробую отправить без HTML разметки...")
                    clean_joke = re.sub('<[^<]+?>', '', joke)
                    bot.send_message(CHANNEL_ID, clean_joke)
                    print("✅ ОТПРАВЛЕНО (без разметки).")
                except Exception as e2:
                    print(f"‼️ КРИТИЧЕСКАЯ ОШИБКА: Не удалось отправить даже текст: {e2}")
        else:
            print("❌ Не удалось получить текст ни от одной модели.")
        
        if i == 0:
            print("Ожидание 10 секунд перед следующей генерацией...")
            time.sleep(10)

    print("\n--- РАБОТА ЗАВЕРШЕНА ---")
