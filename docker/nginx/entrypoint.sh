#!/bin/bash

envsubst '${SERVICE_GATEWAY_SERVER_NAME}' < /etc/nginx/conf.d/servicegateway.conf.template > /etc/nginx/conf.d/servicegateway.conf

envsubst '${MASTER_DATA_SERVER_NAME}' < /etc/nginx/conf.d/masterdata.conf.template > /etc/nginx/conf.d/masterdata.conf

envsubst '${IDENTITY_MANAGER_SERVER_NAME}' < /etc/nginx/conf.d/identitymanager.conf.template > /etc/nginx/conf.d/identitymanager.conf

# Start Nginx
exec nginx -g 'daemon off;'