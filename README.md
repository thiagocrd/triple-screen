# triple-screen
Scanner de ações do IBOV que satisfazem os requisitos do Triple Screen para a ponta compradora (MACD Histograma positivo na referência longa e Estocástico <20 na referência intermediária).

Para saber mais sobre o Triple Screen, consulte o post [Sistema Triple Screen](https://leiturasdotrader.com/sistema-triple-screen/)

**ATENÇÃO: este código não oferece sinal de compra; é apenas um filtro de oportunidades potencialmente interessantes de acordo com o método desenvolvido pelo Dr. Alexander Elder; o usuário deve fazer a própria análise para julgar se vale a pena uma entrada ou não; se julgar que vale abrir a operação, cabe ao usuário definir em que momento/circunstância/contexto a entrada vai ocorrer.**

## Sobre os arquivos
- **ibov.csv**: lista com os papéis do Índice Bovespa (a tabela atualizada está disponível no [site da B3](http://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm))
- **triple-screen-1H.py**: código para scannear oportunidades com o gráfico horário (1H) como referência intermediária e o gráfico diário (1D) como referência longa
- **triple-screen-1D.py**: código para scannear oportunidades com o gráfico diário (1D) como referência intermediária e o gráfico semanal como referência longa

## Dependências necessárias
- [pandas](https://pandas.pydata.org/)
- [yfinance](https://pypi.org/project/yfinance/)
- [TA-Lib](http://mrjbq7.github.io/ta-lib/index.html)
