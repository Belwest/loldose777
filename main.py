import os
import requests
import telebot
import re
import time

# Данные
G_KEY = os.environ.get("GOOGLE_API_KEY")
T_TOKEN = os.environ.get("TG_BOT_TOKEN")
CH_ID = os.environ.get("TG_CHANNEL_ID")

bot = telebot.TeleBot(T_TOKEN)

def get_joke():
    # 1. УЗНАЕМ, КАКИЕ МОДЕЛИ ДОСТУПНЫ
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={G_KEY}"
    try:
        models_data = requests.get(list_url).json()
        if 'error' in models_data:
            print(f"❌ Ошибка ключа: {models_data['error']['message']}")
            return None
            
        # Ищем любую модель, которая умеет генерировать контент
        valid_models = [m['name'] for m in models_data.get('models', []) 
                        if 'generateContent' in m.get('supportedGenerationMethods', [])]
        
        if not valid_models:
            print("❌ Нет доступных моделей для этого ключа.")
            return None

        # Выбираем Flash (она быстрее) или первую попавшуюся
        target_model = next((m for m in valid_models if "flash" in m), valid_models[0])
        print(f"✅ Нашел рабочую модель: {target_model}")
        
    except Exception as e:
        print(f"❌ Ошибка при поиске моделей: {e}")
        return None

    # 2. ГЕНЕРИРУЕМ АНЕКДОТ
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={G_KEY}"
    
    prompt = (
        "Напиши один очень смешной анекдот диалогом на русском языке. \n"
        "ПРАВИЛА: 1. Реплики начинаются с '— '. 2. БЕЗ слов 'сказал/ответил'. "
        "3. Женщина говорит в женском роде, мужчина в мужском. 4. Макс 4 эмодзи. 5. БЕЗ МАТА. "
        "6. ТАБУ: политика, СВО, армия, религия. \n"
        "ФОРМАТ HTML: <b>Заголовок</b>\nТело\n<tg-spoiler>Панчлайн</tg-spoiler>\n#юмор #анекдот #жиза"
    )

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        res = requests.post(gen_url, json=payload, timeout=30).json()
        return res['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"❌ Ошибка генерации у {target_model}: {e}")
        return None

if __name__ == "__main__":
    print("--- СТАРТ ПОИСКА ---")
    for i in range(2):
        print(f"Попытка №{i+1}...")
        text = get_joke()
        if text:
            try:
                bot.send_message(CH_ID, text, parse_mode="HTML")
                print("✅ ОТПРАВЛЕНО")
            except:
                bot.send_message(CH_ID, re.sub('<[^<]+?>', '', text))
                print("✅ ОТПРАВЛЕНО (без разметки)")
        if i == 0: time.sleep(10)
    print("--- КОНЕЦ ---")
