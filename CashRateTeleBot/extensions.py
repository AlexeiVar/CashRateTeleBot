from config import currency_list
import json
import requests


class APIException(Exception):  # Просто класс ошибки
    pass


class Converter:
    @staticmethod
    def exchange(message):
        split_message = message.text.split(" ")
        if len(split_message) > 3:  # Проверка, что аргументов не слишком много
            raise APIException("Введено слишком много параметров")
        try:  # Проверка, что достаточно аргументов
            base, quote, amount = split_message
        except ValueError:
            raise APIException("Введено недостаточно параметров")
        try:  # Проверка правильности ввода валюты
            quote_ticker = currency_list[quote]
        except KeyError:
            raise APIException(f"Неправильно введена валюта: {quote}")
        try:
            base_ticker = currency_list[base]
        except KeyError:
            raise APIException(f'Неправильно введена валюта: {base}')
        if base == quote:  # Проверка, что валюты разные
            raise APIException("Валюты одинаковы")
        try:  # Проверка, что введено число
            amount_float = float(amount)
        except ValueError:
            raise APIException("Введено не число")
        url = (f'https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_hQRwc6TXafrtYgDFfC70mKGoMYNn5gaFLjj9T7RG'
               f'&currencies={quote_ticker}&base_currency={base_ticker}')  # Делаю ссылку
        req = json.loads(requests.get(url).content)  # Отправляю и обрабатываю запрос
        course = float(str(req["data"])[8:-1])  # Получаю курс из запроса
        result = amount_float * course
        text = f"{amount} {base} в {quote} будет {result}"
        return text
