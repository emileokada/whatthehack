import numpy as np
import json
import requests

headers = {"Accept":"application/json","Authorization":"Bearer eaf16995-a77e-3654-a5a3-b29e985168e3"}

def format_int(n):
    s = str(np.int(n))
    l = len(s)
    return "0"*(11-l)+s

def add_zero(n):
    s = str(np.int(n))
    l = len(s)
    return "0"*(2-l)+s

def format_date(date):
    year = str(date.year)
    month = add_zero(date.month)
    day = add_zero(date.day)
    return year + "-" + month + "-" + day
    
def softmax(scores):
    scaled_scores = np.exp(scores - np.max(scores))
    return scaled_scores / scaled_scores.sum()


def get_customer_info(cust_id):
    url = "https://dnbapistore.com/hackathon/customers/1.0/customer/" + format_int(cust_id)
    r = requests.get(url,headers=headers)
    return r.json()

def get_customer_account_info(cust_id):
    url = "https://dnbapistore.com/hackathon/accounts/1.0/account/customer/" + format_int(cust_id)
    r = requests.get(url,headers=headers)
    return r.json()

def create_pub(pub):
    url = "https://dnbapistore.com/hackathon/customers/1.0/customer"
    data = {
            "personalNumber": pub['customerID'], 
            "firstName": pub['name'],
            "lastName": pub['id'], 
            "dateOfBirth": "1900-01-01", 
            "gender": "Male",
            "nationality": "Norwegian", 
            "address":{
                "street":pub['vicinity'], 
                "postalCode":"0000", 
                "city":"Oslo", 
                "country":"Norway"
            },
            "phoneNumber":"+4700000000", 
            "email": pub['customerID'] + "@pub.beer", 
            "idNumber": "1234567", 
            "idType": "passport"
    }
    r = requests.post(url,json=data,headers=headers)
    return r

def patch_pub(pub):
    url = "https://dnbapistore.com/hackathon/customers/1.0/customer"
    data = {
            "customerID": pub['customerID'], 
            "address":{
                "street":pub['vicinity'], 
                "postalCode":"0000", 
                "city":"Oslo", 
                "country":"Norway"
            },
            "phoneNumber":"+4700000000", 
            "email": pub['customerID'] + "@pub.beer"
    }
    r = requests.patch(url,json=data,headers=headers)
    return r

def create_account(custID,account_name):
    url = "https://dnbapistore.com/hackathon/accounts/1.0/account"
    data = {"customerID":custID,"accountName":account_name,"accountType":"Current","currency":"NOK"}
    r = requests.post(url,json=data,headers=headers)
    return r

def delete_account(custID,account_number):
    url = "https://dnbapistore.com/hackathon/accounts/1.0/account/close"
    data = {"customerID":custID,"accountName":account_name}
    r = requests.patch(url,json=data,headers=headers)
    return r

def get_account_info(custID,account_number):
    url = "https://dnbapistore.com/hackathon/accounts/1.0/account/details"
    data = {"customerID":custID,"accountNumber":account_number}
    r = requests.get(url,params=data,headers=headers)
    return r

def check_pub_existsence(custID):
    url = "https://dnbapistore.com/hackathon/customers/1.0/customer/" + custID
    r = requests.get(url,headers=headers)
    #if r.json()['something']:
    #    return True
    return False

def make_transaction(debit_acc,credit_acc,amount,date):
    url = 'https://dnbapistore.com/hackathon/payments/1.0/payment'
    data = {
        "debitAccountNumber": debit_acc, 
        "creditAccountNumber": credit_acc,
        "message": "Great beer",
        "amount": amount,
        "paymentDate": date
    }
    r = requests.put(url,json=data,headers=headers)
    return r.json()

def get_transactions(customerID,accountNumber):
    url = 'https://dnbapistore.com/hackathon/accounts/1.0/account'
    data = {
        "customerID": customerID,
        "accountNumber": accountNumber,
        "dateFrom": "01012016",
        "dateTo": "01012018"
    }
    r = requests.get(url,params=data,headers=headers)
    return r.json()

def get_pub_transactions(pub):
    url = 'https://dnbapistore.com/hackathon/accounts/1.0/account'
    data = {
        "customerID": pub["customerID"],
        "accountNumber": pub["accountNumber"],
        "dateFrom": "01012016",
        "dateTo": "01012018"
    }
    r = requests.get(url,params=data,headers=headers)
    return r.json()

def get_transaction_info(transactionID):
    url = "https://dnbapistore.com/hackathon/payments/1.0/payment/" + str(transactionID)
    r = requests.get(url,headers=headers)
    return r.json()
