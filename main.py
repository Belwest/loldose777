import os
import time
import telebot
import re
import google.generativeai as genai

# --- КЛЮЧИ ИЗ СЕКРЕТОВ ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

# --- НАСТРОЙКИ ---
CHANNEL_ID = "@loldose777" 

# --- ИНИЦИАЛИЗАЦИЯ GEMINI ---
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TG_BOT_TOKEN)

def generate_joke():
    prompt = (
        "Ты — топовый автор и редактор юмористического канала. \n"
        "Задача: Написать ОЧЕНЬ СМЕШНОЙ анекдот или шутку. \n"
        "\n"
        "⚠️ ПРАВИЛА ОФОРМЛЕНИЯ И ЛОГИКИ (СТРОГО):\n"
        "1. ФОРМАТ ДИАЛОГА: Каждая реплика ДОЛЖНА начинаться с длинного тире (— ).\n"
        "2. БЕЗ АВТОРСКОГО ТЕКСТА: Запрещены фразы 'он сказал', 'она ответила', 'спросил врач'. Только прямая речь персонажей.\n"
        "3. ГЕРОИ: Если нужно обозначить кто говорит, пиши коротко перед тире: 'Муж:', 'Врач:', 'Жена:'.\n"
        "4. ГРАММАТИКА РОДА: Строго следи, чтобы женщина говорила о себе в женском роде (я пошла, я сказала), а мужчина — в мужском.\n"
        "5. ЭМОДЗИ: Используй не более 4 эмодзи на весь текст.\n"
        "6. СТИЛЬ: Живой, дерзкий, на грани фола, НО БЕЗ МАТА.\n"
        "\n"
        "⛔️ СТРОЖАЙШИЕ ТАБУ:\n"
        "НИКАКОЙ ПОЛИТИКИ, ВЛАСТИ, ПРЕЗИДЕНТОВ, АРМИИ, СВО, РЕЛИГИИ И ТЕМ, ЗАПРЕЩЕННЫХ В РФ.\n"
        "\n"
        "ФОРМАТ ВЫДАЧИ (HTML РАЗМЕТКА):\n"
        "1. Первая строка: <b>Жирный заголовок-байт</b>\n"
        "2. Тело анекдота (диалог через тире).\n"
        "3. Панчлайн (финал) должен быть скрыт тегом: <tg-spoiler>Текст развязки</tg-spoiler>\n"
        "4. В конце ровно 3 хештега через пробел."
    )

    try:
        print("Запрос к Google Gemini...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"⚠️ Ошибка Gemini: {e}")
        return None

def safe_send(channel, text):
    """Отправка с защитой от ошибок разметки"""
    if not text: return False
    try:
        bot.send_message(channel, text, parse_mode="HTML")
        return True
    except Exception as e:
        print(f"⚠️ Ошибка разметки: {e}. Шлю чистый текст.")
        clean_text = re.sub('<[^<]+?>', '', text)
        try:
            bot.send_message(channel, clean_text)
            return True
        except Exception as e2:
            print(f"❌ Ошибка отправки: {e2}")
            return False

if __name__ == "__main__":
    jokes_sent = 0
    for i in range(2):
        print(f"--- Генерация №{i+1} ---")
        joke_text = generate_joke()
        if safe_send(CHANNEL_ID, joke_text):
            print("✅ Готово!")
            jokes_sent += 1
        
        if i == 0:
            time.sleep(10)
    
    if jokes_sent == 0:
        exit(1)
