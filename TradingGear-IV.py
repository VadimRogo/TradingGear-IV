

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
Coins = ['KNC', 'LTC', 'ETH', 'BTC']
CoinsPassports = []
Tikets = []
#MainBalanceUSD = float(client.get_asset_balance(asset='USDT')['free'])
class MainProcesses():
    def MakeCoinsPassports(Coin):
        global CoinsPassports
        x = {
            'symbol' : Coin,
            'prices' : [],
            'summofloss' : 1,
            'summofincome' : 1,
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
        #Collecting data just collecting, for other functions
            global quantity, price
            #KEY_CANDLESTICK = "https://api.binance.com/api/v3/klines?symbol={}USDT&interval=1h".format(Coin)
            #klines = requests.get(KEY_CANDLESTICK).json()
            #asx = client.get_all_orders(symbol='{}USDT'.format(Coin))
            
            KEY = "https://api.binance.com/api/v3/ticker/price?symbol={}USDT".format(Coin)
            data = requests.get(KEY).json()
            price = float(data['price'])
            quantity = round(PartOfBalance / price, Coins.index(Coin) + 1)
            
            #BuyProcess(price, quantity, Coin)
            #SellProcess(price, quantity, Coin)


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

        MainProcesses.Processes(P, T)
        
    def __main__():
        global PartOfBalance
        PartOfBalance = 10
        for Coin in Coins:
            MainProcesses.CollectData(Coin)
            OrderProcesses.SellAllProcess(Coin)

        MainProcesses.Welcome()
        for Coin in Coins:
            MainProcesses.CollectData(Coin)
            OrderProcesses.SellAllProcess(Coin)
        now = datetime.now()
        TimeEndProgram = now.strftime('%a %d-%m-%Y, %H:%M:%S')
        EndBalanceUSDT = float(client.get_asset_balance(asset='USDT')['free'])
        print('Start was in {} end in {}'.format(TimeStartProgram, TimeEndProgram))
        print('Start with {} end with {}'.format(StartBalanceUSDT, EndBalanceUSDT))
        print('Income is {}'.format(EndBalanceUSDT / StartBalanceUSDT))


    def Processes(P, T):
        #Making time sleep for other functions
        for i in range(int(T / int((P / 60)))):

            for Coin in Coins:

                Indicators.CheckMinAndMax(Coin)
                Indicators.CheckMedium(Coin)
                Indicators.CheckTakeProfitStopLoss(Coin)
                
            print('Waiting - {} min'.format(T-i))
            time.sleep(P)

class OrderProcesses():

    def BuyProcess(Coin):
    #Buy process just Buy by name of coin and quantity that takes from CollectDataProcess
        BalanceUSDT = float(client.get_asset_balance(asset=Coin)['free'])
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
        global quantityprice
        #Sell all coins for trading in future by using SellProcess
        MainProcesses.CollectData(Coin)
        BalanceOfCoin = float(client.get_asset_balance(asset=Coin)['free'])
        BalanceInUSD = BalanceOfCoin * price
        while BalanceInUSD >= PartOfBalance + 2:
            BalanceOfCoin = float(client.get_asset_balance(asset=Coin)['free'])
            BalanceInUSD = BalanceOfCoin * price
            OrderProcesses.SellProcess(Coin)

class Indicators():

    def RSI(Coin):
        
        for Pass in CoinsPassports:
            if Coin == Pass['symbol'] and len(Pass['prices']) > 2:
                MainProcesses.CollectData(Coin)
                Pass['prices'].append(price)
                if Pass['prices'][-1] < Pass['prices'][-2]:
                    Pass['summofloss'] += Pass['prices'][-1]
                elif Pass['prices'][-1] > Pass['prices'][-2]:
                    Pass['summoofincome'] += Pass['prices'][-1]
                if Pass['summofloss'] > 1 and Pass['summoofincome'] > 1:
                    RSI = 100 - (100 / 1 + Pass['summoofincome'] / Pass['summofloss'])
                
                if RSI > 70:
                    print("Because RSI")
                    OrderProcesses.SellProcess(Coin)
                elif RSI < 30:
                    print("Because RSI")
                    OrderProcesses.BuyProcess(Coin)

    def CheckMinAndMax(Coin):
        for Pass in CoinsPassports:
            if Pass['symbol'] == Coin:
                Pass['prices'].append(price)
                MainProcesses.CollectData(Coin)
                # if price >= max(Pass['prices']) and len(Pass['prices']) > 5:
                #     SellProcess(Coin)
                if price <= min(Pass['prices']) and len(Pass['prices']) > 1:
                    print("Because Min")
                    OrderProcesses.BuyProcess(Coin)

    def CheckTakeProfitStopLoss(Coin):
        MainProcesses.CollectData(Coin)
        global Tikets
        PercentForTakeProfit = 0.3
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
        MainProcesses.CollectData(Coin)
        for Pass in CoinsPassports:
            if Pass['symbol'] == Coin and len(Pass['prices']) > 5:
                Medium = sum(Pass['prices']) / len(Pass['prices'])
                if price >= Medium - Medium / 100 * 0.5 and price <= Medium + Medium / 100 * 0.5:
                    print("Because Medium")
                    OrderProcesses.BuyProcess(Coin)
        


        
MainProcesses.__main__()