import aiohttp
import asyncio
from datetime import datetime, timedelta


class CurrencyExchange:
    def __init__(self, api_url, max_days):
        self.api_url = api_url
        self.max_days = max_days

    async def fetch_exchange_rate(self, session, days):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        params = {
            "date": end_date.strftime("%d.%m.%Y"),
            "json": "true",  # Поменял True на "true"
        }

        try:
            async with session.get(self.api_url, params=params) as response:
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
            exchange_rate = await self.fetch_exchange_rate(session, days)

        if exchange_rate:
            filtered_result = [
                {
                    rate["baseCurrency"]: {
                        rate["currency"]: {
                            "sale": rate.get("saleRate", rate["saleRateNB"]),
                            "purchase": rate.get(
                                "purchaseRate", rate["purchaseRateNB"]
                            ),
                        }
                    }
                }
                for rate in exchange_rate["exchangeRate"]
                if rate["currency"] in ["USD", "EUR"]
            ]

            return filtered_result
        else:
            return None


def main():
    api_url = "https://api.privatbank.ua/p24api/exchange_rates"
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
