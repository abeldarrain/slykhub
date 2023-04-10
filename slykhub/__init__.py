import os
from datetime import timedelta
from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = '129j12jd01k-k129i1092djijd01j'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=60)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5433/slykhub_db"

db = SQLAlchemy(app)
from flask_migrate import Migrate
migrate = Migrate(app, db)
from .models import User, Slyk




# a simple page that says hello
@app.route('/', methods=['GET'])
def index():
#    return redirect(url_for("auth.login"))
    session.clear()
    return render_template('index.html')





from . import auth
app.register_blueprint(auth.bp)

from . import dashboard
app.register_blueprint(dashboard.bp)
app.add_url_rule('/', endpoint='index')

from . import help
app.register_blueprint(help.bp)

