from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


# Import Configuration
from config import config


# Load Environment Variables
load_dotenv()


# Initialize Extensions

mysql = MySQL()

bcrypt = Bcrypt()

login_manager = LoginManager()

mail = Mail()

migrate = Migrate()



def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )


    # Load Configuration

    environment = os.environ.get(
        "FLASK_ENV",
        "development"
    )

    app.config.from_object(
        config[environment]
    )


    # Database Configuration

    app.config["MYSQL_HOST"] = app.config["MYSQL_HOST"]

    app.config["MYSQL_USER"] = app.config["MYSQL_USER"]

    app.config["MYSQL_PASSWORD"] = app.config["MYSQL_PASSWORD"]

    app.config["MYSQL_DB"] = app.config["MYSQL_DATABASE"]

    app.config["MYSQL_PORT"] = app.config["MYSQL_PORT"]



    # Initialize Extensions

    mysql.init_app(app)

    bcrypt.init_app(app)

    login_manager.init_app(app)

    mail.init_app(app)

    migrate.init_app(
        app,
        mysql
    )

    CORS(app)



    # Login Manager Configuration

    login_manager.login_view = "auth.login"

    login_manager.login_message = (
        "Please login to access this page."
    )



    # Create Upload Directories

    upload_folders = [

        app.config["UPLOAD_FOLDER"],

        app.config["BOOK_UPLOAD_FOLDER"],

        app.config["COVER_UPLOAD_FOLDER"],

        app.config["LOG_FOLDER"]

    ]


    for folder in upload_folders:

        if not os.path.exists(folder):

            os.makedirs(folder)



    # Register Blueprints

    from routes.auth import auth

    from routes.books import books

    from routes.user import user

    from routes.admin import admin



    app.register_blueprint(
        auth,
        url_prefix="/auth"
    )


    app.register_blueprint(
        books,
        url_prefix="/books"
    )


    app.register_blueprint(
        user,
        url_prefix="/user"
    )


    app.register_blueprint(
        admin,
        url_prefix="/admin"
    )




    # Home Route

    @app.route("/")
    def index():

        return render_template(
            "index.html"
        )




    # Error Handlers


    @app.errorhandler(404)
    def page_not_found(error):

        return render_template(
            "404.html"
        ),404



    @app.errorhandler(500)
    def server_error(error):

        return render_template(
            "500.html"
        ),500



    return app





# =========================================================
# User Loader
# =========================================================

@login_manager.user_loader
def load_user(user_id):

    from models.user import User

    return User.get_by_id(
        user_id
    )





# =========================================================
# Create Flask App
# =========================================================

app = create_app()


# =========================================================
# Application Start
# =========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )