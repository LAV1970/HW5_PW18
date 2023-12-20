import aiohttp
import asyncio
from datetime import datetime, timedelta


class CurrencyExchange:
    def __init__(self, api_url, max_days):
        self.api_url = api_url
        self.max_days = max_days

    async def fetch_exchange_rate(self, session, days):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days - 1)

        params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }

        try:
            url_params = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
            }
            url = f"{self.api_url}?json&start_date={url_params['start_date']}&end_date={url_params['end_date']}"

            async with session.get(url) as response:
                print(f"Запрос к API: {url}")
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
                result = []
                for day_rate in exchange_rate:
                    filtered_result = [
                        {
                            "date": day_rate["date"],
                            "baseCurrency": rate["baseCurrency"],
                            "currency": rate["currency"],
                            "sale": rate.get("saleRate", rate["saleRateNB"]),
                            "purchase": rate.get(
                                "purchaseRate", rate["purchaseRateNB"]
                            ),
                        }
                        for rate in day_rate["exchangeRate"]
                        if rate["currency"] in ["USD", "EUR"]
                    ]
                    result.extend(filtered_result)

                return result
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
