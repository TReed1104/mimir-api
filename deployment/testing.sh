#!/bin/sh
echo ---------------------------------------
echo Deployment Start - Testing
echo ---------------------------------------
echo Building and Deploying Mimir API
echo ---------------------------------------
docker-compose -p mimir-api-testing -f docker-compose.test.yml up -d --build --remove-orphans
echo
echo ---------------------------------------
echo Conntainer Status:
echo ---------------------------------------
docker ps | grep 'mimir-api'