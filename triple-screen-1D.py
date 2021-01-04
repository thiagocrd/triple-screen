import pandas as pd
import yfinance as yf
import talib
from datetime import datetime, timedelta

date_today = datetime.today().strftime('%Y-%m-%d')
date_two_months_ago = ( datetime.today() - timedelta(days=60) ).strftime('%Y-%m-%d')
date_sixteen_months_ago = ( datetime.today() - timedelta(days=480) ).strftime('%Y-%m-%d')

df_ibov = pd.read_csv('ibov.csv')
stocks_list = []

for i in range(len(df_ibov)):
    stocks_list.append(df_ibov['Ticker'][i]+'.SA')
    
data = yf.download(stocks_list, start=date_sixteen_months_ago, end=date_today, group_by='ticker', interval='1wk')
df_triple_screen = pd.DataFrame()

for i in stocks_list:
    close = data[i]['Close']
    close = close.dropna()
    
    last_day = close.index[-1].strftime('%Y-%m-%d')
    week_day = datetime.strptime(last_day, '%Y-%m-%d').strftime('%a')
    
    # Se a última linha for de um dia diferente de domingo, desconsideramos essa linha (na série semanal os preços ficam datados a cada domingo)
    if (week_day != 'Sun'):
        close = close[:-1]
    
    # Rodamos o algoritmo apenas para ações cujo dataframe de preços não esteja vazio (após o close.dropna(), dataframe com preços NaN ficam vazios)
    if (close.empty == False):
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)        
        
        if (macdhist[-1] > 0):
            data_1d = yf.download(i, start=date_two_months_ago, end=date_today, interval='1d')
            high = data_1d['High']
            low = data_1d['Low']
            close = data_1d['Close']
            slowk, slowd = talib.STOCH(high, low, close, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
            if (slowk[-1] < 20):
                new_row = {'Ticker':i, 'MACD_HIST':macdhist[-1], 'STOCH':slowk[-1]}
                df_triple_screen = df_triple_screen.append(new_row, ignore_index=True)

df_triple_screen = df_triple_screen[['Ticker', 'MACD_HIST', 'STOCH']]
print(df_triple_screen)