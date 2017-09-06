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

hip_places = [(59.910156, 10.726016),(59.922068, 10.759155),(59.913963, 10.751155)]
age_buckets = [range(0,30),range(30,50),range(60,100)]

scores = softmax([sum(1/(0.01+(la - pub['geometry']['location']['lat'])**2 + (ll-pub['geometry']['location']['lng'])**2) for la,ll in hip_places[:2]) for pub in pubs])
scores = {pub['accountNumber']: 100*scores[i] for i,pub in enumerate(pubs)}

def get_pub_score(pub_acc):
    acc = str(pub_acc)
    if acc in pub_transactions:
        transactions = pub_transactions[acc]
        revenue = sum(transaction['amount'] for transaction in transactions)
        number_of_transactions = len(transactions)
        ages = np.array([0,0,0])
        for transaction in transactions:
            customer = customers[transaction['customerID']]
            age = np.round((datetime.datetime.now() - get_date(customer['dateOfBirth'])).days/365).astype('int')
            ages += np.array([age in bucket for bucket in age_buckets])
        age_bucket = ages.tolist().index(max(ages))

    else:
        revenue = 0
        number_of_transactions = 0
        hipness = 0
        age_bucket = 1

    hipness = scores[pub_acc]
    return revenue, number_of_transactions, hipness, age_bucket

for pub in pubs:
    revenue, number_of_transactions, hipness, age_bucket = get_pub_score(pub['accountNumber'])
    pub['revenue'] = revenue
    pub['popularity'] = number_of_transactions
    pub['hipness'] = hipness 
    pub['age_bucket'] = age_bucket
    if 'photos' in pub:
        pub['photos'] = pub['photos'][0]
    else:
        pub['photos'] = {}

with open("../../data/data.json",'w') as f:
    json.dump(pubs,f)
