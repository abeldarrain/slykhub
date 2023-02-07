from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from slykhub.auth import login_required
from slykhub.db import get_db
from urllib.error import HTTPError
from .api import get_verified_users , get_enabled_tasks, complete_task, get_wallet_balance



bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def redir():
    return redirect(url_for('dashboard.home'))

@bp.route('/home')
@login_required
def home():
    return render_template('dashboard/home.html')

@bp.route('/tasks', methods=('GET', 'POST'))
@login_required
def tasks():
    if request.method == 'POST':
        error =""
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
        else: 
            flash(error, 'error')
    user_data = get_verified_users(session['api_key'])
    headers=('#','User', 'Email', 'Balance', 'Select')
    rows=[]
    for user in user_data['data']:
        if 'user' in user['roles']:
            (username, email, ids) = (user['name'], user['email'], user['id'])
            wallet = user['primaryWalletId']
            balancedata = get_wallet_balance(session['api_key'], wallet)
            balance = balancedata['data']
            rows.append((username, email, balance, ids))
    
    tasks_data=get_enabled_tasks(session['api_key'])
    tasks=[]
    for task in tasks_data['data']:
        tasks.append(task['name'])
    return render_template('dashboard/tasks.html', headers=headers, rows=rows, tasks=tasks)
