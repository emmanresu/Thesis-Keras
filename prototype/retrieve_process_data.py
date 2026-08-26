import json
import requests
import pandas as pd
from datetime import date
from numpy import where
import data_processing as dp
import rice_stocks as rs
# import price_wholesale as pw
# import price_retail as pr

dataset = rs.stock
# dataset = dataset.merge(pw.wholesale_price, how='inner', on='date')
# dataset = dataset.merge(pr.retail_price, how='inner', on='date')

print(dataset)



