import json
import requests
import pandas as pd
from datetime import date
from numpy import where
from pathlib import Path

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
      output_folder = Path('json_files')
      output_folder.mkdir(parents=True, exist_ok=True)
      file_path = output_folder / f'{filename}.json'
      with open(file_path, "w", encoding="utf-8") as f:
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
  for n in name_col:
    temp[n] = temp[n + '_y'].fillna(temp[n + '_x'])
    temp = temp.drop(columns=[n + '_y', n + '_x'])
  return temp
