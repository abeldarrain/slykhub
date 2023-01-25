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
        api_key = request.form['api_key']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not api_key:
            error = 'API key is required.'

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
                    return redirect(url_for("auth.login"))

        flash(error)

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
            return redirect(url_for('dashboard.home'))

        flash(error)

    return render_template('auth/login.html')

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