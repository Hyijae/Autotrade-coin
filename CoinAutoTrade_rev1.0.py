import time
import pyupbit
import datetime
import numpy as np

access = "sYmz0pwt2QdTfW1ljq7x537QDwhz0M3KwJULr4TY"
secret = "w4KxvRVXydD6QW3mLMvu7XZUEfmq6ebhfxpgK3CX"


#매수 목표가
def get_target_price(ticker):
    # 29틱 갱신
    dfh = pyupbit.get_ohlcv(ticker, interval="minute240", count=29)

    datahigh = np.array(dfh['high'])
    
    for i in range(1, len(dfh)):
        datahigh[i] = max(datahigh[i-1], dfh['high'].iloc[i])
        time.sleep(1)
    dfh['29_highest'] = datahigh

    target_price = np.array(dfh.iloc[0]['29_highest'])
    
    return target_price

#매도 목표가
def get_sell_price(ticker):
    # 17틱 갱신
    dfl = pyupbit.get_ohlcv(ticker, interval="minute240", count=17)

    datalow = np.array(dfl['low'])

    for x in range(1, len(dfl)):
        datalow[x] = min(datalow[x-1], dfl['low'].iloc[x])
        time.sleep(1)
    dfl['17_lowest'] = datalow

    sell_price = np.array(dfl.iloc[0]['17_lowest'])
    
    return sell_price

def get_start_time(ticker):
    """시작 시간 조회"""
    dft = pyupbit.get_ohlcv(ticker, interval="minute240", count=1)
    start_time = dft.index[0]
    return start_time



def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances(ticker)
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
        time.sleep(1)
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(minutes=240)    

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC")
            print(target_price)
            current_price = get_current_price("KRW-BTC")
            print(current_price)
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.49975)             
                
        else:
            btc = get_balance("BTC")
            sell_price = get_sell_price("KRW-BTC")
            print(sell_price)
            if sell_price > current_price:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)