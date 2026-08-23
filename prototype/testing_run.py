import testing
import pandas as pd

response_stock = testing.response_stock

rice_stocks = pd.json_normalize(
    response_stock.json(), record_path=["data"]
)

# Display the cleaned DataFrame
print(rice_stocks)
