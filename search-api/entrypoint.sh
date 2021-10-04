#!/bin/bash

source .env.dev
if [[ $ENVIRONMENT == "PRODUCTION" ]]
then
	echo production 
else
	export FLASK_ENV=development
	pip install ipython
	pip install -r requirements.txt
	chmod -R 777 /code/
	chown -R www-data:www-data /code/
fi
export FLASK_APP=search
# flask db init
# flask db migrate
flask db upgrade

exec "$@"
