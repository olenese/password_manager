from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='flaskuser', password='Sol i Bergen!', server='172.105.131.62', database='flask_test')
    app.secret_key = "super secret key"

    

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for password-manager parts of app
    from .manager import manager as manager_blueprint
    app.register_blueprint(manager_blueprint)

    # blueprint for viewing the login parts of app
    from .viewlogins import viewlogins as manager_blueprint
    app.register_blueprint(manager_blueprint)

    # blueprint for changing a password
    from .editpassword import editpassword as editpassword_blueprint
    app.register_blueprint(editpassword_blueprint)



    return app
