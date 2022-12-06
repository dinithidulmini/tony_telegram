import time
from binance.client import Client
from emoji import emojize
import datetime
import requests

####Invite link -
#https://t.me/+4Rtpt6WF5kUxMzc0

client = Client()

blue_circle = emojize(":blue_circle:")
red_circle = emojize(":red_circle:")
fire = emojize(":fire:")

def send_telegram_message(symbol_list):
    tg_message = f"\n=====================\nList of operational pairs {fire}\n=====================\n\n"

    for sym in symbol_list:
        tg_message += f"{sym}\n"

    telegram_bot_token = "5833178791:AAEKgZUFgFCfN0hv7coAWDY_NMXGqc3mwJk"
    channel_id = "-1001825670439"
    url = "https://api.telegram.org/bot" + telegram_bot_token + "/sendMessage?chat_id=" + channel_id + "&text=" + tg_message
    requests.get(url)


while True:
    time.sleep(117)

    symbol_list = []

    exchange_info = client.futures_exchange_info()
    symbol_details = exchange_info["symbols"]

    list_of_all_futures_symbols = []
    for symbol in symbol_details:
        if symbol["contractType"] == "PERPETUAL" and symbol["quoteAsset"] == "BUSD" and symbol["status"] == "TRADING":
            pair_name = symbol["symbol"]
            list_of_all_futures_symbols.append(pair_name)

    for symbol in list_of_all_futures_symbols:
        current_price = float(client.futures_symbol_ticker(symbol=symbol)["price"])
        print(f"Current price ({symbol}) = {current_price}")

        klines = client.futures_klines(symbol=symbol, interval="1m", limit=405)

        epoch_time = (klines[-1][0]) / 1000

        datetime_time = (datetime.datetime.fromtimestamp(epoch_time).minute) % 2

        if datetime_time == 0:
            new_klines = klines[: -1]
        else:
            new_klines = klines[: -2]

        length = len(new_klines)
        TMA_SUM = 0
        for num in range((length - 1), ((length - 1) - 40), -2):
            TMA_SUM += float(new_klines[num][4])
        TMA = TMA_SUM / 20
        print(f"20MA ({symbol})= {TMA}")

        THMA_SUM = 0
        for num in range((length - 1), ((length - 1) - 400), -2):
            THMA_SUM += float(new_klines[num][4])
        THMA = THMA_SUM / 200
        print(f"200MA ({symbol}) = {THMA}")

        if (current_price < TMA and TMA < THMA) or (current_price > TMA and TMA > THMA):
            symbol_list.append(symbol)

    send_telegram_message(symbol_list=symbol_list)




