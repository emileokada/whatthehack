import sys
sys.path.insert(0, '/Users/emileokada/Documents/hackathon/scraper')

import numpy as np
import json
from api_functions import softmax


with open("../data/pub_account_data.json",'r') as f:
    pubs = json.load(f)

with open('../data/pub_transactions.json') as f:
    pub_transactions = json.load(f)

hip_places = [(59.910156, 10.726016),(59.922068, 10.759155),(59.913963, 10.751155)]

scores = softmax([sum(1/(0.01+(la - pub['geometry']['location']['lat'])**2 + (ll-pub['geometry']['location']['lng'])**2) for la,ll in hip_places[:2]) for pub in pubs])
scores = {pub['accountNumber']: 100*scores[i] for i,pub in enumerate(pubs)}

def get_pub_score(pub_acc):
    acc = str(pub_acc)
    if acc in pub_transactions:
        transactions = pub_transactions[acc]
        revenue = sum(transaction['amount'] for transaction in transactions)
        number_of_transactions = len(transactions)
    else:
        revenue = 0
        number_of_transactions = 0

    hipness = scores[pub_acc]
    return revenue, number_of_transactions, hipness

for pub in pubs:
    revenue, number_of_transactions, hipness = get_pub_score(pub['accountNumber'])
    pub['revenue'] = revenue
    pub['popularity'] = number_of_transactions
    pub['hipness'] = hipness 
    if 'photos' in pub:
        pub['photos'] = pub['photos'][0]
    else:
        pub['photos'] = {}

with open("../../data/data.json",'w') as f:
    json.dump(pubs,f)
