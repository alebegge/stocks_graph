from pandas.core.indexes.base import Index
import pprint
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import market_fonctions
import os
from pathlib import Path
import datetime

path = Path(__file__).parent

value_index = market_fonctions.request_exchange()

#df of all markets indexs
df_exchanges = pd.DataFrame(value_index, index = range(1,70))
with pd.option_context("display.max_rows", None, "display.max_columns", None):
    print(df_exchanges)

# Input index value needed. 
test = True
while test == True:
    exchange_mic = input("Veuillez entrer le nom de la place boursière désirée:").upper()
    if exchange_mic in value_index["Numéro mic"]:
        test = False
    else: 
        print(f"Le numero que vous avez introduit n'est pas correcte.")
        
#request all stocks in the index and print a df 
value_index_stock = market_fonctions.request_stocks_in_index(exchange_mic)
df_stocks = pd.DataFrame(value_index_stock, index = range(1,len(value_index_stock["Noms"])+1))
with pd.option_context("display.max_rows", None, "display.max_columns", None):
    print(df_stocks)

#asking for symbols to user 
name_input = df_exchanges[df_exchanges["Numéro mic"] == exchange_mic].iloc[0]["Noms"]

boucle2 = True
while boucle2:
    test2 = True
    while test2:
        symbols = input(f"Entrez les symboles des stocks de la place bousière {name_input} à analyser:").upper()
        if symbols in value_index_stock["Symbole"]:
            test2 = False
        else:
            print(f"Le symbole du stock n'est pas correcte.")
        
    #request stock_value and print a df 
    value_stocks,stocksdate = market_fonctions.request_stock(exchange_mic, symbols)
    name_stock_test = df_stocks[df_stocks["Symbole"] == symbols].iloc[0]["Noms"] #.loc[0, "Noms"]
    
    if not value_stocks["Open"]:
        print(f"Il n'existe pas de données pour {name_stock_test}.")
        news_input_stock = input("Voulez-vous chercher un autre stock (1)? (Y/N):").upper()
        if news_input_stock == "Y" or news_input_stock == "YES":
            boucle2 = True
        else:
            boucle2 = False
        # boucle2 = news_input_stock == "Y" or news_input_stock =="YES" (permet de remplacer le if/esle car si respecté = true)
    else:
        df_values = pd.DataFrame(value_stocks, index = stocksdate)
        print(df_values)
        #chart imprint 
        # market_fonctions.stock_chart(symbols,stocksdate, df_values["Close"], "-g" )
        market_fonctions.stock_chart_beautiful(df_values, stocksdate, name_stock_test)
        input_stock_csv = input("Voulez-vous exporter les données en CSV ?(Y/N)").upper()
        if input_stock_csv == "Y" or input_stock_csv == "YES":
            try:
                os.mkdir(path/f"{datetime.date.today()}")
                df_values.to_csv(Path(path,f"{datetime.date.today()}",f"{symbols}.csv"))
            except FileExistsError:
                df_values.to_csv(Path(path,f"{datetime.date.today()}",f"{symbols}.csv"))
        news_input_stock = input("Voulez-vous chercher un autre stock ? (Y/N):").upper()
        if news_input_stock == "Y" or news_input_stock == "YES":
            boucle2 = True
        else:
            boucle2 = False
plt.show()