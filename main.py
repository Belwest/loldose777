import os
import time
import random
import requests
from openai import OpenAI

# --- КЛЮЧИ ИЗ СЕКРЕТОВ ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHANNEL_ID = os.environ.get("TG_CHANNEL_ID")

# --- КЛИЕНТ ДЛЯ GROQ ---
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# --- НОВАЯ, 100% РАБОЧАЯ МОДЕЛЬ ---
MODEL = "gemma-7b-it"

def get_joke():
    sys_prompt = (
        "Ты — топовый автор развлекательного Telegram-канала. \n"
        "Задача: Написать АНЕКДОТ, который хочется дочитать до конца. \n"
        "Стиль: Живой, дерзкий,  не использовать мат. \n"
        "\n"
        "⛔️ СТРОГИЕ ЗАПРЕТЫ (ТАБУ):\n"
        "1. НИКАКОЙ ПОЛИТИКИ, ВЛАСТИ, ПРЕЗИДЕНТОВ.\n"
        "2. НЕ ТРОГАТЬ АРМИЮ, СВО, ВЕТЕРАНОВ.\n"
        "3. НЕ ТРОГАТЬ РЕЛИГИЮ И ЦЕРКОВЬ.\n"
        "4. БЕЗ ОСКОРБЛЕНИЙ НАЦИЙ.\n"
        "5. НЕ ЗАТРАГИВАЙ ТЕМЫ, ЗАПРЕЩЕННЫЕ ЗАКОНАМИ РОССИИ.\n"
        "Шути про всё, кроме табуированных тем.\n"
        "\n"
        "ФОРМАТ ОТВЕТА (HTML):\n"
        "1. <b>Кликбейтный заголовок (до 70 знаков)</b>\n"
        "2. Текст анекдота (с эмодзи 🌚🔥).\n"
        "3. <tg-spoiler>Панчлайн (развязка)</tg-spoiler>\n"
        "4. Три хештега (например #юмор #жиза)."
    )
    user_prompt = "Расскажи свежий, убойный анекдот."

    try:
        print(f"Отправляю запрос в Groq (модель: {MODEL})...")
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}],
            temperature=1.1, 
            timeout=30.0
        )
        print("Получил ответ от Groq.")
        return completion.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Ошибка при запросе к Groq: {e}")
        return None

def send_telegram(text):
    if not text: return
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = { "chat_id": TG_CHANNEL_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True }
    try:
        print("Отправляю сообщение в Телеграм...")
        response = requests.post(url, json=payload, timeout=15)
        print(f"Телеграм ответил со статусом: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Полный ответ от Телеграма: {response.text}")
    except Exception as e:
        print(f"❌ Не удалось отправить в Телеграм: {e}")

if __name__ == "__main__":
    jokes_generated = 0
    for i in range(2):
        print(f"--- Анекдот №{i+1} ---")
        joke = get_joke()
        if joke:
            send_telegram(joke)
            jokes_generated += 1
        else:
            print("❌ Модель не сгенерировала анекдот.")
        if i == 0:
            time.sleep(5)
    if jokes_generated == 0:
        print("КРИТИЧЕСКАЯ ОШИБКА: Ни одного анекдота не сгенерировано. Завершаю с ошибкой.")
        exit(1)
