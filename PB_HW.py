import aiohttp
import asyncio


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def main(days):
    if days > 10:
        print("Error: You can request exchange rates for up to 10 days only.")
        return

    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date="
    tasks = [fetch(f"{url}{i}") for i in range(days, 0, -1)]

    try:
        responses = await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    filtered_result = []

    for response in responses:
        if "exchangeRate" in response:
            rates = response["exchangeRate"]
            filtered_rates = {}

            for rate in rates:
                if rate["currency"] in ["USD", "EUR"]:
                    currency_code = rate["currency"]
                    filtered_rates[currency_code] = {
                        "sale": rate["saleRateNB"],
                        "purchase": rate["purchaseRateNB"],
                    }

            if filtered_rates:
                date_key = response.get("date", "Unknown Date")
                filtered_result.append({date_key: filtered_rates})

    if not filtered_result:
        print("No data found in the response.")
        return

    print(filtered_result)


if __name__ == "__main__":
    try:
        days_to_fetch = int(
            input("Enter the number of days for exchange rates (up to 10): ")
        )
    except ValueError:
        print("Error: Please enter a valid number.")
    else:
        asyncio.run(main(days_to_fetch))
