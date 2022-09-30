

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
StartBalance = float(client.get_asset_balance(asset='USDT')['free'])
Coins = ['KNC', 'LTC', 'ETH', 'BTC']
CoinsPassports = []
Tikets = []
#MainBalanceUSD = float(client.get_asset_balance(asset='USDT')['free'])


class Indicators():
    def Fibonachi(Coin):
        #Fibo need to think about that so situative Process
        for Pass in CoinsPassports:
            if Pass['symbol'] == Coin:
                if len(Pass['prices']) > 15:
                    maxprice = max(Pass['prices'][-1:-15])
                    diff = max(Pass['prices'][-1:-15]) - min(Pass['prices'][-1:-15])
                    precent = diff / 100


                    Firstlevel = maxprice - 23.6 * precent
                    Secondlevel = maxprice - 38.2 * precent
                    Thirdlevel = maxprice - 50 * precent
                    Fourlevel = maxprice - 61.8 * precent
                    Final = maxprice
                    
            # if price > Firstlevel - 5 and price < Firstlevel + 5:

            # if price > Secondlevel - 5 and price < Secondlevel + 5:

            # if price > Thirdlevel - 5 and price < Thirdlevel + 5:
              
            # if price > Fourlevel - 5 and price < Thirdlevel + 5:
                
    def Stoch(Coin):
        for Pass in CoinsPassports:
            if Pass['symbol'] == Coin:
                if len(Pass['prices']) > 20:
                    X = 100 * (Pass['prices'][-1] - min(Pass['prices'][-1:-20:-1])) / (max(Pass['prices'][-1:-20:-1])) - min(Pass['prices'][-1:-20:-1])
                    if X < 30:
                        OrderProcesses.BuyProcess(Coin)
    def MACD(Coin):
        for Pass in CoinsPassports:
            if Pass['symbol'] == Coin:
                if len(Pass['prices']) > 26:
                    Medium26 = sum(Pass['prices'][-1:-26:-1]) / 26
                    Medium12 = sum(Pass['prices'][-1:-12:-1]) / 12
                    if Medium12 - Medium26 < 0:
                        OrderProcesses.BuyProcess(Coin)
                
    def Momentum(Coin):
        for Pass in CoinsPassports:
            if Pass['symbol'] == Coin:
                if len(Pass['prices']) > 15:
                    x = Pass['prices'][-1] / Pass['prices'][-15] * 100
                    if x < 100:
                        OrderProcesses.BuyProcess(Coin)
    def CheckRandom(Coin):
        x = random.randint(0, 100)
        if x > 90:
            OrderProcesses.BuyProcess(Coin)
        


    def RSI(Coin):
        global CoinsPassports
        for Pass in CoinsPassports:
            if Coin == Pass['symbol'] and len(Pass['prices']) > 2:
                #MainProcesses.CollectData(Pass['symbol'])
                Pass['prices'].append(price)
                if Pass['prices'][-1] < Pass['prices'][-2]:
                    Pass['summofloss'] += Pass['prices'][-1]
                elif Pass['prices'][-1] > Pass['prices'][-2]:
                    Pass['summoofincome'] += Pass['prices'][-1]
                if Pass['summofloss'] > 1 and Pass['summoofincome'] > 1:
                    RSI = 100 - (100 / 1 + Pass['summoofincome'] / Pass['summofloss'])
                    print('{} RSI is {}'.format(Coin, RSI))
                    if RSI > 70:
                        OrderProcesses.SellProcess(Coin)
                    elif RSI < 30:
                        OrderProcesses.BuyProcess(Coin)
                    print('{} RSI is {}'.format(Coin, RSI))

    def CheckMin(Coin):
        for Pass in CoinsPassports:
            if Pass['symbol'] == Coin:
                #MainProcesses.CollectData(Pass['symbol'])
                #Pass['prices'].append(price)
                if len(Pass['prices']) > 10 and Pass['prices'][-1] <= min(Pass['prices']):
                    OrderProcesses.BuyProcess(Coin)
                elif len(Pass['prices']) > 10 and Pass['prices'][-1] <= min(Pass['prices'][-1:-10:-1]):
                    OrderProcesses.BuyProcess(Coin)
                # elif len(Pass['prices']) > 10 and Pass['prices'][-1] <= min(Pass['prices'][-1:-5:-1]):
                    # OrderProcesses.BuyProcess(Coin)

    def CheckTakeProfitStopLoss(Coin):
        global Tikets
        PercentForTakeProfit = 0.4
        PercentForStopLoss = 0.6
        
        for Tiket in Tikets:
            if Tiket['symbol'] == Coin and price > Tiket['price'] + Tiket['price'] / 100 * PercentForTakeProfit and Tiket['sold'] == False:
                print("Because Take Profit price is {} price in tiket {}".format(price, Tiket['price']))
                Tiket['sold'] = True
                OrderProcesses.SellProcess(Coin)
            elif Tiket['symbol'] == Coin and price < Tiket['price'] - Tiket['price'] / 100 * PercentForStopLoss and Tiket['sold'] == False:
                print("Because Stop Loss price is {} price in tiket {}".format(price, Tiket['price']))
                Tiket['sold'] = True
                OrderProcesses.SellProcess(Coin)

    def CheckMedium(Coin):
        global Medium
        for Pass in CoinsPassports:
            if Pass['symbol'] == Coin and len(Pass['prices']) > 3:
                #MainProcesses.CollectData(Pass['symbol'])
                #Pass['prices'].append(price)
                Medium = sum(Pass['prices']) / len(Pass['prices'])
                if price >= Medium - Medium / 100 * 0.2 and price <= Medium + Medium / 100 * 0.2:
                    OrderProcesses.BuyProcess(Coin)
                

