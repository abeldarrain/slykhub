from http.client import error
import urllib.request
import json
from urllib.request import  Request
from urllib.error import HTTPError

#return a list of all users registered in the slyk
def get_users(apikey, url="https://api.slyk.io/users"):
    return_data = {}
    try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
            data = urllib.request.urlopen(req, timeout = 100)
            json_data = json.loads(data.read())
            return_data = json_data
    except error as e:
            print(e)
    
    except HTTPError as e:
            print(e)
            return e
    else:
        return return_data
    
#return a user registered in the slyk
def get_owner(apikey, url="https://api.slyk.io/users?filter[role]=owner"):
    return_data = {}
    try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
            data = urllib.request.urlopen(req, timeout = 100)
            json_data = json.loads(data.read())
            return_data = json_data
    except error as e:
            print(e)
    
    except HTTPError as e:
            print(e)
            return e
    else:
        return return_data
    
def get_enabled_tasks(apikey, url="https://api.slyk.io/tasks?filter[enabled]=true"):  
        return_data = {}
        try:
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = urllib.request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
        except error as e:
                print(e)

        except HTTPError as e:
                print(e)
                return e
        else:
                return return_data