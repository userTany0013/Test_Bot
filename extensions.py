import json
import requests
from config import keys


class APIException(Exception):
    pass

class get_price:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException('Введены одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось получить валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось получить валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать колличество {amount}')

        r = requests.get(f'https://api.getgeoapi.com/v2/currency/convert\
?api_key=484f336eca2036b8f0ac20985a100b9e36e18bff\
&from={quote_ticker}\
&to={base_ticker}\
&amount={amount}')

        meaning = json.loads(r.content)['rates'][keys[base]]['rate_for_amount']

        return meaning