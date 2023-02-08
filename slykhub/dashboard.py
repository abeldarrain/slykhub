from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from slykhub.auth import login_required
from slykhub.db import get_db
from urllib.error import HTTPError
from .api import get_verified_users , get_enabled_tasks, complete_task, get_wallet_balance, create_user



bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def redir():
    return redirect(url_for('dashboard.home'))

@bp.route('/home')
@login_required
def home():
    # for i in range(8,1000):
    #     userdata = {"approved" : True,
    #                 "email" : f"fake_user{str(i)}@fakemail.com",
    #                 "code": "R876aesad",
    #                 "locale": "en",
    #                 "name": "Fakelton"+str(i),
    #                 "password": "Fakelton3",
    #                 "verified": True
    #                 }
    #     from json import dumps
    #     import urllib
    #     aaa= []
    #     for i in userdata.keys():
    #         (a,b) = (i,dumps(userdata[i]))
    #         aaa.append((a,b))
        
        
    #     userdata = urllib.parse.urlencode(aaa)
    #     # userdata = dumps(userdata)
    #     userdata = userdata.encode()
    #     create_user(session['api_key'],userdata)
        return render_template('dashboard/home.html')

@bp.route('/tasks', methods=('GET', 'POST'))
@login_required
def tasks():
    error = None
    if request.method == 'POST':
        selected_task = request.form['task']
        if not selected_task:
            error='No selected task'
        user_ids =request.form.getlist('taskcheckbox')
        if not user_ids:
            error='No selected users'
            
        if not error:
            error=complete_task(selected_task, user_ids, session['api_key'])
            if error is not HTTPError:
                err422 = error
                succ = len(user_ids)-err422
                error = 'Selected users already completed the task' if succ == 0 else None
        if not error:  
            flash(f'Successfully completed task for {succ} users.', 'success')
            
    headers=('User', 'Email', 'Balance', 'Select')
    rows=[]
    tasks=[]
    user_data = get_verified_users(session['api_key'])
    if user_data is HTTPError:
        error = user_data
    else:
       
        for user in user_data['data']:
            if 'user' in user['roles']:
                (username, email, ids) = (user['name'], user['email'], user['id'])
                wallet = user['primaryWalletId']
                balancedata = get_wallet_balance(session['api_key'], wallet)
                if balancedata is HTTPError:
                    error = balancedata
                else:    
                    balance = balancedata['data']
                    rows.append((username, email, balance, ids))
    tasks_data=get_enabled_tasks(session['api_key'])
    if tasks_data is HTTPError:
        error = tasks_data
    else:
        for task in tasks_data['data']:
            tasks.append(task['name'])
                
    if error:
        flash(error, 'error')
    return render_template('dashboard/tasks.html', headers=headers, rows=rows, tasks=tasks)
