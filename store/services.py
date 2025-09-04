import requests
from django.conf import settings

from store.models import Laptop


def send_to_telegram(data):
    text = (
        f"📞 Новая заявка обратной связи:\n"
        f"👤 Имя: {data['full_name']}\n"
        f"💻 Ноутбук:{data['link']}$\n"
        f"📱 Телефон: {data['phone_number']}\n"
        f"📝  Сообщение: {data['description']}\n"
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


def send_to_telegram_service(data):
    text = (
        f"📞 Новая заявка на сервис:\n"
        f"👤 Имя: {data['full_name']}\n"
        f"📱 Телефон: {data['phone_number']}\n"
        f"📝  Сообщение: {data['description']}\n"
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


def send_to_telegram_callback(data):
    text = (
        f"📞 Заявка обратной связи:\n"
        f"👤 Имя: {data['full_name']}\n"
        f"📱 Телефон: {data['phone_number']}\n"
        f"📝  Сообщение: {data['description']}\n"
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


def cart_item_callback(data):
    product_lines = []
    for item in data["products"]:
        try:
            product = Laptop.objects.get(id=item["id"])
        except Laptop.DoesNotExist:
            continue
        product_lines.append(
            f"    id: {product.id}\n"
            f"    Количество: {item['quantity']}\n"
            f"    Название ноутбука: {product.name}\n"
            f"    Арктикул: {product.articles}\n"
            f"    Цена: {product.price}\n"
            f"    Цена со скидкой: {product.get_discount_price()}\n"

        )

    product_text = "\n".join(product_lines)

    message = (
        f"📱 Телефон: {data['phone_number']};\n"
        f"👤 Имя: {data['full_name']};\n"
        f"📝  Сообщение: {data.get('description', '')};\n"
        f"Ноутбук:\n{product_text}"
        f"Итоговая сумма: {data['total_sum']}\n"
    )

    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print("Telegram error:", e)