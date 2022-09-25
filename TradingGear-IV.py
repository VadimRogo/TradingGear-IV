

from audioop import minmax
import requests
import matplotlib.pyplot as plt
import json, time, math, random
from binance.spot import Spot
from binance.client import Client
from datetime import date, datetime

from Keys import KEY, SECRET

client = Client(KEY, SECRET)
now = datetime.now()
TimeStartProgram = now.strftime('%a %d-%m-%Y, %H:%M:%S')
StartBalanceUSDT = float(client.get_asset_balance(asset='USDT')['free'])
Periods = ['1m', '5m', '10m']
Times = [60, 350, 600]
Coins = ['DOGE', 'KNC', 'LTC', 'ETH', 'BTC']
CoinsPassports = []
#MainBalanceUSD = float(client.get_asset_balance(asset='USDT')['free'])

def MakeCoinsPassports(Coin):
    global CoinsPassports
    x = {
        'symbol' : Coin,
        'prices' : []
    }
    CoinsPassports.append(x)


def CollectData(Coin):
    #Collecting data just collecting, for other functions
        global quantity, price
        #KEY_CANDLESTICK = "https://api.binance.com/api/v3/klines?symbol={}USDT&interval=1h".format(Coin)
        #klines = requests.get(KEY_CANDLESTICK).json()
        #asx = client.get_all_orders(symbol='{}USDT'.format(Coin))
        
        KEY = "https://api.binance.com/api/v3/ticker/price?symbol={}USDT".format(Coin)
        data = requests.get(KEY).json()
        price = float(data['price'])
        quantity = round(PartOfBalance / price, Coins.index(Coin))
        
        #BuyProcess(price, quantity, Coin)
        #SellProcess(price, quantity, Coin)

def CheckMinAndMax(Coin):
    CollectData(Coin)
    for Pass in CoinsPassports:
        if Pass['symbol'] == Coin:
            Pass['prices'].append(price)
            if price >= max(Pass['prices']) and len(Pass['prices']) > 5:
                SellProcess(Coin)
            if price <= min(Pass['prices']) and len(Pass['prices']) > 5:
                BuyProcess(quantity, Coin)

        
def BuyProcess(quantity, Coin):
    #Buy process just Buy by name of coin and quantity that takes from CollectDataProcess
        BalanceUSDT = float(client.get_asset_balance(asset=Coin)['free'])
        if BalanceUSDT >= PartOfBalance:
            try:
                order = client.create_order(
                    symbol='{}USDT'.format(Coin),
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=quantity
                )
                print('Buy {} by price {}'.format(Coin, price))
            except Exception as inst:
                print('Error in Buy', inst)

def SellProcess(Coin):
    #Sell process just Sell by taking name of Coin and quantity that takes from CollectDataProcess
    BalanceOfCoin = float(client.get_asset_balance(asset=Coin)['free'])
    BalanceInUsd = price * BalanceOfCoin
    if BalanceInUsd >= PartOfBalance:
        try:
            order = client.create_order(
                symbol='{}USDT'.format(Coin),
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity = quantity
            )
            print('Sell {} by price {}'.format(Coin, price))
        except Exception as inst:
            print(Coin, quantity, price, BalanceInUsd)
            print('Error in Sell ', inst)

def SellAllProcess(Coin):
    global quantity
    #Sell all coins for trading in future by using SellProcess
    CollectData(Coin)
    BalanceOfCoin = float(client.get_asset_balance(asset=Coin)['free'])
    BalanceInUSD = BalanceOfCoin * price
    while BalanceInUSD >= PartOfBalance + 2:
        BalanceOfCoin = float(client.get_asset_balance(asset=Coin)['free'])
        BalanceInUSD = BalanceOfCoin * price
        SellProcess(Coin)

def Processes(P, T):
    #Making time sleep for other functions
    for i in range(int(T / int((P / 60)))):

        for Coin in Coins:

            CheckMinAndMax(Coin)
            
        print('Waiting - {} min'.format(T-i))
        time.sleep(P)

def Welcome():
    global PartOfBalance
    #Welcome for user and take information from him
    print('Welcome, thanks for using my soft')
    print('Time start -', TimeStartProgram)
    P = input('What period using? ')
    T = int(input('How much time in minutes? '))
    PartOfBalance = int(input('How much you wanna take for one order? '))
    if P in Periods:
        P = Times[Periods.index(P)]

    Processes(P, T)
    
def __main__():
    global PartOfBalance
    PartOfBalance = 10
    for Coin in Coins:
        CollectData(Coin)
        MakeCoinsPassports(Coin)
        SellAllProcess(Coin)

    Welcome()
    for Coin in Coins:
        CollectData(Coin)
        SellAllProcess(Coin)
    now = datetime.now()
    TimeEndProgram = now.strftime('%a %d-%m-%Y, %H:%M:%S')
    EndBalanceUSDT = float(client.get_asset_balance(asset='USDT')['free'])
    print('Start was in {} end in {}'.format(TimeStartProgram, TimeEndProgram))
    print('Start with {} end with {}'.format(StartBalanceUSDT, EndBalanceUSDT))
    print('Income is {}'.format(EndBalanceUSDT / StartBalanceUSDT))


        
__main__()