import json
import requests
import pandas as pd
from datetime import date
from numpy import where
import data_processing as dp
import global_variables as gv

url_stocks = 'https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2E/CS/0032E4ECNV0.px'
sector = ['0', '1', '2', '3']
quers = dp.queries(['Sector', sector],
                ['Year', gv.year_stock],
                ['Month', gv.month])
response_stock = dp.request_data(url_stocks, quers, gv.check_list, 'stocks')

rice_stocks = pd.json_normalize(
    response_stock.json(), record_path=['data']
)

key_split = pd.DataFrame(rice_stocks['key'].to_list(), index=rice_stocks.index)
key_split.columns = ['sector', 'year', 'month']

convert_month = {'0': '01', '1': '02', '2': '03', '3': '04', '4': '05', '5': '06',
                '6': '07', '7': '08', '8': '09', '9': '10', '10': '11', '11': '12'}
key_split['month'] = key_split['month'].map(convert_month)

key_split['date'] = key_split['year'].str.cat(key_split['month'], sep='-')
key_split = key_split.drop(columns=['year', 'month'])

stocks = pd.DataFrame(rice_stocks['values'].to_list(), index=rice_stocks.index)
stocks.columns = ['stocks']

key_split = key_split.merge(stocks, on=key_split.index, how='left')
key_split = key_split.drop(columns=['key_0'])

key_split.drop(key_split[key_split['stocks'] == '..'].index, inplace=True)

stock = key_split.query("sector == '0'")
stock.rename(columns={'stocks': 'total_stock'}, inplace=True)
stock = stock.drop(columns=['sector'])

household_stock = key_split.query("sector == '1'")
household_stock.rename(columns={'stocks': 'stock_household'}, inplace=True)
household_stock = household_stock.drop(columns=['sector'])
stock = stock.merge(household_stock, how='inner', on='date')

commercial_stock = key_split.query("sector == '2'")
commercial_stock.rename(columns={'stocks': 'stock_commercial'}, inplace=True)
commercial_stock = commercial_stock.drop(columns=['sector'])
stock = stock.merge(commercial_stock, how='inner', on='date')

nfa_stock = key_split.query("sector == '3'")
nfa_stock.rename(columns={'stocks': 'stock_nfa'}, inplace=True)
nfa_stock = nfa_stock.drop(columns=['sector'])
stock = stock.merge(nfa_stock, how='inner', on='date')
