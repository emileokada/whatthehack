import pandas as pd
import json

df = pd.read_csv('customer_data.csv',usecols=range(1,16))
json_string = df.to_json()
json_dict = json.loads(json_string)
n = len(json_dict['lastName'])
list_dict = [{key:json_dict[key][str(i)] for key in json_dict.keys()} for i in range(n)]
with open('customer_data.json','w') as f:
    json.dump(list_dict,f)
