import json
from datetime import datetime, timedelta
import aiohttp
import asyncio


async def main(days=1):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    url = "https://api.privatbank.ua/p24api/exchange_rates?json&date="
    url += start_date.strftime("%d.%m.%Y")  # Format start date as dd.mm.YYYY
    url += "&end_date="
    url += end_date.strftime("%d.%m.%Y")  # Format end date as dd.mm.YYYY

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers["content-type"])
            print("Cookies: ", response.cookies)
            print(response.ok)
            result = await response.json()

            print("API Response:", json.dumps(result, indent=2, ensure_ascii=False))

            # Check if 'exchangeRate' key is present
            if "exchangeRate" in result:
                # Фильтрация результатов только для USD и EUR
                filtered_result = [
                    {
                        rate["date"]: {
                            rate["currency"]: {
                                "sale": float(rate["sale"]),
                                "purchase": float(rate["purchase"]),
                            }
                        }
                    }
                    for rate in result["exchangeRate"]
                    if rate["currency"] in ["USD", "EUR"] and "date" in rate
                ]

                return filtered_result
            else:
                print("No 'exchangeRate' key found in the response.")
                return []


if __name__ == "__main__":
    days_to_fetch = 7  # You can change this to the desired number of days
    result = asyncio.run(main(days=days_to_fetch))
    print(json.dumps(result, indent=2, ensure_ascii=False))
