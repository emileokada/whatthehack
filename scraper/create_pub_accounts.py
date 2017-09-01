import numpy as np
import json
import requests
from api_functions import format_int, create_account, create_pub, get_account_info, get_customer_info


with open("../data/data.json") as f:
    pubs = json.load(f)

number_of_pubs = len(pubs)
for i, pub in enumerate(pubs):
    pub["customerID"] = format_int(i)
#list(set([pub["name"] for pub in pubs]))

for pub in pubs:
    response = create_pub(pub)
    print(response.json())
    response = create_account(pub['customerID'],'Pub account')
    pub['accountNumber'] = response.json()['accountNumber']

with open('./pub_account_data.json', 'w') as outfile:
        json.dump(pubs, outfile)
