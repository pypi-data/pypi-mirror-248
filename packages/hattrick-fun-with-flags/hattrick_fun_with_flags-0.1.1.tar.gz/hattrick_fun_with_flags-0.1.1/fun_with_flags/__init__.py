import os

from flask import (
    Flask,
    render_template,
    )

from . import auth
from . import flags



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.environ['FLASK_SECRET'],
    )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    # entry-point
    @app.route('/')
    def index():
        return render_template('index.html')



    app.register_blueprint(auth.bp_a)

    app.register_blueprint(flags.bp_f)


    return app
