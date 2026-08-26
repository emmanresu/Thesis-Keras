import json
import requests
import pandas as pd
from datetime import date
from numpy import where
import data_processing as dp
import global_variables as gv


''' STAGE 1 RETAIL PRICE QUERY (2000 - 2009) '''
url_r_price_1 = 'https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/RP/0042M4ARP01.px'
commodity = ['2', '3']
quers = dp.queries(['Geolocation', ['00'],
                       ['Commdity', commodity],
                       ['Year', gv.year_part1],
                       ['Period', gv.year_part1]])
response_r_price1 = dp.request_data(url_r_price_1, quers, gv.check_list, 'rprice1')

rprice_1 = pd.json_normalize(
    response_r_price1.json(), record_path=["data"]
)
key_split = pd.DataFrame(rprice_1['key'].to_list(), index=rprice_1.index)
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

price = pd.DataFrame(rprice_1['values'].to_list(), index=rprice_1.index)
price.columns = ['price']

key_split = key_split.merge(price, on=key_split.index, how='left')
key_split = key_split.drop(columns=['key_0'])
key_split.drop(key_split[key_split['price'] == '..'].index, inplace=True)

retail = key_split.query("commodity == 'regular'")
retail.rename(columns={'price': 'regular_retail_price'}, inplace=True)
retail = retail.drop(columns=['commodity'])

retail_temp = key_split.query("commodity == 'milled'")
retail_temp.rename(columns={'price': 'milled_retail_price'}, inplace=True)
retail_temp = retail_temp.drop(columns=['commodity'])

retail = retail.merge(retail_temp, how='inner', on='date')


''' STAGE 2 RETAIL PRICE QUERY (2000 - 2009) '''
url_r_price_2 = 'https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/2018NEW/0042M4ARN01.px'
commodity = ['0', '1']
quers = dp.queries(['Geolocation', ['000000000'],
                       ['Commodity', commodity],
                       ['Year', gv.year_part2],
                       ['Period', gv.month]])
response_r_price2 = dp.request_data(url_r_price_2, quers, gv.check_list, 'rprice2')

rprice_2 = pd.json_normalize(
    response_r_price2.json(), record_path=["data"]
)
key_split = pd.DataFrame(rprice_2['key'].to_list(), index=rprice_2.index)
key_split.columns = ['province', 'commodity', 'year', 'month']

key_split["commodity"] = where(key_split["commodity"] == '2', 'milled', 'regular')
convert_yr = {str(x): str(x + 2010) for x in range(0, (gv.curr_year + 1 - 2010))}
key_split['year'] = key_split['year'].map(convert_yr)

key_split['month'] = key_split['month'].map(convert_mnt)

key_split["province"] = key_split["year"].str.cat(key_split["month"], sep='-')
key_split = key_split.rename(columns={'province': 'date'})
key_split = key_split.drop(columns=['year', 'month'])

price = pd.DataFrame(rprice_2['values'].to_list(), index=rprice_2.index)
price.columns = ['price']

key_split = key_split.merge(price, on=key_split.index, how='left')
key_split = key_split.drop(columns=['key_0'])

key_split.drop(key_split[key_split['price'] == '..'].index, inplace=True)

retail2 = key_split.query("commodity == 'regular'")
retail2.rename(columns={'price': 'regular_retail_price'}, inplace=True)
retail2 = retail2.drop(columns=['commodity'])

retail2_temp = key_split.query("commodity == 'milled'")
retail2_temp.rename(columns={'price': 'milled_retail_price'}, inplace=True)
retail2_temp = retail2_temp.drop(columns=['commodity'])

retail2 = retail2.merge(retail2_temp, how='inner', on='date')

retail_price = dp.dataset_concat(retail,
                                 retail2,
                                 'date',
                                 ['regular_retail_price',
                                  'milled_retail_price'])
