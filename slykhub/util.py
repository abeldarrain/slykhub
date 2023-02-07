

def get_task_id(task, tasks):
    for i in tasks['data']:
        if i['name'] == str(task): 
            return i['id'] 
    return None