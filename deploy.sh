#!/bin/bash

cp *.py $1/hvsi/
cp app.fcgi $1/hvsi/
cp app.wsgi $1/hvsi/
cp -r views $1/hvsi/

cp -r js $1/hvsi_static/
cp -r pdf $1/hvsi_static/
cp -r css $1/hvsi_static/
