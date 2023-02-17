from http.client import error
from urllib import request, parse
import json

from urllib.error import HTTPError
from .util import get_task_id
from .api import get_tasks

def complete_task(task, user_ids, apikey, url="https://api.slyk.io/tasks/"):
        err422 = 0
        taskid = get_task_id(task, get_tasks(apikey))
        req_url = str(url) + str(taskid) + '/complete'
        ia=0
        for user_id in user_ids:
                ia+=1
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
                print(f'{ia} loop, task completed for {user_id}, 422 error: {err422}')
        return err422  