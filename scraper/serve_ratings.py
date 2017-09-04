import json
from api_functions import get_transactions

with open('pub_account_data.json') as f:
    pubs = json.load(f)

for pub in pubs:
    transactions = get_pub_transactions(pub)
    print(transactions)
    #pub['number_of_transactions'] = len(transactions)
    #pub['revenue'] = sum((transaction['amount'] for transaction in transactions)
