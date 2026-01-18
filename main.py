import os
import time
import telebot
import re
from openai import OpenAI

# --- КЛЮЧИ ИЗ СЕКРЕТОВ ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

# --- НАСТРОЙКИ КАНАЛА ---
CHANNEL_ID = "@loldose777" 

# --- ИНИЦИАЛИЗАЦИЯ ---
client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
bot = telebot.TeleBot(TG_BOT_TOKEN)

# --- МОДЕЛЬ ---
MODEL = "llama-3.3-70b-versatile"

def generate_joke():
    sys_prompt = (
        "Ты — топовый автор и редактор развлекательного Telegram-канала. \n"
        "Задача: Написать шутку, анекдот, панч, который хочется дочитать до конца. \n"
        "Стиль: Живой, дерзкий, обязательно использовать мат для усиления комичности, но не в целях злобы или оскорблений. \n"
        "\n"
        "⚠️ ПРАВИЛА КАЧЕСТВА И ЛОГИКИ:\n"
        "1. ГРАММАТИКА РОДА: Строго следи за согласованием. Если говорит женщина — используй женский род (я сказала, я пошла). Если мужчина — мужской. Не путай род персонажей!\n"
        "2. ЛОГИКА: Перед выводом проверь, чтобы финал (панчлайн) логически соответствовал началу шутки.\n"
        "3. ЭМОДЗИ: Используй не более 4 тематических эмодзи на весь текст. Не перегружай визуально.\n"
        "\n"
        "⛔️ СТРОГИЕ ЗАПРЕТЫ (ТАБУ):\n"
        "1. НИКАКОЙ ПОЛИТИКИ, ВЛАСТИ, ПРЕЗИДЕНТОВ.\n"
        "2. НЕ ТРОГАТЬ АРМИЮ, СВО, ВЕТЕРАНОВ.\n"
        "3. НЕ ТРОГАТЬ РЕЛИГИЮ И ЦЕРКОВЬ.\n"
        "4. БЕЗ ОСКОРБЛЕНИЙ НАЦИЙ.\n"
        "5. НЕ ЗАТРАГИВАЙ ТЕМЫ, ЗАПРЕЩЕННЫЕ ЗАКОНАМИ РОССИИ.\n"
        "Шути про всё (отношения, быт, секс, работа), кроме табуированных тем.\n"
        "\n"
        "ФОРМАТ ОТВЕТА (СТРОГО HTML):\n"
        "1. <b>Кликбейтный заголовок (до 70 знаков)</b>\n"
        "2. Тело анекдота/шутки.\n"
        "3. <tg-spoiler>Панчлайн (развязка)</tg-spoiler>\n"
        "4. В конце ровно 3 тематических хештега через пробел (например #юмор #жиза #лгтб)."
    )
    
    user_prompt = "Придумай смешной, свежий анекдот на русском языке. Никаких вступлений, сразу текст шутки, анекдота, панча."

    try:
        print(f"Отправляю запрос в Groq (модель: {MODEL})...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=1.1
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Ошибка API: {e}")
        return None

def safe_send(channel, text):
    """Функция безопасной отправки с защитой от кривого HTML"""
    try:
        bot.send_message(channel, text, parse_mode="HTML")
        return True
    except Exception as e:
        print(f"⚠️ Ошибка HTML разметки: {e}. Пробую отправить чистый текст.")
        # Удаляем HTML теги, если они сломаны
        clean_text = re.sub('<[^<]+?>', '', text)
        try:
            bot.send_message(channel, clean_text)
            return True
        except Exception as e2:
            print(f"❌ Критическая ошибка отправки: {e2}")
            return False

if __name__ == "__main__":
    jokes_sent = 0
    for i in range(2):
        print(f"--- Генерация шутки №{i+1} ---")
        joke_text = generate_joke()
        if joke_text:
            if safe_send(CHANNEL_ID, joke_text):
                print("✅ Успешно отправлено!")
                jokes_sent += 1
        
        if i == 0:
            print("Ждем 10 секунд перед вторым постом...")
            time.sleep(10)
    
    if jokes_sent == 0:
        print("Ни одного сообщения не отправлено.")
        exit(1)
