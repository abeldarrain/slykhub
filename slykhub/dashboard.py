from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
import asyncio
import aiohttp
from slykhub.auth import login_required
from . import db
from urllib.error import HTTPError
from .api import(
    get_verified_users , get_enabled_tasks,  
    get_wallets_balance, get_wallet_balance, get_users, get_payment_methods,
    get_completed_transactions, get_orders, get_enabled_assets,
    get_user_by_id, get_completed_tasks_transactions, get_task_by_id, get_order_details_by_id,
    get_orders_for_user, get_product_by_id
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
        #########################ORDERS BY DATE CHART##############################
        from .util import get_dict_user_growth
        orders_by_date = {}
        
        for order in orders['data']:
            date = order['createdAt']
            formated_date = date[:10]
            if orders_by_date.get(formated_date):
                orders_by_date[formated_date] += 1  
            else:
                orders_by_date[formated_date] = 1
        
            
        ################List of days from the beggining###################### 
        timelapses = ['Last week', 'Last 2 weeks', 'Last month', 'Last 3 months', 'Last 6 months', 'Last year', 'All']
        
        today = datetime.date.today()
        if list(orders_by_date.keys()):
            sdate = datetime.date.fromisoformat(list(orders_by_date.keys())[0])
        else:
            sdate = today - relativedelta(days=1)
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
        
        from .util import get_dict_orders_growth
        orders_by_date = dict(OrderedDict(sorted(orders_by_date.items())))
        
        
        orders_by_date_complete = get_dict_user_growth(orders_by_date, date_list_complete)
        orders_by_date_1year = get_dict_user_growth(orders_by_date, date_list_year_ago)
        orders_by_date_6months = get_dict_user_growth(orders_by_date, date_list_six_months_ago)
        orders_by_date_3months = get_dict_user_growth(orders_by_date, date_list_three_months_ago)
        orders_by_date_1month = get_dict_user_growth(orders_by_date, date_list_one_month_ago)
        orders_by_date_2weeks = get_dict_user_growth(orders_by_date, date_list_two_weeks_ago)
        orders_by_date_1week = get_dict_user_growth(orders_by_date, date_list_one_week_ago)
        
        
        orders_by_date_complete_dataset = [{
                            'label': 'New orders',
                            'data': list(orders_by_date_complete.values()),
                            'borderWidth': 2,
                            'spacing': 1
                        }]
        orders_by_date_1year_dataset = [{
                            'label': 'New orders',
                            'data': list(orders_by_date_1year.values()),
                            'borderWidth': 2,
                            'spacing': 1
                        }]
        orders_by_date_6months_dataset = [{
                            'label': 'New orders',
                            'data': list(orders_by_date_6months.values()),
                            'borderWidth': 2,
                            'spacing': 1
                        }]
        orders_by_date_3months_dataset = [{
                            'label': 'New orders',
                            'data': list(orders_by_date_3months.values()),
                            'borderWidth': 2,
                            'spacing': 1
                        }]
        orders_by_date_1month_dataset = [{
                            'label': 'New orders',
                            'data': list(orders_by_date_1month.values()),
                            'borderWidth': 2,
                            'spacing': 1
                        }]
        orders_by_date_2weeks_dataset = [{
                            'label': 'New orders',
                            'data': list(orders_by_date_2weeks.values()),
                            'borderWidth': 2,
                            'spacing': 1
                        }]
        orders_by_date_1week_dataset = [{
                        'label': 'New orders',
                            'data': list(orders_by_date_1week.values()),
                            'borderWidth': 2,
                            'spacing': 1
                        }]
        
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
        #########################################TOP BuYERS###############################
        from .util import get_top_buyers_by_amount, get_top_buyers_by_frequency
        
        top_buyers_by_amount={}
        top_buyers_by_frequency ={}
        top_buyers_labels = ['Name', 'Amount', 'Asset']
        user_data = get_verified_users(session['api_key'])
        if isinstance(user_data,HTTPError):
            error = user_data
        else:   
            top_buyers_by_amount = get_top_buyers_by_amount(orders, user_data)
            top_buyers_by_frequency = get_top_buyers_by_frequency(orders, user_data)
        
        # print(f'USERS BY AMOUNT LIST: {top_buyers_by_amount}')
        # print('######################################################')
        # print(f'USERS BY FREQUENCY LIST: {top_buyers_by_frequency}')
        
        top_buyers_by_amount = sorted(list(top_buyers_by_amount.values()), key=lambda x: x[1], reverse=True)
        top_buyers_by_frequency = sorted(list(top_buyers_by_frequency.values()), key=lambda x: x[1], reverse=True)
        
        #print(f'USERS BY AMOUNT LIST SORTED: {top_buyers_by_amount}')
        # print('######################################################')
        #print(f'USERS BY FREQUENCY LIST SORTED: {top_buyers_by_frequency}')
        
        top_buyers_by_amount_names = []
        top_buyers_by_amount_data =  []
        for i in top_buyers_by_amount:
            top_buyers_by_amount_names.append(i[0])
            top_buyers_by_amount_data.append(i[1])
        
        
        top_buyers_by_frequency_names = []
        top_buyers_by_frequency_data = []
        for i in top_buyers_by_frequency:
            top_buyers_by_frequency_names.append(i[0])
            top_buyers_by_frequency_data.append(i[1])
        
       
        
        #######################################End##########################    
        if error:
            flash(error, 'error')
        return render_template('dashboard/sales.html',
                           payment_methods=list(payment_methods.keys()), payment_methods_data=payment_methods_data,
                           orders_prices=orders_prices_by_asset, orders_prices_data = orders_prices_data,
                           assets=eassets,
                           timelapses=timelapses,
                           date_list_complete = date_list_complete,
                           date_list_year_ago = date_list_year_ago,
                           date_list_six_months_ago=date_list_six_months_ago,
                           date_list_three_months_ago=date_list_three_months_ago,
                           date_list_one_month_ago=date_list_one_month_ago,
                           date_list_two_weeks_ago=date_list_two_weeks_ago,
                           date_list_one_week_ago=date_list_one_week_ago,
                           
                           orders_by_date_complete_dataset=orders_by_date_complete_dataset, 
                           orders_by_date_1year_dataset=orders_by_date_1year_dataset,
                           orders_by_date_6months_dataset=orders_by_date_6months_dataset,
                           orders_by_date_3months_dataset=orders_by_date_3months_dataset,
                           orders_by_date_1month_dataset=orders_by_date_1month_dataset,
                           orders_by_date_2weeks_dataset=orders_by_date_2weeks_dataset,
                           orders_by_date_1week_dataset=orders_by_date_1week_dataset,
                           
                           top_buyers_labels=top_buyers_labels,
                           top_buyers_by_amount = top_buyers_by_amount,
                           top_buyers_by_frequency = top_buyers_by_frequency
                           )

@bp.route('/users')
@login_required
def users():
    error =''   
    
    
    orders = get_orders(session['api_key'])
    if isinstance(orders,Exception):
        error = orders        
    user_table_headers=('User','Email', 'Balance')
    user_table_rows=[]
    users = asyncio.run(get_verified_users(session['api_key']))
    if isinstance(users,HTTPError):
        error = users
    else:
        wallets=[]
        users_depurated = []
        for user in users['data']:
            if 'user' in user['roles']:
                wallets.append(user['primaryWalletId'])
                users_depurated.append(user)
        balances = asyncio.run(get_wallets_balance(session['api_key'],wallets))
        for indx, user in enumerate(users_depurated):
            (username, email, ids) = (user['name'], user['email'], user['id'])
            ######################### With Balance ################# 
            # try:
            balancedata = balances[indx]
            # except:
            #     balancedata = {'data' : []}
            balance = [{'assetCode': 'balance', 'amount': 'empty'}] if not balancedata['data'] else balancedata['data']
            print(f'BALANCE FOR {username} is {balance} WITH WALLET ID {user["primaryWalletId"]}')
            user_table_rows.append((username, email, ids, balance))
                
                ######################### END #################
        
    ############################################User Growth################3
    new_users_by_date ={}
    
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
    
    from .util import get_stacked_users_dict, get_stacked_active_users_dict
    
    total_users_complete = get_stacked_users_dict(new_users_by_date_complete, date_list_complete)
    total_users_1year = get_stacked_users_dict(new_users_by_date_complete, date_list_year_ago)
    total_users_6months = get_stacked_users_dict(new_users_by_date_complete, date_list_six_months_ago)
    total_users_3months = get_stacked_users_dict(new_users_by_date_complete, date_list_three_months_ago)
    total_users_1month = get_stacked_users_dict(new_users_by_date_complete, date_list_one_month_ago)
    total_users_2weeks = get_stacked_users_dict(new_users_by_date_complete, date_list_two_weeks_ago)
    total_users_1week = get_stacked_users_dict(new_users_by_date_complete, date_list_one_week_ago)
       ###############################Total active users####################
    total_active_users_complete = get_stacked_active_users_dict(orders, date_list_complete, date_list_complete)
    total_active_users_1year = get_stacked_active_users_dict(orders, date_list_year_ago, date_list_complete)
    total_active_users_6months = get_stacked_active_users_dict(orders, date_list_six_months_ago, date_list_complete)
    total_active_users_3months = get_stacked_active_users_dict(orders, date_list_three_months_ago, date_list_complete)
    total_active_users_1month = get_stacked_active_users_dict(orders, date_list_one_month_ago, date_list_complete)
    total_active_users_2weeks = get_stacked_active_users_dict(orders, date_list_two_weeks_ago, date_list_complete)
    total_active_users_1week = get_stacked_active_users_dict(orders, date_list_one_week_ago, date_list_complete)
    
    total_users_complete_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_complete.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    },
                                   {
       'label': 'Total active users',
                        'data': list(total_active_users_complete.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_1year_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_1year.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    },
                                {
       'label': 'Total active users',
                        'data': list(total_active_users_1year.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_6months_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_6months.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    },
                                  {
       'label': 'Total active users',
                        'data': list(total_active_users_6months.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_3months_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_3months.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    },
                                  {
       'label': 'Total active users',
                        'data': list(total_active_users_3months.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_1month_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_1month.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    },
                                 {
       'label': 'Total active users',
                        'data': list(total_active_users_1month.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_2weeks_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_2weeks.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    },
                                 {
       'label': 'Total active users',
                        'data': list(total_active_users_2weeks.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]
    total_users_1week_dataset =[{
       'label': 'Total users',
                        'data': list(total_users_1week.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    },
                                {
       'label': 'Total active users',
                        'data': list(total_active_users_1week.values()),
                        'borderWidth': 2,
                        'spacing': 1        
    }]

     
    #######################################################################
    if error:
        flash(error, 'error')
    return render_template('dashboard/users.html',
                           user_table_headers=user_table_headers,
                           user_table_rows=user_table_rows,
                           
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
    
    
@bp.route('/users/<id>', methods=['GET', 'POST'])
@login_required
def user(id):
    user_data = get_user_by_id(session['api_key'],id)['data']
    wallet_id = user_data['primaryWalletId']
        
    ###################################username, Blocked, balance, email, date joined #################################
    from .postapi import block_user, unblock_user
    username = user_data['name']
    if request.method == 'POST':
        user_blocked = user_data['blocked']
        print(f'THIS IS A POST REQUEST AND THE USER STATUS IS {user_blocked}')
        unblock_user(session['api_key'],id) if user_blocked else block_user(session['api_key'],id)
        user_data = get_user_by_id(session['api_key'],id)['data']
    user_blocked = user_data['blocked']
    date_joined = user_data['createdAt'][:10]  
    user_email = user_data['email']
    user_phone = user_data['phone'] if user_data['phone'] else 'Not Available'
    user_balance = get_wallet_balance(session['api_key'], wallet_id) 
    
    
    ###############################Completed tasks #############################
    tasks_table_headers = ['Task', 'Amount', 'Date completed']
    
    completed_tasks_overall = get_completed_tasks_transactions(session['api_key'], wallet_id)
    
    tasks_completed_by_user = []
    
    for cto in completed_tasks_overall['data']:
        task_date = str(cto['processedAt'])[:10]
        task = get_task_by_id(session['api_key'], cto['taskId'])
        task_name = task['data']['name'] 
        task_amount = task['data']['amount']
        tasks_completed_by_user.append([task_name,task_amount, task_date])
    
    
    ###########################################Orders & Products #################################
    product_table_data = []
    product_table_headers = ['Name', 'Quantity', 'Price', 'Date']
    fulfilled_orders = get_orders_for_user(session['api_key'], id)
    orders_by_date = {}
    
    for order in fulfilled_orders['data']:
        date = order['createdAt']
        formated_date = date[:10]
        if orders_by_date.get(formated_date):
            orders_by_date[formated_date] += 1  
        else:
            orders_by_date[formated_date] = 1
                
        details = get_order_details_by_id(session['api_key'],order['id'])
        print(f'THE DETAILS: {details}')
        product = get_product_by_id(session['api_key'],details['data'][0]['productId'])
        product_name = product['data']['name']
        product_quantity = details['data'][0]['quantity']
        order_date = details['data'][0]['fulfilledAt'][:10]
        product_price = product['data']['price']
        product_asset = product['data']['assetCode']
        product_table_data.append([product_name,product_quantity, (str(product_price)+' '+str(product_asset)),order_date] )
    
    from .util import get_dict_user_growth
    orders_by_date = dict(OrderedDict(sorted(orders_by_date.items())))
    today = datetime.date.today()
    sdate = datetime.date.fromisoformat(date_joined)
    edate = today
    date_list_complete = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    date_list_complete = list(map(lambda x: x.isoformat(), date_list_complete))
    orders_by_date_complete = get_dict_user_growth(orders_by_date, date_list_complete)
    orders_by_date_complete_dataset = [{
                    'label': 'Purchased orders since joined',
                    'data': list(orders_by_date_complete.values()),
                    'borderWidth': 2,
                    'spacing': 1
                }]
    
    print(f'THIS IS THE TABLE DATA: {product_table_data}')
    print(f'THIS IS THE CHART DATA: {orders_by_date_complete}')
    return render_template('dashboard/user_view.html',
                           username=username,
                            date_joined=date_joined,
                            tasks_table_headers = tasks_table_headers,
                            tasks_completed_by_user = tasks_completed_by_user,
                            user_blocked=user_blocked,
                            user_email = user_email,
                            user_phone = user_phone,
                            user_balance = user_balance,
                            
                            product_table_headers = product_table_headers,
                            product_table_data = product_table_data,
                            
                            date_list_complete=date_list_complete,
                            orders_by_date_complete_dataset=orders_by_date_complete_dataset
                            )
    