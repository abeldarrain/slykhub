import functools
from .api import get_owner
from urllib.error import HTTPError
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from slykhub.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']
        api_key = request.form['api_key']
        db = get_db()
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
                    db.execute(
                        "INSERT INTO user (username, password, api_key) VALUES (?, ?, ?)",
                        (username, generate_password_hash(password), api_key),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"API key or username already exists"
                else:
                    flash('User created!', 'success')
                    return redirect(url_for("auth.login"))

        flash(error, 'error')

    return render_template('auth/sign_up.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['api_key'] = user['api_key']
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
            db = get_db()
            if not password:
                error = 'Password is required.'
            elif not 8<=len(password)<=20:
                error = "Password must be 8-20 characters"
            elif password_confirmation != password:
                error = "Passwords don't match"   
            if error is None:
                try:
                        db.execute(
                            'UPDATE user SET password = ? WHERE username = ?',
                            (generate_password_hash(password), username),
                        )
                        db.commit()
                except Exception as e:
                    error = e
                else:
                    session.clear()
                    flash('Successfully updated password', 'success')
                    return redirect(url_for("auth.login"))        
        else:
            username = request.form['username']
            api_key = request.form['api_key']
            db = get_db()
            error = None
            if not username:
                error = 'Username is required.'  
            elif not api_key:
                error = 'API key is required.'      
            if error is None:
                    user = db.execute(
                    'SELECT * FROM user WHERE username = ?', (username,)
                    ).fetchone()
                    if user is None:
                        error = 'Incorrect username.'
                    elif user['api_key'] != api_key:
                        error = 'Incorrect user API key.'
            if error is None:
                session['recover_username'] = username            
        if error:
            flash(error, 'error')
    return render_template('auth/recover.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view