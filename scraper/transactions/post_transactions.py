import json
from api_functions import make_transaction
from generate_transactions import generate_random_transactions

transactions = []
for i in range(10000):
    transaction = generate_random_transactions()[0]
    r = make_transaction(transaction['customer_account'],transaction['pub_account'],transaction['amount'],transaction['date'])
    print(r)
    if 'paymentIDNumber' in r:
        transaction['paymentIDNumber'] = r['paymentIDNumber']
        transactions.append(transaction)
    print(transaction)

with open('completed_transactions.json','w') as f:
    json.dump(transactions,f)
