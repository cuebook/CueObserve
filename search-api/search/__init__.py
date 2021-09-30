from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurations
app.config.from_object("config")

db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)


# from .cardTemplates import views, models  # pylint: disable=W0404
from .globalDimensions import views, models  # pylint: disable=W0404

# if __name__ == "app":
#     app = create_app(env, args)
