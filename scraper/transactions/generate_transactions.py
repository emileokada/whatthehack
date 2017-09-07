import sys
sys.path.insert(0, '/Users/emileokada/Documents/hackathon/scraper')

import numpy as np
import json
import datetime
from api_functions import format_int, make_transaction, softmax, format_date, get_date

#Likelihood of a purchase on a given weekday
weekday_likelihoods = np.array([1,2,3,3,4,5,1],dtype=np.float32)
weekday_likelihoods /= weekday_likelihoods.sum()

#Generate possible days and sort them into weekdays
base = datetime.datetime.today()
date_list = [base - datetime.timedelta(days=x) for x in range(0, 365)]
weekdays = {i:[] for i in range(7)}
for day in date_list:
    weekdays[day.weekday()].append(day)


with open("../data/pub_account_data.json") as f:
    pubs = json.load(f)

pub_scores = softmax([pub['rating'] if 'rating' in pub else 2.5 for pub in pubs])

with open("../data/account_data.json") as f:
    customers = json.load(f)

hip_places = [(59.910156, 10.726016),(59.922068, 10.759155),(59.913963, 10.751155)]
age_buckets = [range(0,30),range(30,50),range(60,100)]

scores_p = softmax([sum(1/(0.01+(la - pub['geometry']['location']['lat'])**2 + (ll-pub['geometry']['location']['lng'])**2) for la,ll in hip_places[:2]) for pub in pubs])
scores = {pub['accountNumber']: 100*scores_p[i] for i,pub in enumerate(pubs)}

def generate_random_transactions(number_of_transactions=1):
    transactions = []
    for i in range(number_of_transactions):
        customer = np.random.choice(customers)
        age = np.round((datetime.datetime.now() - get_date(customer['dateOfBirth'])).days/365).astype('int')

        if age <= 30:
            pub = np.random.choice(pubs,p=scores_p)
        else: 
            pub = np.random.choice(pubs)

        if 'rating' in pub:
            if pub['rating'] > 4:
                choice = np.random.choice(['cheap','expensive'],p=[0.1,0.9])
                is_group_purchase = np.random.binomial(1,0.0)
            else:
                choice = np.random.choice(['cheap','expensive'],p=[0.9,0.1])
                is_group_purchase = np.random.binomial(1,0.05)

        if is_group_purchase:
            if choice == 'cheap':
                amount = sum(np.maximum(80+40*np.random.randn(np.random.choice(range(20,30))),20))
            if choice == 'expensive':
                amount = sum(np.maximum(150+40*np.random.randn(np.random.choice(range(20,30))),20))
        else:
            if choice == 'cheap':
                amount = np.maximum(80+40*np.random.randn(),20)
            if choice == 'expensive':
                amount = np.maximum(150+40*np.random.randn(),20)

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

transactions = generate_random_transactions(10000)
with open('../data/transactions.json','w') as f:
    json.dump(transactions,f)
