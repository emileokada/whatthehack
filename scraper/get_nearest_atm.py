import numpy as np
import json

with open('../data/atm_data.json') as f:
    atms = json.load(f)
    
def nearest_atm(lat,lng):
    nearest_atm = min(atms,key=lambda atm:(lat-atm['latitude'])**2+(lng-atm['longitude'])**2)
    return nearest_atm


