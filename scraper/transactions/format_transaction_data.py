import json

with open('../data/transactions.json') as f:
    transactions  = json.load(f)

with open('../data/pub_account_data.json') as f:
    pubs = json.load(f)

pub_account_numbers = [pub['accountNumber'] for pub in pubs]

transactions_per_pub = {account_number: [transaction for transaction in transactions if transaction['pub_account'] == account_number] for account_number in pub_account_numbers}

with open('../data/pub_transactions.json','w') as f:
    json.dump(transactions_per_pub,f)
