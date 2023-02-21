from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from slykhub.auth import login_required
from slykhub.db import get_db
from urllib.error import HTTPError
from .api import(
    get_verified_users , get_enabled_tasks,  
    get_wallet_balance, get_users, get_payment_methods,
    get_completed_transactions, get_orders, get_enabled_assets
)
from .postapi import complete_task
from .util import convert
from collections import OrderedDict


from datetime import timedelta
import datetime
from dateutil.relativedelta import relativedelta


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
    error = None
    if request.method == 'POST':
        selected_task = request.form['task']
        if not selected_task:
            error='No selected task'
        user_ids =request.form.getlist('taskcheckbox')
        if not user_ids:
            error='No selected users'
            
        if not error:
            print(f'User Tasks to complete: {len(user_ids)}')
            error=complete_task(selected_task, user_ids, session['api_key'])
            if error is not HTTPError:
                err422 = error
                succ = len(user_ids)-err422
                error = 'Selected users already completed the task' if succ == 0 else None
        if not error:  
            flash(f'Successfully completed task for {succ} users.', 'success')
            
    headers=('User','Email', 'Select All')
    #headers=('User','Email', 'Balance', 'Select All')
    rows=[]
    tasks=[]
    user_data = get_verified_users(session['api_key'])
    if isinstance(user_data,HTTPError):
        error = user_data
    else:
        for user in user_data['data']:
            if 'user' in user['roles']:
                (username, email, ids) = (user['name'], user['email'], user['id'])
                ######################### With Balance ################# 
                # wallet = user['primaryWalletId']
                # balancedata = get_wallet_balance(session['api_key'], wallet)
                # if balancedata is HTTPError:
                #     error = balancedata
                # else:  
                #     #balance = balancedata['data']
                #     #rows.append((username, email, balance, ids))
                ######################### Without Balance #################
                rows.append((username, email, ids))
                ######################### END #################
    tasks_data=get_enabled_tasks(session['api_key'])
    if tasks_data is HTTPError:
        error = tasks_data
    else:
        for task in tasks_data['data']:
            tasks.append(task['name'])
                
    if error:
        flash(error, 'error')
    return render_template('dashboard/tasks.html', headers=headers, rows=rows, tasks=tasks)

@bp.route('/sales')
@login_required
def sales():
    error=''
    orders = get_orders(session['api_key'])
    apiassets = get_enabled_assets(session['api_key'])
    eassets=[]
    if orders  is HTTPError:
        error = orders
    elif apiassets is HTTPError:
        error = apiassets
    for ea in apiassets['data']:
        eassets.append(ea['code'])   
    else: 
        ######################################Payment methods Chart################################
        payment_methods = {}
        orders_prices ={}
        orders_prices_asset = ''
        for o in orders['data']:
            pm = str.capitalize(o['chosenPaymentMethod'])
            oa = o['amount']
            orders_prices_asset = o['assetCode']
            if payment_methods.get(pm):
                payment_methods[pm] += 1  
            else:
                payment_methods[pm] = 1
            if orders_prices.get(oa):
                orders_prices[oa]+=1
            else:
                orders_prices[oa] = 1
        print (f'This is the payment methods dictionary: {payment_methods}')                       
        payment_methods_data = [{
                        'label': '# Successful payments',
                        'data': list(payment_methods.values()),
                        'borderWidth': 2,
                        'spacing': 1
                    }]
            
        ##################################Orders by Price Chart##############################   
        orders_prices_data =[]
        orders_prices_by_asset = []
        for sa in eassets:
            item = convert(session['api_key'],list(orders_prices.keys()), sa, orders_prices_asset)
            if isinstance(item,HTTPError):
                eassets.remove(sa)
            else:
                orders_prices_by_asset.append(item)
            
        
         
        orders_prices_data = [{
        'label': f'Amount of orders',
        'data': list(orders_prices.values()),
        'fill': False,
        'borderColor': 'rgb(75, 192, 192)',
        'tension': 0.1
        }]
        print(f'This is the Dict im sending {orders_prices_by_asset}')    
            
            
        #######################################End##########################    
        if error:
            flash(error, 'error')
        return render_template('dashboard/sales.html',
                           payment_methods=list(payment_methods.keys()), payment_methods_data=payment_methods_data,
                           orders_prices=orders_prices_by_asset, orders_prices_data = orders_prices_data,
                           assets=eassets)

