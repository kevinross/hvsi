#!/bin/bash

if [ -z "$1" ]; then
	echo "You need to supply the path to public_html (including public_html)!";
	exit 1;
fi
cp app.fcgi $1/hvsi/;

for i in *.py views; do
	rm -r $1/hvsi/app/$i;
	cp -r $i $1/hvsi/app/$i;
done

for i in js pdf css; do
	rm -r $1/hvsi_static/$i;
	cp -r $i $1/hvsi_static/$i;
done
