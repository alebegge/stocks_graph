import requests 
import pandas as pd
import numpy as np 
import json
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go

#setting the date
today = datetime.date.today()
last_year = datetime.date((today.year - 1), today.month, today.day)

#paramétres API 
params = {
'access_key': "b521f854398869c16a978b215ba6ba67",
'limit' : '100000',
}

def request_exchange():
    exchanges = requests.get("http://api.marketstack.com/v1/exchanges", params)
    api_response = exchanges.json() 
#intégration des valeurs
    names, acronyms, mics = [], [], [],

    for i in api_response["data"]: 
        names.append(i["name"])
        acronyms.append(i["acronym"])
        mics.append(i["mic"])

    dico = {"Noms": names, "Acronymes": acronyms, "Numéro mic": mics}
    return dico

def request_stocks_in_index(input_index):
    bel20 = requests.get(f"http://api.marketstack.com/v1/exchanges/{input_index}/tickers", params)
    bel20_response = bel20.json()
    #épurer les données et df
    #pprint.pp(bel20_response)
    stocksnames = []
    stockssymbol = []
    for x in bel20_response["data"]["tickers"]:
        stocksnames.append(x["name"])
        stockssymbol.append(x["symbol"])

    dico = {"Noms":stocksnames, "Symbole":stockssymbol}
    return dico

def request_stock(input_index, input_symbols):
    params2 = {
        'access_key': "b521f854398869c16a978b215ba6ba67",
        'limit' : '10000',
        'date_from' : f"{last_year}",
        'date_to' : f"{today}",
        'symbols' : f"{input_symbols}",
        'exchange' : f"{input_index}",
    }
    stocks = requests.get(f"http://api.marketstack.com/v1/eod", params2)
    sotcks_responds = stocks.json()

    stocksclose, stocksdate, stockslow, stockshigh, stocksopen, stocksvolume, = [],[],[],[],[],[]
    for z in sotcks_responds["data"]:
        stocksclose.append(z["close"])
        stocksdate.append(z["date"][:10])
        stockslow.append(z["low"])
        stockshigh.append(z["high"])
        stocksopen.append(z["open"])
        stocksvolume.append(z["volume"])
    dico = {"Open": stocksopen, "Close": stocksclose, "Low":stockslow, "High":stockshigh, "Volume":stocksvolume}
    return dico, stocksdate

def stock_chart(stock_symbol,x,y,style):
   plt.figure(stock_symbol)
   plt.plot(x,y,f"{style}")
   plt.title(f"Price charts of {stock_symbol}, 1y")
   plt.xlabel("Date")
   plt.locator_params(nbins=12)
   plt.ylabel("Price")
   plt.show(block = False)

# def is_empty(items):  #permet de test si un zip est vide ou pas.
#     try:
#         next(items)
#         return False
#     except StopIteration:
#         return True

def stock_chart_beautiful(df, date, symbol):
    df['MA5'] = df.Close.rolling(5).mean()
    df['MA20'] = df.Close.rolling(20).mean()

    fig = go.Figure(data = [go.Candlestick(x=date,open=df.Open,high=df.High,low=df.Low,close=df.Close),
                            go.Scatter(x=date, y=df.MA5, line=dict(color='orange', width=1), name="MA5"),
                            go.Scatter(x=date, y=df.MA20, line=dict(color='green', width=1), name="MA20")])

    fig.update_layout(title = {"text": f"Charts of \"{symbol}\" for 1year.", "y":0.9, "x":0.5,"xanchor":'center',"yanchor":'top'},
                       title_font_color="#059F75",
                       title_font_family ="Times New Roman",
                       height = 650,
                       width = 900,
                       title_font_size = 22
                    )
    fig.show()
    