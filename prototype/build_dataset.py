import features.rice_stocks as rs
import features.price_wholesale as pw
import features.price_retail as pr

dataset = rs.stock
dataset = dataset.merge(pw.wholesale_price, how='inner', on='date')
dataset = dataset.merge(pr.retail_price, how='inner', on='date')
dataset.to_csv("csv_files\\dataset.csv", index=False)

print(dataset)
