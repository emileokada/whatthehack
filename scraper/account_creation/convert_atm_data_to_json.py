import pandas as pd
import json

df = pd.read_csv('../data/atm_data.csv',usecols=range(1,10),skiprows=1)
json_string = df.to_json()
json_dict = json.loads(json_string)
n = len(json_dict['atmID'])
list_dict = [{key:json_dict[key][str(i)] for key in json_dict.keys()} for i in range(n)]
with open('../data/atm_data.json','w') as f:
    json.dump(list_dict,f)
