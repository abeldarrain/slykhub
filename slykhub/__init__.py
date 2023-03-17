import os
from datetime import timedelta
from flask import Flask, render_template, redirect, url_for, session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='qwer1234',
        DATABASE=os.path.join(app.instance_path, 'slykhub.sqlite'),
    )
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=60)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/', methods=['GET'])
    def index():
    #    return redirect(url_for("auth.login"))
        session.clear()
        return render_template('index.html')
    

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')
    
    from . import help
    app.register_blueprint(help.bp)
    
    return app
    