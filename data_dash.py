from datetime import time
from dash.dcc.Dropdown import Dropdown

from dash.html.Div import Div
from pandas.core.indexes.base import Index
import market_fonctions
import plotly.graph_objects as go 
import pandas as pd 
import numpy as np 
import yfinance as yf 
import matplotlib.pyplot as plt 
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pprint
# from market_primary import df_exchanges
import market_fonctions

app = dash.Dash(__name__)  

df_index = pd.DataFrame(market_fonctions.request_exchange(), index = range(1,70))

dropdown_index = dcc.Dropdown(id='drop-index', options=[{'label': row["Noms"], 'value': row["Numéro mic"]} for index, row in df_index.iterrows()], value="XMEX")


app.layout = html.Div(          #mettre un id à la fin. 
                    [html.H1("Je suis le titre de la page"),
                    html.Div(
                            dropdown_index
                            ),
                    html.P(
                        id='test-value'
                    ),
                    html.P(
                        id = 'drop-second' 
                    )
                    ])

@app.callback (
    Output("test-value", "children"),
    [Input("drop-index", "value")]
)
def test(x):
    if not x:
        x = "Vous n'avez pas encore selectionné de bourse. Veuillez en choisir une dans la liste."
        return x
    name_stock_test = df_index[df_index["Numéro mic"] == x].iloc[0]["Noms"] 
    message = f"Vous avez selectionné la bourse de {name_stock_test}."
    return message

@app.callback (
    Output('drop-second', "children"),
    [Input("drop-index", "value")]
)
def stocksindes(call):
    # if not call:
    #     call = "blabalbla"
    #     return call
    df_stocks_index = pd.DataFrame(market_fonctions.request_stocks_in_index(call))
    # dico_index_stocks = market_fonctions.request_stocks_in_index(call)
    # message2 = dcc.Dropdown(id = "stocks_index", options = [{'labels': dico_index_stocks["Noms"], 'value' : dico_index_stocks["Symbole"]} for i in dico_index_stocks["Noms"]])
    message2 = dcc.Dropdown(id = "stocks_index", options = [{'label': row["Noms"], 'value': row["Symbole"]} for index, row in df_stocks_index.iterrows()])
    # message2 = call
    return message2


if __name__ == "__main__": #__name__ est une variable automatique de python (=nom du module qu'on a lancé) -> lance le fichier que si on a lancé le ficher directement (qui s'appelle main par défaut)
    app.run_server(debug=True)

    #deuxième dropdown sans option au départ -> ajouter callback (@), lire la value du premier dropdown et charger les données qu'il faut. fonction callback qui prend la fonction requests_stocks
