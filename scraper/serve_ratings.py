import json
#from api_functions import get_pub_transactions

with open('pub_transactions.json') as f:
    pub_transactions = json.load(f)

def get_pub_score(pub_acc):
    if pub_acc in pub_transactions:
        transactions = pub_transactions[pub_acc]
        revenue = sum(transaction['amount'] for transaction in transactions)
        number_of_transactions = len(transactions)
    else:
        revenue = 0
        number_of_transactions = 0
    return revenue, number_of_transactions

