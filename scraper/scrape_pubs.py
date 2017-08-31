import requests
import pandas as pd
import numpy as np
import json

#Bjorvika, Aker brygge, Grunerlokka, Ullevaald, Majorstuen, etc.
key_locations = ['59.907588,10.759842', '59.910156, 10.726016', 
        '59.922068, 10.759155', '59.950196, 10.735658', 
        '59.928533, 10.715530','59.925889, 10.744663',
        '59.940104, 10.727357', '59.932319, 10.783982',
        '59.919281, 10.707815']

google_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

key = 'AIzaSyCLY-MK8V2RS9KwZOUqakpUBYxzmHVGzDg'

pubs = []

for loc in key_locations:
    data = {
        'location':loc,
        'radius':1000,
        'type':['bar','pub'],
        'hasNextPage':'true',
        'nextPage()':'true',
        'key':key
    }

    for i in range(3):
        r = requests.get(google_url,params=data)
        json_response = r.json()

        pubs = pubs + json_response['results']
        if 'next_page_token' in json_response:
            next_page_token = json_response['next_page_token']
            data['next_page_token'] = next_page_token
        else:
            break

unique_pubs = []
unique_names = []

for pub in pubs:
    if pub['name'] not in unique_names:
        unique_pubs.append(pub)
        unique_names.append(pub['name'])

print("Number of pubs found: %s"%len(unique_pubs))
number_of_pubs = len(unique_pubs)
custIDs = np.random.choice(range(10**10,10**11-1),number_of_pubs,replace=False)
account_numbers = np.random.choice(range(10**10,10**11-1),number_of_pubs,replace=False)
for i, pub in enumerate(unique_pubs):
    pub['accountNumber'] = account_numbers[i]
    pub['customerID'] = custIDs[i]
#list(set([pub['name'] for pub in pubs]))


with open('data.json', 'w') as outfile:
        json.dump(unique_pubs, outfile)

