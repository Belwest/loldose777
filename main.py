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

# --- НАСТРОЙКА GOOGLE ---
genai.configure(api_key=GOOGLE_API_KEY)

def get_working_model():
    """Функция находит любую доступную модель Gemini, чтобы не было 404"""
    try:
        # Пробуем стандартную
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        # Если не вышло, ищем любую, которая умеет генерировать текст
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Использую альтернативную модель: {m.name}")
                return genai.GenerativeModel(m.name)
    return None

bot = telebot.TeleBot(TG_BOT_TOKEN)

def generate_joke():
    sys_instruction = (
        "Ты — топовый автор и редактор юмористического канала. \n"
        "Задача: Написать ОЧЕНЬ СМЕШНОЙ анекдот или шутку. \n"
        "\n"
        "⚠️ ПРАВИЛА (СТРОГО):\n"
        "1. ФОРМАТ ДИАЛОГА: Каждая реплика начинается с '— '.\n"
        "2. БЕЗ ЛИШНИХ СЛОВ: Не пиши 'он сказал', 'она ответила'. Только прямая речь.\n"
        "3. ГЕРОИ: Пиши 'Муж:', 'Жена:' перед тире, если нужно.\n"
        "4. ГРАММАТИКА: Женщина говорит в женском роде, мужчина — в мужском.\n"
        "5. ЭМОДЗИ: Максимум 4 штуки.\n"
        "6. БЕЗ МАТА.\n"
        "\n"
        "⛔️ ТАБУ: Никакой политики, СВО, армии, религии.\n"
        "\n"
        "ФОРМАТ HTML:\n"
        "1. <b>Заголовок</b>\n"
        "2. Тело шутки (через тире)\n"
        "3. <tg-spoiler>Панчлайн</tg-spoiler>\n"
        "4. 3 хештега."
    )

    try:
        model = get_working_model()
        if not model:
            return None
            
        print(f"Запрос к {model.model_name}...")
        # Объединяем инструкцию и запрос в один промпт для надежности
        full_prompt = f"{sys_instruction}\n\nЗадание: Напиши свежий смешной анекдот на русском."
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"⚠️ Ошибка генерации: {e}")
        return None

def safe_send(channel, text):
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
        except:
            return False

if __name__ == "__main__":
    jokes_sent = 0
    for i in range(2):
        print(f"--- Попытка №{i+1} ---")
        joke_text = generate_joke()
        if safe_send(CHANNEL_ID, joke_text):
            print("✅ Успех!")
            jokes_sent += 1
        
        if i == 0:
            time.sleep(10)
    
    if jokes_sent == 0:
        exit(1)
