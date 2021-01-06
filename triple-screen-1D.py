import pandas as pd
import yfinance as yf
import talib
from datetime import datetime, timedelta

date_today = datetime.today().strftime('%Y-%m-%d')
date_tomorrow = ( datetime.today() + timedelta(days=1) ).strftime('%Y-%m-%d')
date_two_months_ago = ( datetime.today() - timedelta(days=60) ).strftime('%Y-%m-%d')
date_sixteen_months_ago = ( datetime.today() - timedelta(days=480) ).strftime('%Y-%m-%d')

df_ibov = pd.read_csv('ibov.csv')

# Lista com tickers dos papéis do IBOV com um '.SA' no final (é o padrão do Yahoo Finance)
stocks_list = []
for i in range(len(df_ibov)):
    stocks_list.append(df_ibov['Ticker'][i]+'.SA')
    
data = yf.download(stocks_list, start=date_sixteen_months_ago, end=date_tomorrow, group_by='ticker', interval='1wk')
df_triple_screen = pd.DataFrame()

for i in stocks_list:
    close = data[i]['Close']
    close = close.dropna()
    
    last_day = close.index[-1].strftime('%Y-%m-%d')
    week_day = datetime.strptime(last_day, '%Y-%m-%d').strftime('%a')
    
    # Rodamos o algoritmo apenas para ações cujo dataframe de preços não esteja vazio (após o close.dropna(), dataframe com preços NaN ficam vazios)
    if (close.empty == False):

        # Cálculo do MACD no timeframe 1S
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)        
        
        # Verificamos quais ativos têm o histograma MACD positivo no 1S
        if (macdhist[-1] > 0):

            # Colocamos end com a data do dia seguinte porque assim conseguimos os preços do dia atual no timeframe diário.
            # Se colocássemos end com a data atual, teríamos os preços do último pregão.
            data_1d = yf.download(i, start=date_two_months_ago, end=date_tomorrow, interval='1d')
            high = data_1d['High']
            low = data_1d['Low']
            close = data_1d['Close']

            # Cálculo do Estocástico no timeframe 1D
            slowk, slowd = talib.STOCH(high, low, close, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

            # Verificamos se o estocástico está sobrevendido (<20) e incluímos o ativo com essa condição no dataframe df_triple_screen
            if (slowk[-1] < 20):
                new_row = {'Ticker':i, 'MACD_HIST':macdhist[-1], 'STOCH':slowk[-1]}
                df_triple_screen = df_triple_screen.append(new_row, ignore_index=True)

# Organizamos as colunas do df_triple_screen e ordenamos pelo valor do estocástico
df_triple_screen = df_triple_screen[['Ticker', 'MACD_HIST', 'STOCH']]
df_triple_screen.sort_values(by='STOCH', ascending=False, inplace=True)
print(df_triple_screen)