import sys
sys.path.insert(0, '/Users/emileokada/Documents/hackathon/scraper')

import numpy as np
import json
import datetime
from api_functions import softmax, get_date


with open("../data/pub_account_data.json",'r') as f:
    pubs = json.load(f)

with open("../data/customer_data.json",'r') as f:
    customers = json.load(f)
    customers = {c['customerID']:c for c in customers}

with open('../data/pub_transactions.json') as f:
    pub_transactions = json.load(f)

def get_pub_score(pub_acc):
    acc = str(pub_acc)
    if acc in pub_transactions:
        transactions = pub_transactions[acc]
        revenue = sum(transaction['amount'] for transaction in transactions)
        number_of_transactions = len(transactions)
        ages = np.array([0,0,0])
        hipness = 0
        for transaction in transactions:
            customer = customers[transaction['customerID']]
            age = np.round((datetime.datetime.now() - get_date(customer['dateOfBirth'])).days/365).astype('int')
            ages += np.array([age in bucket for bucket in age_buckets])
            if age <= 30:
                hipness += 1
        age_bucket = ages.tolist().index(max(ages))

    else:
        revenue = 0
        number_of_transactions = 0
        hipness = 0
        age_bucket = 1
        hipness = 0

    return revenue, number_of_transactions, hipness, age_bucket

for pub in pubs:
    revenue, number_of_transactions, hipness, age_bucket = get_pub_score(pub['accountNumber'])
    pub['revenue'] = revenue
    pub['popularity'] = number_of_transactions
    pub['hipness'] = hipness 
    pub['age_bucket'] = age_bucket
    if 'photos' in pub:
        if type(pub['photos']) == type([]):
            pub['photos'] = pub['photos'][0]
        else:
            pub['photos'] = pub['photos']
    else:
        pub['photos'] = {}

with open("../../data/data.json",'w') as f:
    json.dump(pubs,f)
