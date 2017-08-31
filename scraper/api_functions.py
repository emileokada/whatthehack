import numpy as np
import json
import requests

headers = {"Accept":"application/json","Authorization":"Bearer b045dcde-4253-3e0f-865f-144556eed318"}

def format_int(n):
    s = str(np.int(n))
    l = len(s)
    return "0"*(11-l)+s

def get_customer_info(cust_id):
    url = "https://dnbapistore.com/hackathon/customers/1.0/customer/" + format_int(cust_id)
    r = requests.get(url,headers=headers)
    return r.json()

def get_account_info(cust_id):
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

def create_account(custID,account_name):
    url = "https://dnbapistore.com/hackathon/accounts/1.0/account"
    data = {"customerID":custID,"accountName":account_name,"accountType":"Current","currency":"NOK"}
    #data = {"customerID": "01011900123", "accountName": "New batmobile", "accountType": "Savings", "currency": "USD"}
    r = requests.post(url,json=data,headers=headers)
    return r

