import aiohttp
import asyncio
from datetime import datetime, timedelta


class CurrencyExchange:
    def __init__(self, api_url, max_days):
        self.api_url = api_url
        self.max_days = max_days

    async def fetch_exchange_rate(self, session, date):
        params = {
            "json": "",
            "date": "",
            "start_date": date.strftime("%d.%m.%Y"),
            "end_date": date.strftime("%d.%m.%Y"),
        }

        try:
            async with session.get(self.api_url, params=params) as response:
                # print(f"Запрос к API: {response.url}")
                if response.status == 200:
                    day_rate = await response.json()
                    if day_rate:
                        date_entry = {
                            date.strftime("%d.%m.%Y"): {
                                rate["ccy"]: {
                                    "sale": rate["sale"],
                                    "purchase": rate["buy"],
                                }
                                for rate in day_rate
                            }
                        }
                        return date_entry
                    else:
                        print(
                            f"Пустой ответ от API для дня {date.strftime('%d.%m.%Y')}"
                        )
                else:
                    error_text = await response.text()
                    print(f"Ошибка при запросе к API. Статус код: {response.status}")
                    print(f"Текст ошибки: {error_text}")
        except aiohttp.ClientError as e:
            print(f"Ошибка при выполнении запроса: {e}")

    async def get_exchange_rates(self, days):
        async with aiohttp.ClientSession() as session:
            result = []

            for i in range(days):
                end_date = datetime.now() - timedelta(days=i)
                result.append(await self.fetch_exchange_rate(session, end_date))

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
