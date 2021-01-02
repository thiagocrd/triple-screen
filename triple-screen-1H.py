import pandas as pd
import yfinance as yf
import talib

df_ibov = pd.read_csv('ibov.csv')
stocks_list = []

for i in range(len(df_ibov)):
    stocks_list.append(df_ibov['Ticker'][i]+'.SA')

data = yf.download(stocks_list, start='2020-09-15', end='2021-01-02', group_by='ticker')
df_triple_screen = pd.DataFrame()

for i in stocks_list:
    close = data[i]['Close']
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    if (macdhist[-1] > 0):
        data_1h = yf.download(i, start='2020-12-01', end='2021-01-02', interval='1h')
        data_1h = data_1h[ data_1h['Volume'] > 0 ]
        high = data_1h['High']
        low = data_1h['Low']
        close = data_1h['Close']
        slowk, slowd = talib.STOCH(high, low, close, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        if (slowk[-1] < 20):
            new_row = {'Ticker':i, 'MACD_HIST':macdhist[-1], 'STOCH':slowk[-1]}
            df_triple_screen = df_triple_screen.append(new_row, ignore_index=True)

df_triple_screen = df_triple_screen[['Ticker', 'MACD_HIST', 'STOCH']]
print(df_triple_screen)