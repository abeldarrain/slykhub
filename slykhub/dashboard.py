from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from slykhub.auth import login_required
from slykhub.db import get_db

from .api import get_users , get_enabled_tasks



bp = Blueprint('dashboard', __name__, url_prefix='/Dashboard')

@bp.route('/')
@login_required
def redir():
    return redirect(url_for('dashboard.home'))

@bp.route('/home')
@login_required
def home():
    return render_template('dashboard/home.html')

@bp.route('/tables')
@login_required
def tables():
    user_data = get_users(session['api_key'])
    headers=('#','User', 'Email', 'Select')
    rows=[]
    for user in user_data['data']:
        if 'user' in user['roles']:
            (username, email) = (user['name'], user['email'])
            rows.append((username, email))
    
    tasks_data=get_enabled_tasks(session['api_key'])
    tasks=[]
    for task in tasks_data['data']:
        (name, id, amount) = (task['name'], task['id'], task['amount'])
        tasks.append((name, id, amount))
    print (tasks)
    return render_template('dashboard/tables.html', headers=headers, rows=rows, tasks=tasks)
