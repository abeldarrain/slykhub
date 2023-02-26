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
    
def get_dict_user_growth(user_growth_dict, list_of_dates):
    new_users_by_date_given = {}
    for day in list_of_dates:
        if user_growth_dict.get(day):
            new_users_by_date_given[day] = user_growth_dict[day]
        else:
            new_users_by_date_given[day] = 0
    return new_users_by_date_given

def get_stacked_users_dict(user_growth_dict, list_of_dates):
    total = 0
    total_users_by_date_given = {}
    ##########get stacked users til date##############
    if list_of_dates[0] in list(user_growth_dict.keys()):
        stop = list_of_dates[0]
        for i in user_growth_dict.keys():   
            if i == stop:
                break
            else:
                total += user_growth_dict[i]
    
    ####make dict####
    for day in list_of_dates:
        if day in user_growth_dict:
            total += user_growth_dict[day]
        total_users_by_date_given[day] = total
        
    
    return total_users_by_date_given

def get_stacked_active_users_dict(orders, list_of_dates, list_of_dates_complete):
    ids = []
    total = 0
    orders_dict = {}
    total_active_users_by_date_given = {}
    
    #############################make orders dict######################
    
    for order in orders['data']:
        if order['userId'] not in ids:
            date = order['createdAt']
            formated_date = date[:10]
            ids.append(order['userId'])
            if formated_date in list(orders_dict.keys()):
                orders_dict[formated_date] += 1
            else:
                orders_dict[formated_date] = 1
    
    orders_dict = get_dict_user_growth(orders_dict, list_of_dates_complete)
    ##########get stacked active users til date##############
    if list_of_dates[0] in list(orders_dict.keys()):
        stop = list_of_dates[0]
        for i in orders_dict.keys():   
            if i == stop:
                break
            else:
                total += orders_dict[i]
    
    for day in list_of_dates:
        if day in orders_dict:
              total += orders_dict[day]
        total_active_users_by_date_given[day] = total
          
    return total_active_users_by_date_given