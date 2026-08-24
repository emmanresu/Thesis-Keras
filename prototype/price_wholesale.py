import json
import requests
import pandas as pd
from datetime import date
from numpy import where
import data_processing as dp
import global_variables as gv

''' STAGE 1 WHOLESALE PRICE QUERY (2000 - 2009) '''
url_ws_price_1 = 'https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/WS/0012M4AWP01.px'
commodity = ['2', '3']
quers = dp.queries(['Region province', ['00']],
                       ['Commodity', ['2', '3']],
                       ['Year', gv.year_part1],
                       ['Month', gv.month])
response_ws_price1 = dp.request_data(url_ws_price_1, quers, gv.check_list, 'wsprice1')

wsprice_1 = pd.json_normalize(
    response_ws_price1.json(), record_path=["data"]
)
key_split = pd.DataFrame(wsprice_1['key'].to_list(), index=wsprice_1.index)
key_split.columns = ['province', 'commodity', 'year', 'month']

key_split["commodity"] = where(key_split["commodity"] == '2', 'milled', 'regular')

convert_yr = {'10': '2000', '11': '2001', '12': '2002', '13': '2003', '14': '2004', '15': '2005',
              '16': '2006', '17': '2007', '18': '2008', '19': '2009', '20': '2010'}
key_split['year'] = key_split['year'].map(convert_yr)

convert_mnt = {'0': '01', '1': '02', '2': '03', '3': '04', '4': '05', '5': '06',
                '6': '07', '7': '08', '8': '09', '9': '10', '10': '11', '11': '12'}
key_split['month'] = key_split['month'].map(convert_mnt)

key_split["province"] = key_split["year"].str.cat(key_split["month"], sep='-')
key_split = key_split.rename(columns={'province': 'date'})
key_split = key_split.drop(columns=['year', 'month'])

price = pd.DataFrame(wsprice_1['values'].to_list(), index=wsprice_1.index)
price.columns = ['price']
key_split = key_split.merge(price, on=key_split.index, how='left')
key_split = key_split.drop(columns=['key_0'])

wholesale = key_split.query("commodity == 'regular'")
wholesale.rename(columns={'price': 'regular_wholesale_price'}, inplace=True)
wholesale = wholesale.drop(columns=['commodity'])
wholesale_temp = key_split.query("commodity == 'milled'")
wholesale_temp.rename(columns={'price': 'milled_wholesale_price'}, inplace=True)
wholesale_temp = wholesale_temp.drop(columns=['commodity'])

wholesale = wholesale.merge(wholesale_temp, how='inner', on='date')


''' STAGE 2 WHOLESALE PRICE QUERY (2010 - CURRENT YEAR) '''
url_ws_price_2 = ''
commodity = ['2', '3']
quers = dp.queries(['Geolocation', ['0'],
                       ['Commodity', commodity],
                       ['Year', gv.year_part2],
                       ['Period', gv.month]])
response_ws_price2 = dp.request_data(url_ws_price_2, quers, gv.check_list, 'wsprice2')

wsprice_2 = pd.json_normalize(
    response_ws_price2.json(), record_path=["data"]
)

key_split = pd.DataFrame(wsprice_2['key'].to_list(), index=wsprice_2.index)
key_split.columns = ['province', 'commodity', 'year', 'month']
key_split["commodity"] = where(key_split["commodity"] == '2', 'milled', 'regular')

convert_yr = {str(x): str(x + 2010) for x in range(0, (gv.curr_year + 1 - 2010))}
key_split['year'] = key_split['year'].map(convert_yr)
key_split['month'] = key_split['month'].map(convert_mnt)

key_split["province"] = key_split["year"].str.cat(key_split["month"], sep='-')
key_split = key_split.rename(columns={'province': 'date'})
key_split = key_split.drop(columns=['year', 'month'])

price = pd.DataFrame(wsprice_2['values'].to_list(), index=wsprice_2.index)
price.columns = ['price']
key_split = key_split.merge(price, on=key_split.index, how='left')
key_split = key_split.drop(columns=['key_0'])

key_split.drop(key_split[key_split['price'] == '..'].index, inplace=True)

wholesale_2 = key_split.query("commodity == 'regular'")
wholesale_2.rename(columns={'price': 'regular_wholesale_price'}, inplace=True)
wholesale_2 = wholesale_2.drop(columns=['commodity'])

wholesale_2_temp = key_split.query("commodity == 'milled'")
wholesale_2_temp.rename(columns={'price': 'milled_wholesale_price'}, inplace=True)
wholesale_2_temp = wholesale_2_temp.drop(columns=['commodity'])

wholesale_2 = wholesale_2.merge(wholesale_2_temp, how='inner', on='date')

wholesale_price = dp.dataset_concat(wholesale, 
                                    wholesale_2, 
                                    'date',
                                    ['regular_wholesale_price',
                                     'milled_wholesale_price'])