@bp.route('/users')
@login_required
def users():
    error =''
    
        
        
    ############################################User Growth################3
    new_users_by_date ={}
    
    users = get_verified_users(session['api_key'])
    if isinstance(users,HTTPError):
        error = users
    else:
        for user in users['data']:
            date = user['createdAt']
            formated_date = date[:10]
            if new_users_by_date.get(formated_date):
                new_users_by_date[formated_date] += 1  
            else:
                new_users_by_date[formated_date] = 1
        new_users_by_date = dict(OrderedDict(sorted(new_users_by_date.items())))    
    # print(new_users_by_date)
    ################List of days from the beggining###################### 
    timelapses = ['Last week', 'Last 2 weeks', 'Last month', 'Last 3 months', 'Last 6 months', 'Last year', 'All']
       
    today = datetime.date.today()
    sdate = datetime.date.fromisoformat(list(new_users_by_date.keys())[0])
    edate = today
    date_list_complete = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    date_list_complete = list(map(lambda x: x.isoformat(), date_list_complete))
    # print (date_list_complete)
    
    ###########################List of days from 1y ago#########################
    sdate = today.replace(year= (today.year-1))
    date_list_year_ago =[sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    date_list_year_ago = list(map(lambda x: x.isoformat(), date_list_year_ago))
    #print (date_list_year_ago)

    ###########################List of days from 6m ago#########################
    sdate = today - relativedelta(months=6)
    date_list_six_months_ago =[sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    date_list_six_months_ago = list(map(lambda x: x.isoformat(), date_list_six_months_ago))
    #print (date_list_six_months_ago)
    
    ###########################List of days from 3m ago#########################
    sdate = today- relativedelta(months=3)
    date_list_three_months_ago =[sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    date_list_three_months_ago = list(map(lambda x: x.isoformat(), date_list_three_months_ago))
    #print (date_list_three_months_ago)
    
    ###########################List of days from 1m ago#########################
    sdate = today- relativedelta(months=1)
    date_list_one_month_ago =[sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    date_list_one_month_ago = list(map(lambda x: x.isoformat(), date_list_one_month_ago))
    #print (date_list_one_month_ago)
    
    ###########################List of days from 2w ago#########################
    sdate = today- relativedelta(weeks=2)
    date_list_two_weeks_ago =[sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    date_list_two_weeks_ago = list(map(lambda x: x.isoformat(), date_list_two_weeks_ago))
    #print (date_list_two_weeks_ago)
    
    ###########################List of days from 1w ago#########################
    sdate = today- relativedelta(weeks=1)
    date_list_one_week_ago =[sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    date_list_one_week_ago = list(map(lambda x: x.isoformat(), date_list_one_week_ago))
    #print (date_list_one_week_ago)
    
    # update dict for every date
    from .util import get_dict_user_growth
    
    new_users_by_date_complete = get_dict_user_growth(new_users_by_date, date_list_complete)
    new_users_by_date_1year = get_dict_user_growth(new_users_by_date, date_list_year_ago)
    new_users_by_date_6months = get_dict_user_growth(new_users_by_date, date_list_six_months_ago)
    new_users_by_date_3months = get_dict_user_growth(new_users_by_date, date_list_three_months_ago)
    new_users_by_date_1month = get_dict_user_growth(new_users_by_date, date_list_one_month_ago)
    new_users_by_date_2weeks = get_dict_user_growth(new_users_by_date, date_list_two_weeks_ago)
    new_users_by_date_1week = get_dict_user_growth(new_users_by_date, date_list_one_week_ago)
    
    
    new_users_by_date_complete_dataset = [{
                        'label': 'New users',
                        'data': list(new_users_by_date_complete.values()),
                        'borderWidth': 2,
                        'spacing': 1
                    }]
    new_users_by_date_1year_dataset = [{
                        'label': 'New users',
                        'data': list(new_users_by_date_1year.values()),
                        'borderWidth': 2,
                        'spacing': 1
                    }]
    new_users_by_date_6months_dataset = [{
                        'label': 'New users',
                        'data': list(new_users_by_date_6months.values()),
                        'borderWidth': 2,
                        'spacing': 1
                    }]
    new_users_by_date_3months_dataset = [{
                        'label': 'New users',
                        'data': list(new_users_by_date_3months.values()),
                        'borderWidth': 2,
                        'spacing': 1
                    }]
    new_users_by_date_1month_dataset = [{
                        'label': 'New users',
                        'data': list(new_users_by_date_1month.values()),
                        'borderWidth': 2,
                        'spacing': 1
                    }]
    new_users_by_date_2weeks_dataset = [{
                        'label': 'New users',
                        'data': list(new_users_by_date_2weeks.values()),
                        'borderWidth': 2,
                        'spacing': 1
                    }]
    new_users_by_date_1week_dataset = [{
                        'label': 'New users',
                        'data': list(new_users_by_date_1week.values()),
                        'borderWidth': 2,
                        'spacing': 1
                    }]
    ########################################Total users####################3
    
    from .util import get_stacked_users_dict
    
    total_users_complete = get_stacked_users_dict(new_users_by_date_complete, date_list_complete)
    total_users_1year = get_stacked_users_dict(new_users_by_date_complete, date_list_year_ago)
    total_users_6months = get_stacked_users_dict(new_users_by_date_complete, date_list_six_months_ago)
    total_users_3months = get_stacked_users_dict(new_users_by_date_complete, date_list_three_months_ago)
    total_users_1month = get_stacked_users_dict(new_users_by_date_complete, date_list_one_month_ago)
    total_users_2weeks = get_stacked_users_dict(new_users_by_date_complete, date_list_two_weeks_ago)
    total_users_1week = get_stacked_users_dict(new_users_by_date_complete, date_list_one_week_ago)
     
    
    total_users_complete_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_complete.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_1year_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_1year.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_6months_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_6months.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_3months_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_3months.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_1month_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_1month.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_2weeks_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_2weeks.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_1week_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_1week.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    
    ###############################Total active users####################
    
    
    
    
    
    
      
    #######################################################################
    if error:
        flash(error, 'error')
    return render_template('dashboard/users.html',
                           timelapses=timelapses,
                           date_list_complete = date_list_complete,
                           date_list_year_ago = date_list_year_ago,
                           date_list_six_months_ago=date_list_six_months_ago,
                           date_list_three_months_ago=date_list_three_months_ago,
                           date_list_one_month_ago=date_list_one_month_ago,
                           date_list_two_weeks_ago=date_list_two_weeks_ago,
                           date_list_one_week_ago=date_list_one_week_ago,
                           
                           new_users_by_date_complete_dataset=new_users_by_date_complete_dataset, 
                           new_users_by_date_1year_dataset=new_users_by_date_1year_dataset,
                           new_users_by_date_6months_dataset=new_users_by_date_6months_dataset,
                           new_users_by_date_3months_dataset=new_users_by_date_3months_dataset,
                           new_users_by_date_1month_dataset=new_users_by_date_1month_dataset,
                           new_users_by_date_2weeks_dataset=new_users_by_date_2weeks_dataset,
                           new_users_by_date_1week_dataset=new_users_by_date_1week_dataset,
                           
                           total_users_complete_dataset = total_users_complete_dataset,
                           total_users_1year_dataset = total_users_1year_dataset,
                           total_users_6months_dataset=total_users_6months_dataset,
                           total_users_3months_dataset=total_users_3months_dataset,
                           total_users_1month_dataset=total_users_1month_dataset,
                           total_users_2weeks_dataset=total_users_2weeks_dataset,
                           total_users_1week_dataset=total_users_1week_dataset
                           )
    
    
    
    