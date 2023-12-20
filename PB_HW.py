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
            result_text = await response.text()
            print("API Response:", result_text)

            result = await response.json()

            # Check if 'exchangeRate' key is present
            if "exchangeRate" in result:
                # Фильтрация результатов только для USD и EUR
                filtered_result = [
                    {
                        rate["baseCurrency"]: {
                            rate["currency"]: {
                                "sale": float(
                                    rate.get("saleRateNB", rate.get("saleRate", 0))
                                ),
                                "purchase": float(
                                    rate.get(
                                        "purchaseRateNB", rate.get("purchaseRate", 0)
                                    )
                                ),
                            }
                        }
                    }
                    for rate in result["exchangeRate"]
                    if rate["currency"] in ["USD", "EUR"]
                ]

                return filtered_result
            else:
                print("No data found in the response.")
                return []


if __name__ == "__main__":
    days_to_fetch = 7  # You can change this to the desired number of days
    result = asyncio.run(main(days=days_to_fetch))
    print(json.dumps(result, indent=2, ensure_ascii=False))
