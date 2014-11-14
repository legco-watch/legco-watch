#!/bin/bash

echo "Building containers"
docker build -t legcowatch/dbdata docker/dbdata
docker build -t legcowatch/logdata docker/logdata
docker build -t legcowatch/dbserver docker/dbserver
docker build -t legcowatch/appserver docker/appserver