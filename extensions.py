import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class MoneyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            moneyInTicker = keys[base.lower()]
        except KeyError:
            raise ConvertionException(f'К сожалению у нас нет валюты {base} для расчетов.')

        try:
            moneyOutTicker = keys[quote.lower()]
        except KeyError:
            raise ConvertionException(f'К сожалению у нас нет валюты {quote.lower()} для расчетов.')

        if (base.lower() == quote.lower()):
            raise ConvertionException(f'Нельзя указывать одинаковые валюты для расчета {base.lower()} и {quote.lower()}.')

        try:
            moneyAmount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не верно указана сумма валюты {amount}.')

        moneyInTicker, moneyOutTicker = keys[base.lower()], keys[quote.lower()]
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={moneyInTicker}&tsyms={moneyOutTicker}')
        return float(json.loads(r.content)[keys[quote.lower()]]) * moneyAmount
