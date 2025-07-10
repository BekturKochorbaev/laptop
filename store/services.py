import requests
from django.conf import settings


def send_to_telegram(data):
    laptop = data['laptop']
    text = (
        f"📞 Новая заявка обратной связи:\n"
        f"👤 Имя: {data['full_name']}\n"
        f"💻 Ноутбук: {laptop.name} — {laptop.cpu_model} — {laptop.ram_size_gb}ГБ — {laptop.price}$\n"
        f"📱 Телефон: {data['phone_number']}\n"
        f"📝  Сообщение: {data['description']}\n"
        f"📩 Email: {data['email'] or '—'}"
    )
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print("Telegram error:", e)