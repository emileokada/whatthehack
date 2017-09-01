import numpy as np
import json
import requests

headers = {"Accept":"application/json","Authorization":"Bearer b045dcde-4253-3e0f-865f-144556eed318"}

def format_int(n):
    s = str(np.int(n))
    l = len(s)
    return "0"*(11-l)+s

def add_zero(n):
    s = str(np.int(n))
    l = len(s)
    return "0"*(2-l)+s
    

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

def make_transaction(debit_acc,credit_acc):
    url = 'https://dnbapistore.com/hackathon/payments/1.0/payment'
    amount = 50 + 100*np.random.rand()
    day = np.random.choice(28)+1
    month= np.random.choice(12)+1
    year = np.random.choice(2)+2016
    data = {
        "debitAccountNumber": debit_acc, 
        "creditAccountNumber": credit_acc,
        "message": "Great beer",
        "amount": str(amount),
        "paymentDate": str(year) + add_zero(month) + add_zero(day)
    }
    r = requests.post(url,json=data,headers=headers)
    return r.json()
