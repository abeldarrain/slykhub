from http.client import error
from urllib import request, parse
import json

from urllib.error import HTTPError
from .util import get_task_id


#return a list of all users registered in the slyk
def get_users(apikey, url="https://api.slyk.io/users?page[size]=100&sorted=createdAt"):
    return_data = {}
    try:
            req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
            data = request.urlopen(req, timeout = 100)
            json_data = json.loads(data.read())
            return_data = json_data
            total_rows = json_data['total']
    except error as e:
            print(e)
    
    except HTTPError as e:
            return e
        
        
    for i in range(int(total_rows/100)):
        
        try:
            req = request.Request(url+"&page[number]="+str(i+2), headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
            data = request.urlopen(req, timeout = 100)
            json_data = json.loads(data.read())
            return_data['data'].extend(json_data['data'])
            print(url+"&page[size]="+str(i+2))
            print(len(return_data['data']))
            
        except error as e:
            print(e)

        except HTTPError as e:
            return e
    return return_data

def get_verified_users(apikey, url="https://api.slyk.io/users?page[size]=100&sorted=createdAt&filter[verified]=true"):
    return_data = {}
    try:
            req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
            data = request.urlopen(req, timeout = 100)
            json_data = json.loads(data.read())
            return_data = json_data
            total_rows = json_data['total']
    except error as e:
            print(e)
    
    except HTTPError as e:
            return e
        
        
    for i in range(int(total_rows/100)):
        
        try:
            req = request.Request(url+"&page[number]="+str(i+2), headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
            data = request.urlopen(req, timeout = 100)
            json_data = json.loads(data.read())
            return_data['data'].extend(json_data['data'])
            print(url+"&page[size]="+str(i+2))
            print(len(return_data['data']))
            
        except error as e:
            print(e)

        except HTTPError as e:
            return e
    return return_data


#return a user registered in the slyk
def get_owner(apikey, url="https://api.slyk.io/users?filter[role]=owner"):
    return_data = {}
    try:
            req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
            data = request.urlopen(req, timeout = 100)
            json_data = json.loads(data.read())
            return_data = json_data
    except error as e:
            print(e)
    
    except HTTPError as e:
            print(e)
            return e
    else:
        return return_data

def get_tasks(apikey, url="https://api.slyk.io/tasks?page[size]=100&sorted=createdAt"):  
        return_data = {}
        try:
                req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
                total_rows = json_data['total']
        except error as e:
                print(e)
        except HTTPError as e:
                print(e)
                return e
        
        for i in range(int(total_rows/100)):
                try:
                        req = request.Request(url+"&page[number]="+str(i+2), headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                        data = request.urlopen(req, timeout = 100)
                        json_data = json.loads(data.read())
                        return_data['data'].extend(json_data['data'])
                        print(url+"&page[size]="+str(i+2))
                        print(len(return_data['data']))
                except error as e:
                        print(e)
                except HTTPError as e:
                        return e
        return return_data
    
def get_enabled_tasks(apikey, url="https://api.slyk.io/tasks?page[size]=100&sorted=createdAt&filter[enabled]=true"):  
        return_data = {}
        try:
                req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
                total_rows = json_data['total']
        except error as e:
                print(e)
        except HTTPError as e:
                print(e)
                return e
        
        for i in range(int(total_rows/100)):
                try:
                        req = request.Request(url+"&page[number]="+str(i+2), headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                        data = request.urlopen(req, timeout = 100)
                        json_data = json.loads(data.read())
                        return_data['data'].extend(json_data['data'])
                        print(url+"&page[size]="+str(i+2))
                        print(len(return_data['data']))
                except error as e:
                        print(e)
                except HTTPError as e:
                        return e
        return return_data
        
def complete_task(task, user_ids, apikey, url="https://api.slyk.io/tasks/"):
        err422 = 0
        taskid = get_task_id(task, get_tasks(apikey))
        req_url = str(url) + str(taskid) + '/complete'
        for user_id in user_ids:
                try:
                        data = parse.urlencode({'userId': user_id}).encode()
                        req =  request.Request(req_url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey}, data=data)
                        resp = request.urlopen(req)
                except HTTPError as e:
                        if e.code == 422:
                                print(e)
                                err422+=1
                        else:
                                return e
        return err422                

#return balance of specific wallet from the slyk for each existing asset given the wallet id
def get_wallet_balance(apikey, id):
    try:
        url="https://api.slyk.io/wallets/"+id+"/balance"
        req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
        data = request.urlopen(req, timeout = 100)
        json_data = json.loads(data.read())
        return json_data
    except error as e:
        print(e)
    
    except HTTPError as e:
        print(e)
        return e

def create_user(apikey, userdata):
        print(userdata)
        try:
                req =  request.Request("https://api.slyk.io/users/", headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey}, data=userdata)
                resp = request.urlopen(req)
        except HTTPError as e:
                print(e.reason)
                
                

                