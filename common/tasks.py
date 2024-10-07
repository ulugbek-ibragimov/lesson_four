import requests
import logging

from apps.common.models import Currency
from core.celery import app


@app.task(queue='update')
def update_currency_exchange_rate():
    try:
        response = requests.get('https://cbu.uz/uz/arkhiv-kursov-valyut/json')
        response.raise_for_status()
        currencies_rate = response.json()
        for currency in currencies_rate:
            exchange_rate = 1 / float(currency['Rate'])
            Currency.objects.filter(code=currency['Ccy']).update(exchange_rate=exchange_rate)
    except Exception as e:
        logging.error(e)

    return 200


@app.task()
def update_currency_exchange_rate_clone():
    try:
        response = requests.get('https://cbu.uz/uz/arkhiv-kursov-valyut/json')
        response.raise_for_status()
        currencies_rate = response.json()
        for currency in currencies_rate:
            exchange_rate = 1 / float(currency['Rate'])
            Currency.objects.filter(code=currency['Ccy']).update(exchange_rate=exchange_rate)
    except Exception as e:
        logging.error(e)

    return 400
