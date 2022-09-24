from logging.handlers import RotatingFileHandler
from statistics import quantiles



import requests
import matplotlib.pyplot as plt
import json, time, math, random
from binance.spot import Spot
from binance.client import Client
from datetime import datetime

from Keys import KEY, SECRET

client = Client(KEY, SECRET)

Coins = ['ETH', 'BTC', 'LTC', 'KNC', 'DOGE']

def MakeQuantity(Coin, price):
    if Coin == 'DOGE':
        quantity = round(10.5 / price)
    elif Coin == 'KNC':
        quantity = round(10.5 / price, 1)
    elif Coin == 'LTC':
        quantity = round(10.5 / price, 3)
    elif Coin == 'ETH':
        quantity = round(10.5 / price, 4)
    else:    
        quantity = round(10.5 / price, 5)
    return quantity
    

def CollectData():
        MainBalanceUSD = float(client.get_asset_balance(asset='USDT')['free'])
        for Coin in Coins:
            KEY = "https://api.binance.com/api/v3/ticker/price?symbol={}USDT".format(Coin)
            KEY_CANDLESTICK = "https://api.binance.com/api/v3/klines?symbol={}USDT&interval=1h".format(Coin)
            data = requests.get(KEY).json()
            klines = requests.get(KEY_CANDLESTICK).json()
            price = float(data['price'])
            quantity = MakeQuantity(Coin, price)
            BalanceOfCoin = float(client.get_asset_balance(asset=Coin)['free'])

            #BuyProcess(price, quantity, Coin)
            #SellProcess(price, quantity, Coin)

            asx = client.get_all_orders(symbol='{}USDT'.format(Coin))
            print(klines[1][1])
            #print('Price of {} is {}, quantity will be {}'.format(Coin, price, quantity))
            # print(asx)
def BuyProcess(quantity, Coin):
        try:
            order = client.create_order(
                symbol='{}USDT'.format(Coin),
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        except Exception as inst:
            print(inst)

def SellProcess(quantity, Coin):
    try:
        order = client.create_order(
            symbol='{}USDT'.format(Coin),
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity = quantity
        )
        print('All fine')
    except Exception as inst:
        print(inst)



CollectData()