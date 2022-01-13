from pandas.core.indexes.base import Index
import requests
import json
import pprint
import pandas as pd 
import numpy as np
from requests import api
import datetime
import matplotlib.pyplot as plt

params = {
    'access_key': "b521f854398869c16a978b215ba6ba67",
    'limit' : '100000',
}

#get exchanges datas
exchanges = requests.get("http://api.marketstack.com/v1/exchanges", params)
api_response = exchanges.json()

#epuration des données + création df 
names = []
acronyms = []
mics = []
for i in api_response["data"]: 
    names.append(i["name"])
    acronyms.append(i["acronym"])
    mics.append(i["mic"])

dico = {"Noms": names, "Acronymes": acronyms, "Numéro mic": mics}

df_exchanges = pd.DataFrame(dico, index = range(1,70))
with pd.option_context("display.max_rows", None, "display.max_columns", None):
    print(df_exchanges)

#asking for the mic of the exchange
test = True
while test == True:
    exchange_mic = input("Veuillez entrer le nom de la place boursière désirée:").upper()
    if exchange_mic in mics:
        test = False
    else: 
        print(f"Le numero que vous avez introduit n'est pas correcte.")
        
name_input = df_exchanges[df_exchanges["Numéro mic"] == exchange_mic].iloc[0]["Noms"]

#get bel20 thickers 
bel20 = requests.get(f"http://api.marketstack.com/v1/exchanges/{exchange_mic}/tickers", params)
bel20_response = bel20.json()
#épurer les données et df
#pprint.pp(bel20_response)
stocksnames = []
stockssymbol = []
for x in bel20_response["data"]["tickers"]:
    stocksnames.append(x["name"])
    stockssymbol.append(x["symbol"])

dico2 = {"Noms du stock":stocksnames, "Symbole du stock":stockssymbol}
df_stocks = pd.DataFrame(dico2, index = range(len(stocksnames)))
with pd.option_context("display.max_rows", None, "display.max_columns", None):
    print(df_stocks)

#define the date 
today = datetime.date.today()
last_year = datetime.date((today.year - 1), today.month, today.day)
symbols = input(f"Entrez les symboles des stocks de la place bousière {name_input} à analyser:")

#parameter for each symbols
params2 = {
    'access_key': "b521f854398869c16a978b215ba6ba67",
    'limit' : '10000',
    'date_from' : f"{last_year}",
    'date_to' : f"{today}",
    'symbols' : f"{symbols}",
    'exchange' : f"{exchange_mic}",
}
#get stocks via symbols 
stocks = requests.get(f"http://api.marketstack.com/v1/eod", params2)
sotcks_responds = stocks.json()

# traitement des données et df
stocksclose, stocksdate, stockslow, stockshigh, stocksopen, stocksvolume, = [],[],[],[],[],[]
for z in sotcks_responds["data"]:
    stocksclose.append(z["close"])
    stocksdate.append(z["date"][:10])
    stockslow.append(z["low"])
    stockshigh.append(z["high"])
    stocksopen.append(z["open"])
    stocksvolume.append(z["volume"])
 

df_values = pd.DataFrame(zip(stocksopen, stocksclose, stockslow, stockshigh, stocksvolume), index = stocksdate,
            columns=["Open", "Close", "Low", "High", "Volume"])
print(df_values)
plt.plot(stocksdate,stocksclose, '-r')
plt.title(f"Price charts of {symbols}, 1y.")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()
