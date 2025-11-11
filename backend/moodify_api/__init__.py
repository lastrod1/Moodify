from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():

    app = Flask(__name__)


    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'moodify.db')
    app.config['SECRET_KEY'] = '1234'

    # blah blah
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    #CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})


    from moodify_api.main.routes import main as main_bp
    app.register_blueprint(main_bp, url_prefix='/api')

    from moodify_api.auth.routes import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app