class OrderProcesses():
    def BuyProcess(Coin):
    #Buy process just Buy by name of coin and quantity that takes from CollectDataProcess
        BalanceUSDT = float(client.get_asset_balance(asset='USDT')['free'])
        print(BalanceUSDT)
        if BalanceUSDT > 10:
            try:
                order = client.create_order(
                    symbol='{}USDT'.format(Coin),
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=quantity
                )
                print('Buy {} by price {}'.format(Coin, price))
                MainProcesses.MakeTiket(Coin)
                
            except Exception as inst:
                print('Error in Buy', inst)

    def SellProcess(Coin):
        #Sell process just Sell by taking name of Coin and quantity that takes from CollectDataProcess
        BalanceOfCoin = float(client.get_asset_balance(asset=Coin)['free'])
        BalanceInUsd = price * BalanceOfCoin
        print(BalanceInUsd)
        if BalanceInUsd > 10:
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


class MainProcesses():

    def SellAll():
        for Coin in Coins:
            #MainProcesses.CollectData(Coin)
            for Tiket in Tikets:
                if Tiket['sold'] == False and Tiket['symbol'] == Coin:
                    OrderProcesses.SellProcess(Tiket['symbol'])
                    Tiket['sold'] = True
    def CheckTime():
        TimeEndProgramm = now.strftime('%a %d-%m-%Y, %H:%M:%S')
        print('Start was in {} \n End is {}', TimeStartProgram, TimeEndProgramm)

    def CheckIncome():
        EndBalance = float(client.get_asset_balance(asset='USDT')['free'])
        Income = EndBalance / StartBalance
        print('Income is - ', Income)


    def CheckTrend(Coin):
        global CoinsPassports
        for Pass in CoinsPassports:
            if Pass['symbol'] == Coin and len(Pass['prices']) > 10:
                if Pass['prices'][-1] > Pass['prices'][-10]:
                    Trend = "Up"
                elif Pass['prices'][-1] < Pass['prices'][-10]:
                    Trend = "Down"
                else:
                    Trend = "Nowhere"
                #print('{} trend is {}'.format(Coin, Trend))

    def MakeCoinsPassports(Coin):
        global CoinsPassports
        x = {
            'symbol' : Coin,
            'prices' : [],
            'summofloss' : 1,
            'summofincome' : 1,
            'trend' : ''
        }
        CoinsPassports.append(x)

    def MakeTiket(Coin):
        x = {
            'symbol' : Coin,
            'price' : price,
            'sold' : False
        }
        Tikets.append(x)

    def CollectData(Coin):
        global quantity, price
        try:

            KEY = "https://api.binance.com/api/v3/ticker/price?symbol={}USDT".format(Coin)
            data = requests.get(KEY).json()
            price = float(data['price'])
            quantity = round(PartOfBalance / price, Coins.index(Coin) + 1)
            
            for Pass in CoinsPassports:
                if Pass['symbol'] == Coin:
                    Pass['prices'].append(price)
        except Exception as inst:
            print(Exception)
            


for Coin in Coins:
        MainProcesses.MakeCoinsPassports(Coin)

M = int(input("Minutes - "))
T = int(input("Times - "))
PartOfBalance = int(input("USD for one order - "))


for i in range(T):
    for Coin in Coins:
        MainProcesses.CollectData(Coin)
        MainProcesses.CheckTrend(Coin)
        Indicators.CheckMedium(Coin)
        Indicators.CheckTakeProfitStopLoss(Coin)
        Indicators.CheckMin(Coin)
        Indicators.RSI(Coin)
        Indicators.CheckRandom(Coin)
        Indicators.MACD(Coin)
        Indicators.Momentum(Coin)
        Indicators.Stoch(Coin)

    print('Cycle ', i)
    time.sleep(M * 60)

MainProcesses.SellAll()
MainProcesses.CheckIncome()
MainProcesses.CheckTime()
