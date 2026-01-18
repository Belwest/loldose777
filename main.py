import os, telebot, re, time, google.generativeai as genai

# Конфигурация
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
bot = telebot.TeleBot(os.environ.get("TG_BOT_TOKEN"))

def get_joke():
    # Пробуем разные варианты названий моделей для обхода ошибки 404
    for m_name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(m_name)
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
                "ФОРМАТ HTML:\n"
                "<b>Заголовок</b>\n"
                "Тело анекдота\n"
                "<tg-spoiler>Панчлайн</tg-spoiler>\n"
                "#юмор #анекдот #жиза"
            )
            response = model.generate_content(prompt)
            return response.text
        except:
            continue
    return None

if __name__ == "__main__":
    for i in range(2):
        joke = get_joke()
        if joke:
            try:
                bot.send_message("@loldose777", joke, parse_mode="HTML")
            except:
                # Если ошибка в HTML, отправляем без тегов
                bot.send_message("@loldose777", re.sub('<[^<]+?>', '', joke))
        if i == 0:
            time.sleep(10)
