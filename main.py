def get_mem_gems():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 200,
        "page": 1,
        "sparkline": False
    }

    try:
        response = requests.get(url, params=params)
        coins = response.json()
        gems = []

        for coin in coins:
            name = coin["name"]
            symbol = coin["symbol"].upper()
            price = coin["current_price"]
            ath = coin["ath"]
            volume = coin["total_volume"]
            cap = coin["market_cap"]

            if (
                not name or not symbol or
                price <= 0 or ath <= 0 or
                cap is None or cap < 5_000_000 or
                volume is None or volume < 1_000_000 or
                price > 3 or
                any(stable in symbol for stable in ["USD", "USDT", "BUSD", "DAI", "TUSD"]) or
                any(bad in symbol for bad in ["SCAM", "PIG", "TURD", "RUG", "ASS"])
            ):
                continue

            drop_pct = (1 - price / ath) * 100
            if drop_pct < 80:
                continue

            # Фибоначчи цели
            tp1 = round(price * 1.272, 6)
            tp2 = round(price * 1.618, 6)
            tp3 = round(price * 2.0, 6)
            tp4 = round(price * 2.618, 6)

            gem = f"""🚀 Найден новый MEM-GEM!

🔸 Название: {name} ({symbol})
💲 Цена: ${price}
📉 Падение от ATH: -{drop_pct:.1f}%
📊 Объём: ${volume:,.0f}
🏷️ Цели (Fibonacci):
• TP1 (1.272): ${tp1}
• TP2 (1.618): ${tp2}
• TP3 (2.0):   ${tp3}
• TP4 (2.618): ${tp4}
🔗 https://www.coingecko.com/en/coins/{coin['id']}
"""
            gems.append(gem)

        return gems

    except Exception as e:
        print("Error in get_mem_gems:", e)
        return []
