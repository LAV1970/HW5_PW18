import aiohttp
import asyncio
from datetime import datetime, timedelta


class CurrencyExchange:
    def __init__(self, api_url, max_days):
        self.api_url = api_url
        self.max_days = max_days

    async def fetch_exchange_rate(self, session, start_date, end_date):
        params = {
            "json": "",
            "date": "",
            "start_date": start_date.strftime("%d.%m.%Y"),
            "end_date": end_date.strftime("%d.%m.%Y"),
        }

        try:
            async with session.get(self.api_url, params=params) as response:
                print(f"Запрос к API: {response.url}")
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    print(f"Ошибка при запросе к API. Статус код: {response.status}")
                    print(f"Текст ошибки: {error_text}")
                    return None
        except aiohttp.ClientError as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    async def get_exchange_rates(self, days):
        async with aiohttp.ClientSession() as session:
            end_date = datetime.now()
            result = []

            for i in range(days):
                start_date = end_date - timedelta(days=i)
                exchange_rate = await self.fetch_exchange_rate(
                    session, start_date, end_date
                )

                if exchange_rate:
                    # Выводим структуру ответа перед обращением к 'date'
                    print(exchange_rate)

                    day_rate = exchange_rate[
                        0
                    ]  # Предполагаем, что ответ содержит только один элемент
                    filtered_result = [
                        {
                            "date": day_rate.get("date"),
                            "baseCurrency": day_rate.get("base_ccy"),
                            "currency": day_rate.get("ccy"),
                            "sale": day_rate.get("sale"),
                            "purchase": day_rate.get("buy"),
                        }
                    ]
                    result.extend(filtered_result)

            return result if result else None


def main():
    api_url = "https://api.privatbank.ua/p24api/pubinfo"
    max_days = 10

    try:
        days = int(
            input(
                f"Введите количество дней для получения курсов валют (до {max_days}): "
            )
        )
        if days > max_days:
            raise ValueError(
                f"Ошибка: Вы можете запрашивать курсы обмена только на {max_days} дней вперёд"
            )

        currency_exchange = CurrencyExchange(api_url, max_days)
        exchange_rate = asyncio.run(currency_exchange.get_exchange_rates(days))

        if exchange_rate:
            print(exchange_rate)
        else:
            print("Ошибка при получении данных.")

    except ValueError as ve:
        print(f"Ошибка: {ve}")


if __name__ == "__main__":
    main()
