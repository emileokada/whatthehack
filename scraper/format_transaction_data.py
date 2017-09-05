import json

with open('transactions.json') as f:
    transactions  = json.load(f)

with open('pub_account_data.json') as f:
    pubs = json.load(f)

pub_account_numbers = [pub['accountNumber'] for pub in pubs]

transactions_per_pub = {account_number: [transaction for transaction in transactions if transaction['pub_account'] == account_number] for account_number in pub_account_numbers}

with open('pub_transactions.json','w') as f:
    json.dump(transactions_per_pub,f)
