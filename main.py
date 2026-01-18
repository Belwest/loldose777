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
        "Ты — мастер короткого, острого анекдота. Твоя задача: написать шутку в стиле лаконичного диалога. \n"
        "\n"
        "⚠️ СТИЛЬ И ОФОРМЛЕНИЕ:\n"
        "1. ДИАЛОГ ЧЕРЕЗ ТИРЕ: Каждая реплика должна начинаться с символа длинного тире (—).\n"
        "2. БЕЗ ФИЛЛЕРОВ: Категорически исключи фразы 'он сказал', 'она ответила', 'спросил мужик'. Текст должен быть чистым диалогом.\n"
        "3. ОБОЗНАЧЕНИЕ ГЕРОЕВ: Если нужно указать, кто говорит, пиши коротко перед тире: 'Муж:', 'Врач:', 'Гаишник:'.\n"
        "4. ГРАММАТИКА: Строго следи за родом (сказала/пошла — для женщин, сказал/пошел — для мужчин). \n"
        "5. ЭМОДЗИ: Используй строго НЕ БОЛЕЕ 4 эмодзи на весь пост. \n"
        "\n"
        "⛔️ СТРОГИЕ ЗАПРЕТЫ (ТАБУ):\n"
        "Никакой политики, власти, ПРЕЗИДЕНТОВ, СВО, армии, религии и тем, запрещенных в РФ.\n"
        "\n"
        "ФОРМАТ ОТВЕТА (HTML):\n"
        "1. <b>Кликбейтный заголовок (до 70 знаков)</b>\n"
        "2. Тело шутки (диалог через тире —).\n"
        "3. <tg-spoiler>Панчлайн (финальная фраза)</tg-spoiler>\n"
        "4. В конце 3 тематических хештега через пробел."
    )
    
    user_prompt = "Придумай смешной, короткий диалоговый анекдот на русском языке. Сразу текст без вступлений."

    try:
        print(f"Отправляю запрос в Groq (модель: {MODEL})...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=1.0
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
        clean_text = re.sub('<[^<]+?>', '', text)
        try:
            bot.send_message(channel, clean_text)
            return True
        except Exception as e2:
            print(f"❌ Критическая ошибка отправки: {e2}")
            return False

if __name__ == "__main__":
    jokes_sent = 0
    # Постим 2 анекдота
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
        exit(1)
