import json
import requests
import pandas as pd
from datetime import date
from numpy import where
import helper_funcs as funcs

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


