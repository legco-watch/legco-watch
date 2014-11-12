#!/bin/bash

export DB_USER=legcowatchdb
export DB_PASSWORD=e8aVqxwaKVXMfBT
export DB_NAME=legcowatch


# Create the user and DB

echo "******CREATING DOCKER DATABASE******"
gosu postgres postgres --single << EOF
CREATE USER ${DB_USER} WITH NOSUPERUSER CREATEDB PASSWORD '${DB_PASSWORD}';
CREATE DATABASE ${DB_NAME} WITH OWNER=${DB_USER} TEMPLATE=template0 ENCODING='UTF-8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8';
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} to ${DB_USER};
EOF
echo ""
echo "******DOCKER DATABASE CREATED******"
