import json
import requests
import pandas as pd
from datetime import date
from numpy import where
import prototype.data_processing as funcs

curr_year = date.today().year
year_stock = [str(i) for i in range(2000, curr_year + 1)]
year_part1 = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19']
year_part2 = [str(i - 2010) for i in range(2010, curr_year + 1)]
month = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
cl = []

url_stocks = 'https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2E/CS/0032E4ECNV0.px'
sector = ['0', '1', '2', '3']
quers = funcs.queries(['Sector', sector],
                ['Year', year_stock],
                ['Month', month])
response_stock = funcs.request_data(url_stocks, quers, cl, "stocks")

url_ws_price_1 = 'https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/WS/0012M4AWP01.px'
commodity = ['2', '3']
quers = funcs.queries(['Region province', ['00']],
                       ['Commodity', ['2', '3']],
                       ['Year', year_part1],
                       ['Month', month])
response_ws_price1 = funcs.request_data(url_ws_price_1, quers, cl, 'wsprice1')

url_ws_price_2 = ''
commodity = ['2', '3']
quers = funcs.queries(['Geolocation', ['0'],
                       ['Commodity', commodity],
                       ['Year', year_part2],
                       ['Period', month]])
response_ws_price2 = funcs.request_data(url_ws_price_2, quers, cl, 'wsprice2')

url_r_price_1 = ''
commodity = ['2', '3']
quers = funcs.queries(['Geolocation', ['00'],
                       ['Commdity', commodity],
                       ['Year', year_part1],
                       ['Period', year_part1]])
response_r_price1 = funcs.request_data(url_r_price_1, quers, cl, 'rprice1')

url_r_price_2 = ''
commodity = ['0', '1']
quers = funcs.queries(['Geolocation', ['000000000'],
                       ['Commodity', commodity],
                       ['Year', year_part2],
                       ['Period', month]])
response_r_price2 = funcs.request_data(url_r_price_2, quers, cl, 'rprice2')


