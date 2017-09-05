import numpy as np
import json

with open("../data/pub_account_data.json",'r') as f:
    pubs = json.load(f)

with open('../data/pub_transactions.json') as f:
    pub_transactions = json.load(f)

def get_pub_score(pub_acc):
    acc = str(pub_acc)
    if acc in pub_transactions:
        transactions = pub_transactions[acc]
        revenue = sum(transaction['amount'] for transaction in transactions)
        number_of_transactions = len(transactions)
    else:
        revenue = 0
        number_of_transactions = 0

    revenue = 5*np.random.rand()
    revenue = 10*np.random.rand()
    return revenue, number_of_transactions

for pub in pubs:
    revenue, number_of_transactions = get_pub_score(pub['accountNumber'])
    pub['revenue'] = revenue
    pub['popularity'] = number_of_transactions

with open("../../data/data.json",'w') as f:
    json.dump(pubs,f)
