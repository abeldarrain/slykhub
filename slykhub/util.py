from decimal import *
from .api import get_rates
from urllib.error import HTTPError

def get_task_id(task, tasks):
    for i in tasks['data']:
        if i['name'] == str(task): 
            return i['id'] 
    return None


def convert(apikey,values, toasset, fromasset):
    rvalues=[]
    values = list(map( lambda x: Decimal(x), values))
    if toasset != fromasset:
        print(f'This are the values{values}')
        rate = get_rates(apikey, fromasset, toasset)
        print(rate.__class__.__name__ )
        if isinstance(rate,HTTPError):
            return rate
        else:
            rate = Decimal(rate['data']['rate'])
            print(f'This is the rate{rate}')
            values = list(map(lambda x:x*rate,values))
    values = sorted(values, key=float)
    for val in values:
        if val % 1 == 0:
            val = str(val).rstrip('0')
            val = val.rstrip('.')
        else:
            val = str(val.normalize())
        rvalues.append(val)                 
    return rvalues
    
