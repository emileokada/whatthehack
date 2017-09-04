import numpy as np
import json
import datetime
from api_functions import format_int, make_transaction, softmax, format_date

#Likelihood of a purchase on a given weekday
weekday_likelihoods = np.array([1,2,3,3,4,5,1],dtype=np.float32)
weekday_likelihoods /= weekday_likelihoods.sum()

#Generate possible days and sort them into weekdays
base = datetime.datetime.today()
date_list = [base - datetime.timedelta(days=x) for x in range(0, 365)]
weekdays = {i:[] for i in range(7)}
for day in date_list:
    weekdays[day.weekday()].append(day)


with open("./pub_account_data.json") as f:
    pubs = json.load(f)

pub_scores = softmax([pub['rating'] if 'rating' in pub else 2.5 for pub in pubs])

with open("./account_data.json") as f:
    customers = json.load(f)

def generate_random_transactions(number_of_transactions=1):
    transactions = []
    for i in range(number_of_transactions):
        choice = np.random.choice(['cheap','expensive'],p=[0.6,0.4])
        is_group_purchase = np.random.binomial(1,0.05)

        if is_group_purchase:
            if choice == 'cheap':
                amount = sum(np.maximum(100+40*np.random.randn(np.random.choice(range(10,30))),20))
            if choice == 'expensive':
                amount = sum(np.maximum(180+40*np.random.randn(np.random.choice(range(10,30))),20))
        else:
            if choice == 'cheap':
                amount = np.maximum(100+40*np.random.randn(),20)
            if choice == 'expensive':
                amount = np.maximum(180+40*np.random.randn(),20)
        
        pub = np.random.choice(pubs,p=pub_scores)
        customer = np.random.choice(customers)

        weekday = np.random.choice(7,p=weekday_likelihoods)
        date = np.random.choice(weekdays[weekday])
        transactions.append({
            'pub_account': pub['accountNumber'],
            'customer_account':customer['accountNumber'],
            'pubID': pub['customerID'],
            'customerID': customer['customerID'],
            'amount': amount,
            'date': format_date(date),
            'weekday': date.weekday()
        })

    return transactions

#transactions = generate_random_transactions(100000)
#with open('transactions.json','w') as f:
#    json.dump(transactions,f)
