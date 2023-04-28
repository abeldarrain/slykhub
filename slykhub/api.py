from http.client import error
from urllib import request, parse
import json
import asyncio
import aiohttp
from urllib.error import HTTPError



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
    except Exception as e:
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

#return balance of specific wallet from the slyk for each existing asset given the wallet id
def get_wallet_balance(apikey, id):
    try:
        url="https://api.slyk.io/wallets/"+id+"/balance"
        req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
        data = request.urlopen(req, timeout = 10000)
        json_data = json.loads(data.read())
        print(f'Returning wallet balance for {id}')
        return json_data
    except error as e:
        print(e)
    
    except HTTPError as e:
        print(e)
        return e

def get_tasks_for_balance(apikey, wallets,  session):
        tasks = []
        for wallet in wallets:
                url="https://api.slyk.io/wallets/"+wallet+"/balance"
                tasks.append(asyncio.create_task(session.get(url, ssl=False, headers={ 'apiKey': apikey} )))
        return tasks                      
                
async def get_wallets_balance(apikey, wallets):
        results =[]
        async with aiohttp.ClientSession() as session:
                try:
                        tasks = get_tasks_for_balance(apikey, wallets, session)
                        responses = await asyncio.gather(*tasks)
                        for response in responses:
                                results.append( await response.json()) 
                        print(f'#############THESE ARE THE RESULTS {results}')  
                        return results
                except error as e:
                        print(e)
                
                except HTTPError as e:
                        print(e)
                        return e

def get_payment_methods(apikey, url="https://api.slyk.io/payment-methods"):  
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

def get_completed_transactions(apikey, url="https://api.slyk.io/transactions?filter[status]=completed&filter[code]=nin:internal:purchase&filter[code]=nin:internal:earn:task&filter[code]=nin:internal:bonus:referral:earn&filter[code]=nin:internal:bonus:referral:purchase&filter[code]=nin:internal&filter[code]=nin:internal:bonus:purchase"):  
        return_data = {}
        try:
                req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
                total_rows = json_data['total']
        except HTTPError as e:
                print(e)
                return e
        except Exception as e:
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

def get_orders(apikey, url="https://api.slyk.io/orders?page[size]=100&sorted=createdAt&filter[orderStatus]=fulfilled"):  
        return_data = {}
        try:
                req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
                total_rows = json_data['total']
        except HTTPError as e:
                print(e)
                return e
        except Exception as e:
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

def get_enabled_assets(apikey, url="https://api.slyk.io/assets?filter[enabled]=true"): 
        return_data = {}
        try:
                req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
                total_rows = json_data['total']
        except HTTPError as e:
                print(e)
                return e
        except Exception as e:
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
 
def get_rates(apikey, fromasset, toasset, url="https://api.slyk.io/rates"): 
        return_data = {}
        finalurl = str(url +f'/' + fromasset +f'/'+ toasset)
        print(f'This is the final URL: {finalurl}')
        try:
                req = request.Request(finalurl, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
        except HTTPError as e:
                print(e)
                return e
        except Exception as e:
                return e
        print(f'This is the returning data : {return_data}')
        return return_data


def get_user_by_id(apikey, id, url="https://api.slyk.io/users"): 
        return_data = {}
        finalurl = str(f'{url}/{id}')
        print(f'This is the final URL: {finalurl}')
        try:
                req = request.Request(finalurl, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
        except HTTPError as e:
                print(e)
                return e
        except Exception as e:
                return e
        
        return return_data

def get_completed_tasks_transactions(apikey, wallet_id, url="https://api.slyk.io/transactions?filter[status]=completed&filter[code]=internal:earn:task"):
        return_data = {}
        finalurl = url +'&filter[destinationWalletId]=' + str(wallet_id)
        
        print(f'this is the final url for tasks:{finalurl}')
        try:
                req = request.Request(finalurl, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
                total_rows = json_data['total']
        except HTTPError as e:
                print(e)
                return e
        except Exception as e:
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

def get_task_by_id(apikey, id, url="https://api.slyk.io/tasks"):
        return_data = {}
        finalurl = url +'/'+ str(id)
        try:
                req = request.Request(finalurl, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
        except HTTPError as e:
                print(e)
                return e
        except Exception as e:
                return e
        return return_data

def get_order_details_by_id(apikey, order_id, url="https://api.slyk.io/orders"):
        return_data = {}
        finalurl = url +'/'+ str(order_id) +'/lines'
        try:
                req = request.Request(finalurl, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
        except HTTPError as e:
                print(e)
                return e
        except Exception as e:
                return e
        return return_data

def get_orders_for_user(apikey, user_id, url="https://api.slyk.io/orders?filter[orderStatus]=fulfilled&sorted=createdAt"):
        return_data = {}
        finalurl = url +'&filter[userId]=' + str(user_id)
        
        print(f'this is the final url for orders:{finalurl}')
        try:
                req = request.Request(finalurl, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
                total_rows = json_data['total']
        except HTTPError as e:
                print(e)
                return e
        except Exception as e:
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

def get_product_by_id(apikey, product_id, url="https://api.slyk.io/products"):
        return_data = {}
        finalurl = url +'/'+ str(product_id) 
        try:
                req = request.Request(finalurl, headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey})
                data = request.urlopen(req, timeout = 100)
                json_data = json.loads(data.read())
                return_data = json_data
        except HTTPError as e:
                print(e)
                return e
        except Exception as e:
                return e
        return return_data

def create_user(apikey, userdata):
        print(userdata)
        try:
                req =  request.Request("https://api.slyk.io/users/", headers={'User-Agent': 'Mozilla/5.0', 'apiKey': apikey}, data=userdata)
                resp = request.urlopen(req)
        except HTTPError as e:
                print(e.reason)
 
              
                

                