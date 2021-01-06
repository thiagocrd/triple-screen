import pandas as pd
import yfinance as yf
import talib
from datetime import datetime, timedelta

date_today = datetime.today().strftime('%Y-%m-%d')
date_tomorrow = ( datetime.today() + timedelta(days=1) ).strftime('%Y-%m-%d')
date_one_month_ago = ( datetime.today() - timedelta(days=30) ).strftime('%Y-%m-%d')
date_three_months_ago = ( datetime.today() - timedelta(days=90) ).strftime('%Y-%m-%d')

df_ibov = pd.read_csv('ibov.csv')

# Lista com tickers dos papéis do IBOV com um '.SA' no final (é o padrão do Yahoo Finance)
stocks_list = []
for i in range(len(df_ibov)):
    stocks_list.append(df_ibov['Ticker'][i]+'.SA')

data = yf.download(stocks_list, start=date_three_months_ago, end=date_tomorrow, group_by='ticker')
df_triple_screen = pd.DataFrame()

for i in stocks_list:
    close = data[i]['Close']
    
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    
    # Verificamos quais ativos têm o histograma MACD positivo no 1D
    if (macdhist[-1] > 0):
        
        # Colocamos end com a data do dia seguinte porque assim conseguimos os preços do dia atual no timeframe horário.
        # Se colocássemos end com a data atual, teríamos os preços do último pregão.
        data_1h = yf.download(i, start=date_one_month_ago, end=date_tomorrow, interval='1h')
        data_1h = data_1h[ data_1h['Volume'] > 0 ]
        
        high = data_1h['High']
        low = data_1h['Low']
        close = data_1h['Close']
        
        # Cálculo do Estocástico no timeframe 1H
        slowk, slowd = talib.STOCH(high, low, close, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        
        # Verificamos se o estocástico está sobrevendido (<20) e incluímos o ativo com essa condição no dataframe df_triple_screen
        if (slowk[-1] < 20):
            new_row = {'Ticker':i, 'MACD_HIST':macdhist[-1], 'STOCH':slowk[-1]}
            df_triple_screen = df_triple_screen.append(new_row, ignore_index=True)

# Organizamos as colunas do df_triple_screen e ordenamos pelo valor do estocástico
df_triple_screen = df_triple_screen[['Ticker', 'MACD_HIST', 'STOCH']]
df_triple_screen.sort_values(by='STOCH', ascending=False, inplace=True)
print(df_triple_screen)