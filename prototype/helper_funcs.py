import json
import requests
import pandas as pd
from datetime import date
from numpy import where

def queries(*args):
  query = []
  for i in range(len(args)):
    query.append({'code': f'{args[i][0]}',
                    'selection' : {'filter': 'item',
                    'values': args[i][1]}
    })
  return query

def request_data(url, queries, check_list, filename):
  payload = {
    "query": queries,
    "response": {"format": "json"},
  }
  headers = {"Content-Type": "application/json"}
  try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
      response.encoding = "utf-8-sig"
      data = response.json()
      output_filename = f"{filename}.json"
      with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
      check_list.append("success")
    else:
      check_list.append(f"fail: {response.status_code}")
      # print(f"API Error {response.status_code}: {response.text}")
  except requests.exceptions.RequestException as e:
    check_list.append(f"fail: {e}")
  return response

def dataset_concat(df1, df2, on_col, name_col):
  temp = pd.merge(df1, df2, on=on_col, how='outer')
  temp[name_col] = temp[name_col + '_y'].fillna(temp[name_col + '_x'])
  temp = temp.drop(columns=[name_col + '_y', name_col + '_x'])
  return temp
