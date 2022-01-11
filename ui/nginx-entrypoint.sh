#!/usr/bin/env bash

set -eu

# envsubst '${API_HOST} ${API_PORT}' < /etc/nginx/conf.d/nginx-default.conf.template > /etc/nginx/conf.d/nginx-default.conf
if [[ "$ENVIRONMENT" = "PRODUCTION" ]] 
then
	echo "Running for PRODUCTION"
	envsubst '${NGINX_API_URL} ${NGINX_ALERT_API_URL} ${NGINX_SEARCH_API_URL} ${NGINX_UI_URL}' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf
else
	echo "Running for DEVELOPMENT"
	envsubst '${NGINX_API_URL} ${NGINX_ALERT_API_URL} ${NGINX_SEARCH_API_URL} ${NGINX_UI_URL}' < /etc/nginx/conf.d/nginx-dev.conf.template > /etc/nginx/conf.d/default.conf
fi

exec "$@"