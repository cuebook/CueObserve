from flask.cli import FlaskGroup
from search import app

cli = FlaskGroup(app)
# @cli.command()

if __name__ == "__main__":
    cli()
