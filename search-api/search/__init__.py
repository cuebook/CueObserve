# Import flask and template operators
from flask import Flask, render_template
from flask_migrate import Migrate


# Could import flask extensions, such as SQLAlchemy, here
from flask_sqlalchemy import SQLAlchemy

# Define WSGI object
app = Flask(__name__)

# Configurations
app.config.from_object('config')


# Some more example SQLAlchemy config
# Define the database object which is imported by modules and controllers
db = SQLAlchemy(app)


# # HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

# # Home page view
# @app.route('/')
# def home():
#     return render_template('home.html')


# Import modules here
from .cardTemplates import views, models
from .globalDimensions import views, models

migrate = Migrate()
migrate.init_app(app, db)


# if __name__ == "app":
#     app = create_app(env, args)
