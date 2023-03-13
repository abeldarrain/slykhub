from flask import (
    Blueprint, render_template
)

bp = Blueprint('help', __name__, url_prefix='/help')

@bp.route('/')
def help():
    return render_template('help.html')