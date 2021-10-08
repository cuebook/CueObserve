from flask import Flask, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)
CORS(app)


@app.after_request
def after_request(response):
    app.logger.info("response %s", response.headers)
    response.headers.add('Origin', "http://localhost:3000")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Configurations
app.config.from_object("config")

db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)


# from .cardTemplates import views, models  # pylint: disable=W0404
from .globalDimensions import views, models  # pylint: disable=W0404

# if __name__ == "app":
#     app = create_app(env, args)
