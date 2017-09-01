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

with open("../data/data_old.json") as f:
    old_pubs = json.load(f)

pubs = []

for loc in key_locations:
    data = {
        'location':loc,
        'radius':100,
        'type':['bar','pub'],
        'nextPage()':'true',
        'key':key
    }

    r = requests.get(google_url,params=data)
    json_response = r.json()
    pubs = pubs + json_response['results']

    while 'next_page_token' in json_response:
        next_page_token = json_response['next_page_token']
        data['pagetoken'] = next_page_token
        json_response['status'] = 'INVALID_REQUEST'

        while json_response['status'] == 'INVALID_REQUEST':
            r = requests.get(google_url,params=data)
            json_response = r.json()
            pubs = pubs + json_response['results']

new_pubs = []
unique_names = [pub['name'] for pub in old_pubs]
#unique_names = []

for pub in pubs:
    if pub['name'] not in unique_names:
        new_pubs.append(pub)
        unique_names.append(pub['name'])

all_pubs = old_pubs+new_pubs
#all_pubs = new_pubs

print("Number of new pubs: %s"%len(new_pubs))
print("Total number of pubs: %s"%len(all_pubs))

with open('../data/data.json', 'w') as outfile:
        json.dump(all_pubs, outfile)
