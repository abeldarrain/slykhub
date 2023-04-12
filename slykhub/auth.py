import functools
from .api import get_owner
from urllib.error import HTTPError
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import *

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']
        api_key = request.form['api_key']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not api_key:
            error = 'API key is required.'
        elif password_confirmation != password:
            error = "Passwords don't match"
        elif not 8<=len(password)<=20:
            error = "Password must be 8-20 characters"
        elif not 4<=len(username)<=20:
            error = "Username must be 4-20 characters"
        elif any(char.isdigit() for char in username):
            error = "Username must not contain numbers"
        
        if error is None:
            owner = get_owner(api_key)
            if isinstance(owner, HTTPError):
               error = 'API key could not be found'
            else:
                try:
                    # with db.session as db.session:
                        try:
                            if User.query.filter_by(username=username).first() is None:
                                new_user = User(username=username, password=generate_password_hash(password))
                                db.session.add(new_user)
                                if Slyk.query.filter_by(api_key=api_key).first() is None:
                                    new_slyk=Slyk(user_id=new_user.id, name=owner['data'][0]['name'], api_key=api_key)
                                    db.session.add(new_slyk)
                                    
                                    
                                    try:
                                        db.session.commit()
                                        new_user.active_slyk_id = new_slyk.id
                                        db.session.commit()
                                    except Exception as e:
                                        error = 'Error creating new user and new slyk'
                                        print(e)
                                    else:
                                        flash('User created!', 'success')
                                        return redirect(url_for("auth.login"))
                                else:
                                    error = 'Slyk API key already exist for an user'
                            else:
                                error = f"Username already exists"
                        except Exception as e:
                            print(e)
                            error = e
                            raise e
                except Exception as e:
                    print(e)
                    print('Could not connect to database')
                    error = e
                    raise e
        flash(error, 'error')

    return render_template('auth/sign_up.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            active_slyk = Slyk.query.filter_by(id=user.active_slyk_id).first()
            session['api_key'] = active_slyk.api_key
            session['active_slyk'] = active_slyk.name
            return redirect(url_for('dashboard.home'))

        flash(error, 'error')

    return render_template('auth/login.html')

@bp.route('/recover', methods=('GET', 'POST'))
def recover():
    if request.method == 'POST':
        if session.get('recover_username'):
            username = session['recover_username']
            password = request.form['password']
            password_confirmation = request.form['password_confirmation'] 
            error = None
            if not password:
                error = 'Password is required.'
            elif not 8<=len(password)<=20:
                error = "Password must be 8-20 characters"
            elif password_confirmation != password:
                error = "Passwords don't match"   
            if error is None:
                try:
                        user = User.query.filter_by(username=username).first()
                        user.password = generate_password_hash(password) 
                        db.session.commit()
                except Exception as e:
                    print(e)
                    error = e
                else:
                    session.clear()
                    flash('Successfully updated password', 'success')
                    return redirect(url_for("auth.login"))        
        else:
            username = request.form['username']
            api_key = request.form['api_key']
            error = None
            if not username:
                error = 'Username is required.'  
            elif not api_key:
                error = 'API key is required.'      
            if error is None:
                    user = User.query.filter_by(username=username).first()
                    if user is None:
                        error = 'Incorrect username.'
                    else:
                        error = 'Incorrect API key.'
                        for slyk in user.slyks:
                            if slyk.api_key == api_key:
                                error = None
            if error is None:
                session['recover_username'] = username            
        if error:
            flash(error, 'error')
    return render_template('auth/recover.html')


@bp.route('/owner', methods=['GET', 'POST'])
@login_required
def owner():
    if request.method == 'POST':
        slyk_id = request.form['slyk_id']
        slyk = Slyk.query.filter_by(id=slyk_id).first()
        slyk_user = User.query.filter_by(id = slyk.user_id).first()
        slyk_user.active_slyk_id = slyk.id
        db.session.commit()
        session['api_key'] = slyk.api_key
        session['active_slyk'] = slyk.name

    
    return render_template('auth/owner.html')

@bp.route('/owner/add_slyk', methods=['POST'])
@login_required
def add_slyk():
    error=''
    api_key = request.form['api_key']
    owner = get_owner(api_key)
    if isinstance(owner,Exception):
        error='Slyk not found'
    else:
        if Slyk.query.filter_by(api_key=api_key).first() is None:
            print(owner)
            new_slyk=Slyk(user_id=g.user.id, name=owner['data'][0]['name'], api_key=api_key)
            db.session.add(new_slyk)
            try:
                db.session.commit()
            except Exception as e:
                error = 'Error adding slyk'
                print(e)
            else:
                flash('Slyk created!', 'success')
                return redirect(url_for("auth.owner"))
        else:
                error = 'Slyk API key already exist for an user'
    flash(error, 'error')

    return redirect(url_for("auth.owner"))
    
@bp.route('/owner/del_slyk', methods=['POST'])
@login_required
def delete_slyk():
    id = request.form['slyk_for_delete']
    try:
        slyk = Slyk.query.filter_by(id=id).first()
        db.session.delete(slyk)
        db.session.commit()
        flash('Slyk successfully deleted!', 'success')
    except Exception as e:
        error = 'Could not delete Slyk'
        print(error)
        flash(error, 'error')
    return redirect(url_for("auth.owner"))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

