from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from slykhub.auth import login_required
from slykhub.db import get_db

bp = Blueprint('dashboard', __name__)

@bp.route('/home')
@login_required
def home():
    return render_template('dashboard/home.html')

